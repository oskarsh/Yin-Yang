#!/bin/bash
set -euo pipefail
help() {
cat << EOF
Build and install as flatpak. Requires both "poetry" and "flatpak".

usage:
    flatpak-install [--user]
    flatpak-install --help | -h

options:
    --user      If present, --user will also be added to flatpak command calls
    --help -h   Show this help

See Also:
    - poetry: https://python-poetry.org/docs/#installation
    - flatpak: https://flathub.org/setup

EOF
exit "$1"
}

command -V poetry || help 1
command -V flatpak || help 1
for ARG in "$@"
do
    case "$ARG" in
    --user) USE_USER=1;;
    --help|-h) help 0;;
    esac
done

# follow the development setup
poetry build

flatpak remote-add --if-not-exists ${USE_USER:+--user} flathub https://dl.flathub.org/repo/flathub.flatpakrepo
flatpak install -y ${USE_USER:+--user} flathub org.flatpak.Builder

# see https://github.com/flatpak/flatpak-builder/issues/237 if you have issues with rofiles
flatpak run ${USE_USER:+--user} org.flatpak.Builder --install ${USE_USER:+--user} --force-clean --install-deps-from=flathub build sh.oskar.yin_yang.json
