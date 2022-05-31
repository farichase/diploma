#!/bin/bash

cp /home/farida/SuperCompiler/my-app/cont/log.scpgraph /home/farida/SuperCompiler/my-app/backend/routes/graphs/
python3 -u /home/farida/SuperCompiler/my-app/backend/routes/graphs/parser.py
cp img.png /home/farida/SuperCompiler/my-app//src/Components/OutputAreaCode
cp img.png /home/farida/SuperCompiler/my-app//src/Components/Buttons/Button