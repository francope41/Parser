#!/bin/sh
if [ $# -eq 0 ]
  then
    echo "Path to file required to run (EXAMPLE: \"./exec.sh ../samples/badbool.frag\")"
else
    python ../Lexical/Lexical_Analyzer.py $1

    python ../main.py arr
fi