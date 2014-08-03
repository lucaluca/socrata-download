#!/bin/sh
set -e

if test -z "$SOCRATA_URL"; then
  echo You need to set the SOCRATA_URL.
  exit 1
fi
DIR="data/$SOCRATA_URL/views"

# Sleep if we aren't using a proxy
if test -z "$http_proxy"; then
  sleep_interval=1s
else
  sleep_interval=0s
fi

#tmp=$(mktemp)  # had to add this
tmp=$SOCRATA_URL  # had to add this
mkdir -p "$DIR"
echo $tmp
for viewid in $(cat "data/$SOCRATA_URL/viewids"); do
  url="http://$SOCRATA_URL/views/${viewid}.json"

  if test -e "$DIR/${viewid}"; then
    # Skip it if we have it.
    continue
  fi

  wget --no-check-certificate -O "$DIR/${viewid}" "$url" 2> $tmp || sleep 0s

  if grep 'ERROR 404: Not Found.' $tmp; then
    # Skip on 404, after sleeping
    sleep $sleep_interval

  elif grep 'ERROR 429: 429' $tmp; then
    # Die on API limit, with a note to try later.
    echo "You've hit an API limit. Try again later. Bye."
    exit 2

  else
    # Sleep if it worked
    echo Downloaded "$url"
    sleep $sleep_interval
  fi 
done
echo Done downloading "$SOCRATA_URL"
