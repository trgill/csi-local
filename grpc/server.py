# Copyright (C) 2022  Red Hat, Inc.
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

import concurrent.futures as futures
import csi_pb2_grpc
import grpc
import logging
import argparse
import json
import socket
from pathlib import Path


from identity import SpringfieldIdentityService
from controller import SpringfieldControllerService
from controller import disks_to_use

# from controller import dbus_handle

from controller import VOLUME_GROUP_NAME

from node import SpringfieldNodeService

STORAGE_DEVS_FILE = "storage_devs.json"


def run_server(port, addr, nodeid):

    logging.info("Starting grpc server:")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    csi_pb2_grpc.add_ControllerServicer_to_server(
        SpringfieldControllerService(nodeid=nodeid), server
    )
    csi_pb2_grpc.add_IdentityServicer_to_server(SpringfieldIdentityService(), server)
    csi_pb2_grpc.add_NodeServicer_to_server(
        SpringfieldNodeService(nodeid=nodeid), server
    )

    logging.info("server.add_insecure_port()")
    server.add_insecure_port(addr + str(port))
    server.start()
    server.wait_for_termination()


# Note: the disks need to be initialized and the volume group created before the
# grpc server is started.


def initilize_disks(init_disks):

    path = Path(STORAGE_DEVS_FILE)

    if not path.is_file():
        logging.warning("%s file not found in %s", STORAGE_DEVS_FILE, Path.cwd())
        # look in the grpc subdirectory
        path = Path("grpc/" + STORAGE_DEVS_FILE)
        if not path.is_file():
            logging.error("%s file not found in %s", STORAGE_DEVS_FILE, Path.cwd())
            exit()

    try:
        with open(path) as json_file:
            storage_devs = json.load(json_file)["use_for_csi_storage"]
    except ValueError:
        logging.error("Failed to parse {}", STORAGE_DEVS_FILE)
        exit()

    pvs = list()

    for dev_path in storage_devs:
        disks_to_use.append(dev_path)

    if len(disks_to_use) == 0:
        logging.error("No useable disks")
        exit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--nodeid",
        dest="nodeid",
        type=str,
        help="unique node identifier",
        default=socket.getfqdn(),
    )
    parser.add_argument(
        "--addr", dest="addr", type=str, help="ip address to listen", default="[::]:"
    )
    parser.add_argument(
        "--port", dest="port", type=int, help="port to listen", default=50024
    )
    parser.add_argument(
        "--init_disks",
        dest="init_disks",
        type=bool,
        help="initialize storage",
        default=False,
    )

    args = parser.parse_args()

    port = args.port
    addr = args.addr
    nodeid = args.nodeid
    init_disks = args.init_disks

    logging.basicConfig()
    # initilize_disks(init_disks)
    run_server(port, addr, nodeid)
