#!/bin/bash

cd /backend/cont
cp text.ref /SuperCompiler/my-app/MSCPAver1
cd /SuperCompiler/my-app/MSCPAver1
./mscp-a text.ref
cp rsd_text.ref /backend/cont
cd /SuperCompiler/my-app/MSCPAver1/mscplog
cp trace_scp /backend/cont
cp trace_scp /SuperCompiler/my-app
cd /SuperCompiler/my-app
# dos2unix trace_scp
./decode_graph trace_scp

cp log.scpgraph /backend/cont


