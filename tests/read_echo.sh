#!/usr/bin/env bash

echo "echo one"
echo "echo two"
echo "Say something:"
read WORD
echo "you said ${WORD}"
echo "Say something else:"
read WORD2
echo "you said ${WORD2}" 1>&2
#sleep 20
echo "echo done"