#!/bin/bash
set -e

if [ ! -z "${DEBUG}" ]; then set -x; fi
if [ -z "${GITHUB_ACTIONS}" ]; then
    exec okv ${@}
else
    strict_mode='--no-strict'
    if [ "${INPUT_STRICT}" = "true" ]; then strict_mode=''; fi
    INPUT_CPU_NUM="$(env | sed -n 's/^INPUT_CPU-NUM=\(.*\)/\1/p')"
    INPUT_FILE_RESTRICTIONS="$(env | sed -n 's/^INPUT_FILE-RESTRICTIONS=\(.*\)/\1/p')"
    schema_flag="--ok=${INPUT_OK}"
    if [ ! -z "${INPUT_SCHEMA}" ]; then
        schema_flag="--schema=${INPUT_SCHEMA}"
    fi
    output=""
    result="0"
    set +e
    if [ -z "${INPUT_FILE_RESTRICTIONS}" ]; then
        output=$(okv ${schema_flag} --cpu-num=${INPUT_CPU_NUM} --parser=${INPUT_PARSER} ${strict_mode} -path=${INPUT_PATH})
        result=$?
        echo "${output}"
    else
        # INPUT_FILE_RESTRICTIONS is expected to be a space-separated array
        # of files
        file_arr=($INPUT_FILE_RESTRICTIONS)
        for file in ${file_arr[@]}; do
            # If an input path is also provided, it is expected to serve as an
            # enforced prefix for each of the file restrictions. In the case
            # of the pull request, this means that added and modified files
            # must exist within a particular directory or match a file
            if [[ ! -z "${INPUT_PATH}" ]] && [[ "${file}" != ${INPUT_PATH}* ]]; then
                continue
            fi
            tmp_output=$(okv ${schema_flag} --cpu-num=${INPUT_CPU_NUM} --parser=${INPUT_PARSER} ${strict_mode} -path=${file})
            tmp_result=$?
            # Loop over all files before throwing non-zero exit below
            if [ "${tmp_result}" == "0"  ]; then
                continue
            fi
            if [ "${result}" == "0"  ]; then
                result="$tmp_result"
            fi
            if [ -z "${output}" ]; then
                output="${tmp_output}"
                echo "${output}"
            else
                echo "----
${tmp_output}"
                output="${output}
                ----
${tmp_output}"
            fi
        done
    fi
    set -e
    echo "::set-output name=results::$(echo $output)"
    if [ "${result}" != "0" ]; then exit 1; fi
fi