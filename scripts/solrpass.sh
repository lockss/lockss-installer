#!/bin/bash

# Simulate xxd -r -p
function xxdrp () {
  local input
  read input
  I=0
  while [ $I -lt 64 -a $I -lt ${#input} ];
  do
    echo -en "\x"${input:$I:2}
    let "I += 2"
  done
}

# Simulate base64 -w 0
function base64w0() {
  base64 | tr -d '\n'
}

PW="${1:?Usage: $0 PASSWORD}"
#SALT="$(pwgen 48 -1)"
SALT=$(dd if=/dev/urandom bs=1 count=48 status=none | base64 | cut -c 1-48)
#echo "$(echo -n "${SALT}${PW}" | sha256sum -b | xxd -r -p | sha256sum -b | xxd -r -p | base64 -w 1024) $(echo -n "$SALT" | base64 -w 1024)"
echo "$(echo -n "${SALT}${PW}" | sha256sum -b | xxdrp | sha256sum -b | xxdrp | base64w0) $(echo -n "$SALT" | base64w0)"
