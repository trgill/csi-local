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

FROM python:3.10.6

USER root

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get -y install --no-install-recommends \
    build-essential \
    glib-2.0 \
    bash \
    file \
    python3-dev \
    python-dbus-dev \
    python3.10 \
    python3-pip \
    libdbus-1-3 \
    libdbus-1-dev \
    dbus


ARG RELEASE=master
ARG BUILD_DATE

RUN apt-get install -y dbus

LABEL maintainers="Todd Gill <tgill@redhat.com>" \
    version="0.0.1" \
    description="Springfield CSI Plugin" \
    org.label-schema.schema-version="1.0" \
    org.label-schema.name="springfield-csi" \
    org.label-schema.description="Springfield CSI Plugin" \
    org.label-schema.url="https://github.com/trgill/csi-local" \
    org.label-schema.build-date=${BUILD_DATE} \
    org.opencontainers.image.source="https://github.com/trgill/csi-local"

RUN mkdir /csi-springfield-driver
WORKDIR /csi-springfield-driver
ADD ./grpc .
RUN chmod 755 /csi-springfield-driver/entrypoint.sh

RUN pip3 install --upgrade pip
RUN pip3 --version
#RUN pip3 install --upgrade setuptools
#RUN pip3 install --no-cache-dir -r requirements.txt

RUN python3 -m pip install grpcio
RUN python3 -m pip install grpcio-tools
RUN python3 -m pip install protobuf
RUN python3 -m pip install dbus-python


COPY ./grpc/com.redhat.lvmdbus1.conf /etc/dbus-1/system.d/

RUN mkdir /var/run/dbus/

ENV DBUS_SYSTEM_BUS_ADDRESS=unix:path=/var/run/dbus/system_bus_socket
ENV PATH="/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

# grpc server listtens on 50025, http server for debugging listens on 50025
EXPOSE 5000 50024 50025 

ENTRYPOINT ["/csi-springfield-driver/entrypoint.sh"]
