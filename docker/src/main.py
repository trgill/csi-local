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

import dbus

OBJECT_MANAGER = "org.freedesktop.DBus.ObjectManager"
BUS = dbus.SystemBus("tcp:host=localhost,port=55556,family=ipv4")
BUS_NAME = "org.storage.stratis3"
TOP_OBJECT = "/org/storage/stratis3"
REVISION_NUMBER = 5
REVISION = f"r{REVISION_NUMBER}"
TIMEOUT = 10 * 1000


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


if __name__ == "__main__":
    objects = get_managed_objects()
    print(objects)
