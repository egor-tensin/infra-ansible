#!/usr/bin/env bash

set -o errexit -o nounset -o pipefail
shopt -s inherit_errexit lastpipe

script_path="$( readlink --canonicalize-existing -- "${BASH_SOURCE[0]}" )"
readonly script_path
script_dir="$( dirname -- "$script_path" )"
readonly script_dir

_git() {
    git -C "$script_dir" "$@"
}

check_tag_release() {
    if ! command -v tag-release &>/dev/null; then
        echo "tag-release not found" >&2
        return 1
    fi
}

get_new_version() {
    if [ "$#" -ne 1 ]; then
        echo "${FUNCNAME[0]}: must provide the version upgrade tier" >&2
        return 1
    fi

    new_version="$( tag-release --print-only "$1" )"
}

modify_meta_file() {
    local path
    path="$script_dir/galaxy.yml"

    local ansible_version
    ansible_version="${new_version#v}"

    sed -i -e "s/version:.*/version: $ansible_version/" "$path"
}

commit_and_tag() {
    _git add galaxy.yml
    _git commit -m "$new_version"
    _git push
    tag-release -u "$@"
}

main() {
    check_tag_release
    get_new_version "$@"
    modify_meta_file 
    commit_and_tag "$@"
}

main "$@"
