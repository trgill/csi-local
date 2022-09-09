FROM python:3.10.5

ARG RELEASE=master
ARG BUILD_DATE

LABEL maintainers="Todd Gill <tgill@redhat.com>" \
    openstack_release=${RELEASE} \
    version=${VERSION} \
    description="Springfield CSI Plugin" \
    org.label-schema.schema-version="1.0" \
    org.label-schema.name="springfield-csi" \
    org.label-schema.description="Springfield CSI Plugin" \
    org.label-schema.url="https://github.com/trgill/csi-local" \
    org.label-schema.build-date=${BUILD_DATE} \
    org.opencontainers.image.source=https://github.com/trgill/springfield-csi-driver

RUN mkdir /csi-springfield-driver
WORKDIR /csi-springfield-driver
ADD ../../grpc ./
RUN pip install -r requirements.txt

# grpc server listtens on 50025, http server for debugging listens on 50025
EXPOSE 5000 50024 50025 

CMD ["python", "/csi-springfield-driver/server.py"]
