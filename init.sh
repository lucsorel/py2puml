#! /bin/sh

depsinstall='install --no-dev'

while getopts d OPTION "$@"; do
    # echo "option ${OPTION}"
    case $OPTION in
        # also installs development dependencies
        d)
            depsinstall='install'
            ;;
        \?)
            echo "Invalid option: -$OPTION" >&2
            ;;
    esac
done

poetry config virtualenvs.create true --local
poetry config virtualenvs.in-project true --local
echo "$(date '+%Y-%m-%d_%H:%M:%S') $(poetry --version) will be used to install dependencies"

# installs the project dependencies
echo "$(date '+%Y-%m-%d_%H:%M:%S') poetry ${depsinstall}"
poetry ${depsinstall}