FROM alpine:latest
MAINTAINER "crypt0n1t3"

RUN apk update && \
	apk add runc && \
	apk add bash &&   \
	apk add python3 &&  \
	apk add iproute2 &&   \
	mkdir h00ks

COPY . /h00ks/
ENV CDIR="/h00ks"
ENV SCRIPT_DIR="/h00ks/scripts-hooks"
ENV ADDCNF="/h00ks/config-add.json" 
WORKDIR "/h00ks"
CMD run.sh