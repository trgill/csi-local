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

FROM python:3.9 

ENV DEBIAN_FRONTEND=noninteractive

USER root

RUN apt-get update && \
    apt-get -y install --no-install-recommends \
        build-essential dbus-daemon python3-dbus libpython3-dev libdbus-1-dev libdbus-glib-1-dev libgirepository1.0-dev 

RUN pip install dbus-python

LABEL maintainers="Todd Gill <tgill@redhat.com>" \
    version="0.1.1" \
    release="1" \
    description="Springfield Docker Plugin" \
    summary="Springfield Docker driver" \
    org.label-schema.schema-version="1.0" \
    org.label-schema.name="springfield-csi" \
    org.label-schema.description="Springfield Docker Plugin" \
    org.label-schema.url="https://github.com/trgill/csi-local" \
    org.label-schema.build-date=${BUILD_DATE} \
    org.opencontainers.image.source="https://github.com/trgill/csi-local" \
    org.opencontainers.image.description="Springfield prototype Docker driver"

RUN mkdir /csi-springfield-driver

WORKDIR /csi-springfield-driver

ADD ./src .

RUN chmod 755 /csi-springfield-driver/entrypoint.sh

ENV DBUS_SYSTEM_BUS_ADDRESS=unix:path=/var/run/dbus/system_bus_socket
ENV PATH="/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

ENTRYPOINT ["/csi-springfield-driver/entrypoint.sh"]
