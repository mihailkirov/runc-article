FROM alpine:latest
MAINTAINER "crypt0n1t3"

RUN apk update && \
	apk add runc && \
	apk add bash &&   \
	apk add python3 &&  \
	apk add iproute2 &&   \
	mkdir h00ks

COPY . /h00ks/
ENV CDIR="/h00ks" SCRIPT_DIR="/h00ks/scripts-hooks" ADDCNF="/h00ks/config-add.json" 
WORKDIR "/h00ks"
# final setup
RUN chmod 755 httph.py; \
	chmod 755 transform.py; \
	rm results-scripts/*.txt; \
	rm bundle/config.json 2>/dev/null 
CMD transform.py