#!/bin/bash

script_path=$(dirname $(realpath $0))
venv_dirname="venv"
venv_path="$script_path/$venv_dirname"
install_ok_file="$script_path/install.ok"

working_directory=$(pwd)

cd "$script_path"

need_install=false

if [ ! -f "$install_ok_file" ] | [ ! -d "$venv_path" ]; then
    echo "Need a fresh dependencies installation"
    need_install=true
else
    install_ok_time=$(stat -c %Y "$install_ok_file")
    requirements_time=$(stat -c %Y "requirements.txt")

    if [ "$install_ok_time" -lt "$requirements_time" ]; then
        echo "Need to update dependencies"
        need_install=true
    fi
fi

if [ "$need_install" = true ]; then
    if [ -d "$venv_path" ]; then
        rm -rf "$venv_path"
	rm "$install_ok_file"
    fi

    python3 -m venv "$venv_dirname"

    source "$venv_path/bin/activate" && pip install -r requirements.txt

    touch "$install_ok_file"
fi

python_script=$1
shift # remove first arguments form $@

cd "$working_directory"

source "$venv_path/bin/activate" && python3 "$script_path"/"$python_script" $@


