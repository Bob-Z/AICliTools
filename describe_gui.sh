#!/bin/bash

script_path=$(dirname $(realpath $0))

"$script_path"/auto_deps.sh describe_gui.py "$@"


