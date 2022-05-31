#!/bin/bash



cd /backend/cont
rm -R lasttrace
mkdir lasttrace
cp text.ref /SuperCompiler/my-app/mscp-trace
cd /SuperCompiler/my-app/mscp-trace
dos2unix text.ref
chmod +x trace_echo.sh
./mscp-a text.ref
cd /SuperCompiler/my-app/mscp-trace/mscplog
cp log.scpgraph /backend/cont
cd /SuperCompiler/my-app/mscp-trace


cp -R lasttrace /backend/cont
rm -R lasttrace
mkdir lasttrace