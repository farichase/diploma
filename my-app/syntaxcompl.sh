#!/bin/bash

cd /backend/cont
cp SuperCompilerInput.txt /SuperCompiler/my-app
cd /SuperCompiler/my-app
cp SuperCompilerInput.txt /syntaxCompletions
cd /syntaxCompletions
python3 -u main.py
cp SuperCompilerOut.txt /backend/cont


