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
#

import os
import dbus
import json
import argparse

OBJECT_MANAGER = "org.freedesktop.DBus.ObjectManager"
BUS = dbus.SystemBus()
BUS_NAME = "org.storage.stratis3"
TOP_OBJECT = "/org/storage/stratis3"
REVISION_NUMBER = 2
REVISION = f"r{REVISION_NUMBER}"
TIMEOUT = 10 * 1000

MNGR_IFACE = f"{BUS_NAME}.Manager.{REVISION}"
REPORT_IFACE = f"{BUS_NAME}.Report.{REVISION}"
POOL_IFACE = f"{BUS_NAME}.pool.{REVISION}"
FS_IFACE = f"{BUS_NAME}.filesystem.{REVISION}"
BLKDEV_IFACE = f"{BUS_NAME}.blockdev.{REVISION}"

CONTAINER_POOL = os.getenv("CONTAINER_POOL", "springfield-docker-test")
JSON_DEV_FILE = os.getenv("JSON_DEV_FILE", "ok_to_destroy.json")


def get_managed_objects():
    """
    Get managed objects for stratis
    :return: A dict,  Keys are object paths with dicts containing interface
                        names mapped to property dicts.
                        Property dicts map names to values.
    """
    object_manager = dbus.Interface(
        BUS.get_object(
            BUS_NAME, TOP_OBJECT),
        OBJECT_MANAGER,
    )
    return object_manager.GetManagedObjects(timeout=TIMEOUT)


def pool_object_path(pool_name):
    """
    Query the pools
    :return: the dbus object path for the pool
    :rtype: str
    """

    for obj_path, obj_data in get_managed_objects().items():
        if POOL_IFACE in obj_data and str(obj_data[POOL_IFACE]["Name"]) == pool_name:
            print(obj_data)
            return obj_path

    return None


def fs_create(pool_path, fs_name, *, fs_size=None):
    """
    Create a filesystem
    :param str pool_path: The object path of the pool in which the filesystem will be created
    :param str fs_name: The name of the filesystem to create
    :param str fs_size: The size of the filesystem to create
    :return: The return values of the CreateFilesystems call
    :rtype: The D-Bus types (ba(os)), q, and s
    """
    iface = dbus.Interface(
        BUS.get_object(BUS_NAME, pool_path),
        POOL_IFACE,
    )

    file_spec = (
        (fs_name, (False, "")) if fs_size is None else (fs_name, (True, fs_size))
    )

    return iface.CreateFilesystems([file_spec], timeout=TIMEOUT)


def get_empty_devs_list():
    list = []
    f = open(JSON_DEV_FILE)

    devices = json.load(f)

    for i in devices["use_for_stratis"]:
        print(i["device"])
        list.append(i["device"])

    f.close()

    return list


def pool_create(
    pool_name,
    devices,
    *,
    key_desc=None,
    clevis_info=None,
    redundancy=None


):
    """
    Create a pool
    :param str pool_name: The name of the pool to create
    :param str devices: A list of devices that can be used to create the pool
    :param key_desc: Key description
    :type key_desc: str or NoneType
    :param clevis_info: pin identifier and JSON clevis configuration
    :type clevis_info: str * str OR NoneType
    :return: The return values of the CreatePool call
    :rtype: The D-Bus types (b(oao)), q, and s
    """
    iface = dbus.Interface(
        BUS.get_object(
            BUS_NAME, TOP_OBJECT),
        MNGR_IFACE,
    )
    return iface.CreatePool(
        pool_name,
        (True, redundancy) if redundancy is not None else (False, 0),
        devices,
        (True, key_desc) if key_desc is not None else (False, ""),
        (True, clevis_info) if clevis_info is not None else (False, ("", "")),
        timeout=TIMEOUT,
    )


def fs_create(pool_path, fs_name, *, fs_size=None):
    """
        Create a filesystem
        :param str pool_path: The object path of the pool in which the filesystem will be created
        :param str fs_name: The name of the filesystem to create
        :param str fs_size: The size of the filesystem to create
        :return: The return values of the CreateFilesystems call
        :rtype: The D-Bus types (ba(os)), q, and s
        """
    iface = dbus.Interface(
        BUS.get_object(BUS_NAME, pool_path),
        POOL_IFACE,
    )

    file_spec = (
        (fs_name, (False, "")) if fs_size is None else (
            fs_name, (True, fs_size))
    )

    return iface.CreateFilesystems([file_spec], timeout=TIMEOUT)


def fs_list():
    """
    Query the file systems
    :return: A dict,  Key being the fs name, the value being the pool name
    :rtype: dict mapping str to str
    """
    objects = get_managed_objects().items()

    fs_objects = [
        obj_data[FS_IFACE]
        for _, obj_data in objects
        if FS_IFACE in obj_data

    ]

    pool_path_to_name = {
        obj: obj_data[POOL_IFACE]["Name"]
        for obj, obj_data in objects
        if POOL_IFACE in obj_data
    }

    return {
        fs_object["Name"]: pool_path_to_name[fs_object["Pool"]]
        for fs_object in fs_objects
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-d', '--devices', nargs='+', action='append',
                        dest="devices", help='required block devices for stratis pool', required=True)

    args = parser.parse_args()

    pool_path = pool_object_path(CONTAINER_POOL)

    if pool_path is None:
        pool_devs = args.devices[0]

        pool = pool_create(CONTAINER_POOL, pool_devs)
        pool_path = pool_object_path(CONTAINER_POOL)
        fs_create(pool_path, "fs1")
        fs_create(pool_path, "fs2")

    print(fs_list())

    print("container completed")
