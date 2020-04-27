#!/usr/bin/env bash

readonly sourceFile="./venv/bin/activate"

source ${sourceFile} # venv is now active.

python cds/utils/cron.py
