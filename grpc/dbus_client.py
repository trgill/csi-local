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

import dbus
import os
from traceback import print_exc

BUS_NAME = os.getenv('LVM_DBUS_NAME', 'com.redhat.lvmdbus1')
BASE_INTERFACE = 'com.redhat.lvmdbus1'
MANAGER_INT = BASE_INTERFACE + '.Manager'
MANAGER_OBJ = '/' + BASE_INTERFACE.replace('.', '/') + '/Manager'


class DbusClient:
    def __init__(self):
        try:
            self.bus = dbus.SystemBus()
            self.bus.list_names()

        except dbus.DBusException:
            print_exc()
            exit(1)

    def get_objects(self):
        try:
            object_manager_object = self.bus.get_object(
                BUS_NAME, "/com/redhat/lvmdbus1", introspect=False)

            manager_interface = dbus.Interface(
                object_manager_object, "org.freedesktop.DBus.ObjectManager")

            objects = manager_interface.GetManagedObjects()

            for object_path, v in objects.items():
                print(object_path)

            for interface in v.keys():
                print(interface)
        except dbus.DBusException:
            print_exc()
