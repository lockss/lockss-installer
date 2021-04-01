#!/bin/bash
PW="${1:?Usage: $0 PASSWORD}"
#SALT="$(pwgen 48 -1)"
SALT=$(dd if=/dev/urandom bs=1 count=48 status=none | base64 | cut -c 1-48)
echo "$(echo -n "${SALT}${PW}" | sha256sum -b | xxd -r -p | sha256sum -b | xxd -r -p | base64 -w 1024) $(echo -n "$SALT" | base64 -w 1024)"