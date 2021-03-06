#!/usr/bin/env bash



BTC_LIST=$HOME/btc/blockchair_bitcoin_addresses_latest_16_05_2020.tsv-sorted
BTC_DIR=$HOME/btc/BTC-CRACK-RESULT
BTC_RESULT=$BTC_DIR/BTC_FIND_ADDRESS
NOTIFY=./notify.sh

if [[ ! -d "$BTC_DIR" ]]; then
    mkdir -p "$BTC_DIR"
fi

# 0x2540BE400 - 10 000 000 000 
# 0x4A817C800 - 20 000 000 000
# 0x5D21DBA00 - 25 000 000 000

$NOTIFY &>/dev/null &

while :; do
    RAND=$(xxd -p -c 32 -l 32 /dev/urandom)
    ./bin/cuBitCrack -i $BTC_LIST \
                     -o $BTC_RESULT -d 0 \
                     -b 32 -t 64 -p 32 \
                     --keyspace $RAND:+5D21DBA00
done
