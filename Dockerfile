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
ENTRYPOINT ["/bin/bash", "-c"]
CMD /h00ks/run.sh