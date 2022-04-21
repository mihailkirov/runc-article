FROM alpine:latest
MAINTAINER "crypt0n1t3"

ARG ROOTFSTAR="/h00ks/alpine-rootfs-docker-export-x86_64.tar"

RUN apk update && \
	apk add runc && \
	apk add bash &&   \
	apk add python3 &&  \
	apk add iproute2

COPY . /h00ks/
ENV CDIR="/h00ks" SCRIPT_DIR="/h00ks/scripts-hooks" ADDCNF="/h00ks/config-add.json" \
	BUNDLEDIR="/h00ks/bundle"  GOPT="" CNAME="c"

WORKDIR "/h00ks"
RUN mkdir -p bundle/rootfs && \
	tar xf ${ROOTFSTAR} -C bundle/rootfs && \
	chmod 755 transform.py && \
	mkdir -p results-scripts; \
	rm bundle/config.json 2>/dev/null
CMD ["./transform.py"]