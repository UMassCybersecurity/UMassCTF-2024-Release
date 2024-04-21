#!/bin/bash

set -Eeuo pipefail

TIMEOUT=20
PERIOD=30

export TERM=linux
export TERMINFO=/etc/terminfo

while true; do
  echo -n "[$(date)] "
  # Use curl to fetch the web page and grep to search for "UMASS"
  if timeout "${TIMEOUT}" curl localhost:1337 -A "Bikini Bottom" -H "Date: Wed, 14 Jul 2024 07:28:00 GMT" -H "Accept-Language: fr-FR" -H "Cookie: flavor=chocolate_chip; Login=eyJsb2dnZWRpbiI6IHRydWV9" | grep -q "UMASS"; then
    echo 'ok' > /tmp/healthz
  else
    # If UMASS is not found in the content, write 'err' to /tmp/healthz
    echo 'err' > /tmp/healthz
  fi
  sleep "${PERIOD}"
done
