# Copyright (C) 2023  Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions of
# the GNU General Public License v.2, or (at your option) any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY expressed or implied, including the implied warranties of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.  You should have received a copy of the
# GNU General Public License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.  Any Red Hat trademarks that are incorporated in the
# source code or documentation are not subject to the GNU General Public
# License and may only be used or replicated with the express permission of
# Red Hat, Inc.
#
# Red Hat Author(s): Todd Gill <tgill@redhat.com>
#

from concurrent import futures
import threading
import logging
import argparse
import os
import sys
import grpc


import csi_pb2
from csi_pb2 import ControllerServiceCapability
from csi_pb2_grpc import ControllerServicer
import json
import stratis


VOLUME_GROUP_NAME = "springfield"

file_handler = logging.FileHandler(filename="/tmp/csi_driver.log")
stdout_handler = logging.StreamHandler(stream=sys.stdout)
handlers = [file_handler, stdout_handler]

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s",
    handlers=handlers,
)

logger = logging.getLogger("LOGGER_NAME")


volume_list = list()
vg_list = list()
disks_to_use = list()
volume_group = None


class VolumeMap:
    def __init__(self, real_name, blivet_name, csi_volume, lv):
        self.real_name = real_name
        self.csi_volume = csi_volume
        self.lv = lv
        self.published_path = None


def get_major_minor_str(device):
    return str(device.major) + ":" + str(device.minor)


def get_volume(volume_id):
    print("Searching for {}", volume_id)
    for volume_map in volume_list:
        print("compare to : {}", volume_map.csi_volume.volume_id)
        if volume_map.csi_volume.volume_id == volume_id:
            print("found: {}", volume_id)
            return volume_map
    return None


def print_volume_list():
    print("Volume List:")
    for volume_map in volume_list:
        print("Volume ID : ", volume_map.csi_volume.volume_id)
        print("\tCapacity : ", volume_map.csi_volume.capacity_bytes)
    print("Device Tree:")
    print("\n")


def destroy(device):
    """Schedule actions as needed to ensure the pool does not exist."""
    if device is None:
        return

    ancestors = device.ancestors  # ascending distance ordering

    dbus_handle.devicetree.recursive_remove(device)
    ancestors.remove(device)
    leaves = [a for a in ancestors if a.isleaf]
    while leaves:
        for ancestor in leaves:

            if ancestor.is_disk:
                dbus_handle.devicetree.recursive_remove(ancestor)
            else:
                dbus_handle.destroy_device(ancestor)

            ancestors.remove(ancestor)

        leaves = [a for a in ancestors if a.isleaf]

    device = None


def get_capability(capability):
    access_type = capability.WhichOneof("access_type")

    if access_type == "mount":
        return csi_pb2.VolumeCapability(
            mount=csi_pb2.VolumeCapability.MountVolume(
                fs_type=capability.mount.fs_type
            ),
            access_mode=csi_pb2.VolumeCapability.AccessMode(
                mode=capability.access_mode.mode
            ),
        )

    return csi_pb2.VolumeCapability(
        mount=csi_pb2.VolumeCapability.BlockVolume(),
        access_mode=csi_pb2.VolumeCapability.AccessMode(
            mode=capability.access_mode.mode
        ),
    )


def get_volume_name(request):
    return request.name[: min(len(request.name), 55)]


