#!/bin/bash

log_dir=".logs-$(date +"%Y%m%d%H%M%S")"
mkdir -p "$log_dir"

log_file="$log_dir/validator-4.log"

snarkos start --nodisplay --dev 4 --dev-num-validators 4 --validator --logfile ${log_file} --validators "127.0.0.1:5000" --rest "127.0.0.1:3034" --nocdn
 
