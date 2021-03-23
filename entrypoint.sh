#!/bin/bash
set -ex

if [ -z "${GITHUB_ACTIONS}" ]; then
    exec okv ${@}
else
    strict_mode='--no-strict'
    if [ "${INPUT_STRICT}" = "true" ]; then strict_mode=''; fi
    INPUT_CPU_NUM="$(env | sed -n 's/^INPUT_CPU-NUM=\(.*\)/\1/p')"
    schema_flag="--ok=${INPUT_OK}"
    if [ ! -z "${INPUT_SCHEMA}" ]; then
        schema_flag="--schema=${INPUT_SCHEMA}"
    fi
    output=$(okv ${schema_flag} --cpu-num=${INPUT_CPU_NUM} --parser=${INPUT_PARSER} ${strict_mode} -path=${INPUT_PATH})
    result=$?
    echo "::set-output name=results::$(echo $output)"
    if [ "${result}" != "0" ]; then exit 1; fi
fi