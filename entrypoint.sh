#!/bin/bash
set -ex

if [ -z "${GITHUB_ACTIONS}" ]; then
    exec okv ${@}
else
    strict_mode='--no-strict'
    if [ "${INPUT_STRICT}" = "true" ]; then strict_mode=''; fi
    INPUT_CPU_NUM="$(env | sed -n 's/^INPUT_CPU-NUM=\(.*\)/\1/p')"
    output=$(okv --schema=${INPUT_SCHEMA}  --cpu-num=${INPUT_CPU_NUM} --parser=${INPUT_PARSER} ${strict_mode} -p=${INPUT_PATH})
    echo "::set-output name=results::$(echo $output)"
fi