class SpringfieldControllerService(ControllerServicer):
    def __init__(self, nodeid):
        self.nodeid = nodeid

    def CreateVolume(self, request, context):

        logger.info("CreateVolume()")
        sys.stdout.flush()
        sys.stderr.flush()

        # Validate the parameters for the request
        if request.name == None:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Must include volume name")

        request_name = request.name

        logger.info("CreateVolume name =", request_name)
        sys.stdout.flush()
        sys.stderr.flush()

        name = get_volume_name(request)

        if request.capacity_range.required_bytes:
            size = request.capacity_range.required_bytes
        elif request.capacity_range.limit_bytes:
            size = request.capacity_range.limit_bytes
        else:  # TODO: default to 10 MiB?
            size = 10485760

        print_volume_list()
        volume_map = get_volume(request.name)

        # If the volume already exits - just return success
        if volume_map != None:
            if (
                volume_map.csi_volume.capacity_bytes
                == request.capacity_range.limit_bytes
                or volume_map.csi_volume.capacity_bytes
                == request.capacity_range.required_bytes
            ):
                return csi_pb2.CreateVolumeResponse(volume=volume_map.csi_volume)
            else:
                context.abort(
                    grpc.StatusCode.ALREADY_EXISTS,
                    "Volume already exists with different capacity",
                )

        if len(request.volume_capabilities) == 0:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT, "Must have at least one capabiltiy"
            )

        for capability in request.volume_capabilities:
            print(capability)
            fstype = capability.mount.fs_type

            access_type = capability.WhichOneof("access_type")
            assert access_type == "mount" or access_type == "block"

            if fstype not in ["xfs", "btrfs", "ext4", ""]:
                context.abort(
                    grpc.StatusCode.INVALID_ARGUMENT,
                    "Unsupported filesystem type: {fstype}",
                )
            if fstype == "":
                fstype = "xfs"

            if capability.access_mode.mode not in [
                csi_pb2.VolumeCapability.AccessMode.Mode.SINGLE_NODE_WRITER
            ]:
                context.abort(
                    grpc.StatusCode.INVALID_ARGUMENT,
                    "Unsupported access mode: {csi_pb2.VolumeCapability.AccessMode.Mode.Name(volume_capability.access_mode.mode)}",
                )

        if 

        csi_volume = csi_pb2.Volume(
            volume_id=request.name,
            capacity_bytes=size,
            accessible_topology=[
                csi_pb2.Topology(segments={"hostname": os.uname().nodename})
            ],
        )
        volume_map = VolumeMap(request.name, name, csi_volume, lv)

        volume_list.append(volume_map)
        print_volume_list()
        return csi_pb2.CreateVolumeResponse(volume=csi_volume)

    def DeleteVolume(self, request, context):
        logger.info("DeleteVolume()")
        if request.volume_id == None or request.volume_id == "":
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Must include volume_id")

        volume_map = volume_map = get_volume(request.volume_id)

        if volume_map == None:
            return csi_pb2.DeleteVolumeResponse()

        dbus_handle.reset()

        # TODO: catch the errors thrown by do_it()
        try:
            device = dbus_handle.devicetree.get_device_by_path(volume_map.device.path)
            if device == None:
                context.abort(
                    grpc.StatusCode.ABORTED, "An exception occurred: {}".format(error)
                )

            dbus_handle.destroy_device(device)
            dbus_handle.do_it()
        except BaseException as error:
            print("An exception occurred: {}".format(error))
            context.abort(
                grpc.StatusCode.ABORTED, "An exception occurred: {}".format(error)
            )

        for volume_map in volume_list:
            if volume_map.csi_volume.volume_id == request.volume_id:
                volume_list.remove(volume_map)

        print_volume_list()
        # TODO: successful delete just returns and empty response?
        return csi_pb2.DeleteVolumeResponse()

    def ControllerPublishVolume(self, request, context):
        logger.info("ControllerPublishVolume()")
        access_type = request.volume_capability.WhichOneof("access_type")

        if access_type == None:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "Must include volume_capability access_type",
            )
        if request.volume_id == None or request.volume_id == "":
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Must include volume_id")

        if request.node_id == None or request.node_id == "":
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Must include volume_id")

        volume_map = get_volume(request.volume_id)

        if volume_map == None:
            context.abort(
                grpc.StatusCode.NOT_FOUND, "request.target_path does not exits"
            )

        if request.node_id != self.nodeid:
            context.abort(grpc.StatusCode.NOT_FOUND, "Mismatched node id")
        publish_context = {
            "real_name": volume_map.real_name,
            "blivet_name": volume_map.device.name,
            "dev_path": volume_map.device.path,
        }

        return csi_pb2.ControllerPublishVolumeResponse(publish_context=publish_context)

    def ControllerUnpublishVolume(self, request, context):
        logger.info("ControllerUnpublishVolume()")
        if request.volume_id == None or request.volume_id == "":
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Must include volume_id")

        volume_map = volume_map = get_volume(request.volume_id)

        if volume_map == None:
            return csi_pb2.ControllerUnpublishVolumeResponse()
        return csi_pb2.ControllerUnpublishVolumeResponse()

    def ValidateVolumeCapabilities(self, request, context):
        logger.info("ValidateVolumeCapabilities()")
        if request.volume_id == None or request.volume_id == "":
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Must include volume_id")

        try:
            volume_capability = request.volume_capabilities[0]
            print("capability = ", volume_capability)
        except IndexError as e:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT, "Must include volume_capabilities"
            )

        volume_map = get_volume(request.volume_id)

        if volume_map == None:
            context.abort(
                grpc.StatusCode.NOT_FOUND, "request.target_path does not exits"
            )

        access_type = volume_capability.WhichOneof("access_type")

        if access_type != "mount" and access_type != "block":
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Invalid access_type")

        if access_type == "mount":
            fstype = volume_capability.mount.fs_type
            if fstype not in ["xfs", "btrfs", "ext4", ""]:
                context.abort(
                    grpc.StatusCode.INVALID_ARGUMENT,
                    "Unsupported filesystem type: {fstype}",
                )

        if volume_capability.access_mode.mode not in [
            csi_pb2.VolumeCapability.AccessMode.Mode.SINGLE_NODE_WRITER
        ]:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "Unsupported access mode: {csi_pb2.VolumeCapability.AccessMode.Mode.Name(volume_capability.access_mode.mode)}",
            )

        capabilities = []
        for capability in request.volume_capabilities:
            supported_capability = get_capability(capability)
            capabilities.append(supported_capability)

        confirmed = csi_pb2.ValidateVolumeCapabilitiesResponse.Confirmed(
            volume_context=request.volume_context,
            volume_capabilities=capabilities,
            parameters=request.parameters,
        )

        response = csi_pb2.ValidateVolumeCapabilitiesResponse(confirmed=confirmed)

        return response

    def ListVolumes(self, request, context):
        logger.info("ListVolumes()")
        # blivet_handle.reset()      # detect system storage configuration
        # print(str(blivet_handle.devicetree))

        # # TODO: update to just add the volumes?
        # device_json = devicetree_tojson(blivet_handle.devicetree)

        print_volume_list()
        next_token = None
        if request.starting_token:
            try:
                int(request.starting_token)
            except ValueError:
                context.abort(
                    grpc.StatusCode.ABORTED,
                    "request.starting_token must be an integer: {starting_token}",
                )

        if request.starting_token and not request.max_entries:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "request.starting_token defined with no request.max_entries: {starting_token}",
            )

        if not request.max_entries:
            csi_list = volume_list
        elif request.starting_token:
            csi_list = volume_list[
                request.starting_token : request.starting_token + request.max_entries
            ]
            next_token = request.starting_token + request.max_entries + 1
        else:
            csi_list = volume_list[: request.max_entries]

        return_list = list()

        for volume_map in csi_list:
            volume = csi_pb2.Volume(
                volume_id=volume_map.csi_volume.volume_id,
                capacity_bytes=volume_map.csi_volume.capacity_bytes,
            )
            return_list.append(csi_pb2.ListVolumesResponse.Entry(volume=volume))

        return csi_pb2.ListVolumesResponse(entries=return_list, next_token=next_token)

    def GetCapacity(self, request, context):
        logger.info("GetCapacity()")
        for capability in request.volume_capabilities:
            supported_capability = get_capability(capability)
            print(supported_capability)

        for key, value in request.parameters:
            print(key, value)

        device = dbus_handle.devicetree.get_device_by_name(VOLUME_GROUP_NAME)

        return csi_pb2.GetCapacityResponse(
            available_capacity=int(volume_group.free_space.convert_to(B))
        )

    def ControllerGetCapabilities(self, request, context):
        logger.info("ControllerGetCapabilities()")
        create_delete_volume = ControllerServiceCapability(
            rpc=ControllerServiceCapability.RPC(
                type=ControllerServiceCapability.RPC.CREATE_DELETE_VOLUME
            )
        )

        publish_unpublish_volume = ControllerServiceCapability(
            rpc=ControllerServiceCapability.RPC(
                type=ControllerServiceCapability.RPC.PUBLISH_UNPUBLISH_VOLUME
            )
        )

        list_volumes = ControllerServiceCapability(
            rpc=ControllerServiceCapability.RPC(
                type=ControllerServiceCapability.RPC.LIST_VOLUMES
            )
        )

        get_capacity = ControllerServiceCapability(
            rpc=ControllerServiceCapability.RPC(
                type=ControllerServiceCapability.RPC.GET_CAPACITY
            )
        )

        create_delete_snapshots = ControllerServiceCapability(
            rpc=ControllerServiceCapability.RPC(
                type=ControllerServiceCapability.RPC.CREATE_DELETE_SNAPSHOT
            )
        )

        list_snapshots = ControllerServiceCapability(
            rpc=ControllerServiceCapability.RPC(
                type=ControllerServiceCapability.RPC.LIST_SNAPSHOTS
            )
        )

        clone_volume = ControllerServiceCapability(
            rpc=ControllerServiceCapability.RPC(
                type=ControllerServiceCapability.RPC.CLONE_VOLUME
            )
        )

        publish_readonly = ControllerServiceCapability(
            rpc=ControllerServiceCapability.RPC(
                type=ControllerServiceCapability.RPC.PUBLISH_READONLY
            )
        )

        list_volumes_published_nodes = ControllerServiceCapability(
            rpc=ControllerServiceCapability.RPC(
                type=ControllerServiceCapability.RPC.LIST_VOLUMES_PUBLISHED_NODES
            )
        )

        volume_condition = ControllerServiceCapability(
            rpc=ControllerServiceCapability.RPC(
                type=ControllerServiceCapability.RPC.VOLUME_CONDITION
            )
        )

        get_volume = ControllerServiceCapability(
            rpc=ControllerServiceCapability.RPC(
                type=ControllerServiceCapability.RPC.GET_VOLUME
            )
        )

        expand_volume = ControllerServiceCapability(
            rpc=ControllerServiceCapability.RPC(
                type=ControllerServiceCapability.RPC.EXPAND_VOLUME
            )
        )

        # TODO: add capabilties as support is implemented

        capabilities = [
            create_delete_volume,
            publish_unpublish_volume,
            list_volumes,
            get_capacity,
            create_delete_snapshots,
            list_snapshots,
            clone_volume,
            publish_readonly,
            expand_volume,
            list_volumes_published_nodes,
            volume_condition,
            get_volume,
        ]

        return csi_pb2.ControllerGetCapabilitiesResponse(capabilities=capabilities)

    def CreateSnapshot(self, request, context):
        logger.info("CreateSnapshot()")
        if request.volume_id == None:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Must include volume_id")

        volume_map = get_volume(request.volume_id)

        if volume_map == None:
            context.abort(
                grpc.StatusCode.NOT_FOUND, "request.target_path does not exits"
            )

        context.abort(
            grpc.StatusCode.UNIMPLEMENTED,
            "CreateSnapshot not implemented",
        )
        return csi_pb2.CreateSnapshotResponse()

    def DeleteSnapshot(self, request, context):
        logger.info("DeleteSnapshot()")
        if request.volume_id == None:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Must include volume_id")

        context.abort(
            grpc.StatusCode.UNIMPLEMENTED,
            "DeleteSnapshot not implemented",
        )
        return csi_pb2.DeleteSnapshotResponse()

    def ListSnapshots(self, request, context):
        logger.info("ListSnapshots()")
        if request.volume_id == None:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Must include volume_id")

        volume_map = get_volume(request.volume_id)

        if volume_map == None:
            context.abort(
                grpc.StatusCode.NOT_FOUND, "request.target_path does not exits"
            )

        context.abort(
            grpc.StatusCode.UNIMPLEMENTED,
            "ListSnapshots not implemented",
        )
        return csi_pb2.CreateSnapshotResponse()

    def ControllerExpandVolume(self, request, context):
        logger.info("ControllerExpandVolume()")
        if request.volume_id == None or request.volume_id == "":
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Must include volume_id")

        volume_map = get_volume(request.volume_id)

        if volume_map == None:
            context.abort(grpc.StatusCode.NOT_FOUND, "request.volume_id does not exits")

        return csi_pb2.ControllerExpandVolumeResponse()

    def ControllerGetVolume(self, request, context):
        logger.info("ControllerGetVolume()")
        if request.volume_id == None or request.volume_id == "":
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Must include volume_id")

            volume_map = get_volume(request.volume_id)

            if volume_map == None:
                context.abort(
                    grpc.StatusCode.NOT_FOUND, "request.volume_id does not exits"
                )
            return csi_pb2.ControllerGetVolumeResponse()

    # def ListDevices(self, request, context):
    #     blivet_handle.reset()      # detect system storage configuration
    #     print(str(blivet_handle.devicetree))

    #     device_json = devicetree_tojson(blivet_handle.devicetree)
    #     return csi_pb2.StorageListReply(message="ListDevices, completed", device_json=device_json, return_code=0)
