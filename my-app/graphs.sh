#!/bin/bash

cd /backend/cont
cp log.scpgraph /SuperCompiler/my-app/graphs
cd /SuperCompiler/my-app/graphs
python3 -u parser.py
cp img.png /backend/cont
