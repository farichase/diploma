#!/bin/bash

cp ./mscplog/curr_trace ./lasttrace/last_trace.`eval date +%s`
./mscplog/decode_graph ./mscplog/curr_trace
cp ./mscplog/log.scpgraph ./lasttrace/log_trace.`eval date +%s`
echo T > key.txt