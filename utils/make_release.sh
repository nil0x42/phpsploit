#!/usr/bin/env bash

# Run this script to create a new release of phpsploit

SCRIPTDIR="$(readlink -f `dirname $0`)"
cd "$(git rev-parse --show-toplevel)"

# colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BOLD='\033[1m'
NC='\033[0m' # No Color



########## ERROR HANDLING


# check arguments
if (( $# != 1 )); then
    >&2 echo -e "Usage: $0 <version>"
    >&2 echo -e "Example: ${GREEN}$0 3.0${NC}"
    exit 1
fi


# check current branch is master
cur_branch="$(git rev-parse --abbrev-ref HEAD)"
if [ "$cur_branch" != "master" ]; then
    >&2 echo -e "\n${RED}[-] Please checkout on master branch:${NC}"
    >&2 echo -e "    ${GREEN}git checkout master${NC}"
    exit 1
fi


# check existence of `github_changelog_generator` tool
# needed to generate CHANGELOG.md
gh_changelog_gen="github_changelog_generator"
if ! which "$gh_changelog_gen" >/dev/null; then
    >&2 echo -e "\n${RED}[-] Please install '$gh_changelog_gen':${NC}"
    >&2 echo -e "    ${GREEN}sudo gem install ${gh_changelog_gen}${NC}"
    exit 1
fi

# check existence of `remark` tool
# needed to generate CHANGELOG.md
remark="remark"
if ! which "$remark" >/dev/null; then
    >&2 echo -e "\n${RED}[-] Please install '$remark':${NC}"
    >&2 echo -e "    ${GREEN}sudo npm install -g remark-cli remark-preset-lint-recommended${NC}"
    exit 1
fi


# check existence of `txt2tags` tool
# needed to run ./man/update-man.sh
txt2tags="txt2tags"
if ! which "$txt2tags" >/dev/null; then
    >&2 echo -e "\n${RED}[-] Please install '$txt2tags':${NC}"
    >&2 echo -e "    ${GREEN}sudo apt install ${txt2tags}${NC}"
    exit 1
fi


# make sure that git work tree is clean
# source: https://stackoverflow.com/questions/30063411/git-bash-script-check-working-tree
require_clean_work_tree () {
    git rev-parse --verify HEAD >/dev/null || exit 1
    git update-index -q --ignore-submodules --refresh
    err=0
    if ! git diff-files --quiet --ignore-submodules
    then
        echo >&2 "Cannot $1: You have unstaged changes."
        err=1
    fi
    if ! git diff-index --cached --quiet --ignore-submodules HEAD --
    then
        if [ $err = 0 ]
        then
            echo >&2 "Cannot $1: Your index contains uncommitted changes."
        else
            echo >&2 "Additionally, your index contains uncommitted changes."
        fi
        err=1
    fi
    if [ $err = 1 ]
    then
        test -n "$2" && echo >&2 "$2"
        exit 1
    fi
}
require_clean_work_tree
if [ -n "$(git status --porcelain)" ]; then
    >&2 echo -e "\n${RED}[-] Please commit or stash untracked files${NC}"
    >&2 echo -e "    ${GREEN}git status${NC}"
    exit 1
fi


# check nothing to pull
local_head="$(git rev-parse HEAD)"
remote_head="$(git ls-remote origin master | cut -f1)"
if [ "$local_head" != "$remote_head" ]; then
    >&2 echo -e "\n${RED}[-] Local branch != remote, please pull or push:${NC}"
    >&2 echo -e "    ${GREEN}git pull; git push${NC}"
    exit 1
fi



########## MAKE RELEASE

VER=$1
TAG="v${VER}"
MSG="${VER} release"

# set verbose/err
set -ve

# replace VERSION string in ./phpsploit
sed -i '/^VERSION = /c\VERSION = "'${VER}'"' ./phpsploit
git add ./phpsploit


# generate CHANGELOG.md
github_changelog_generator --future-release ${TAG}
remark CHANGELOG.md -o
git add ./CHANGELOG.md

# update man page
./man/update-man.sh
git add ./man/

# create commit
git commit -m "$MSG"

# add release tag to created commit
git tag -a $TAG -m "$MSG"

# unset verbose/err
set +ve

echo -e "${BOLD}[+] Release commit created successfully${NC}"
echo -e ""
echo -e "  1. Check the release commit:"
echo -e "      ${GREEN}git diff HEAD^${NC}"
echo -e ""
echo -e "  2. Push the commit and it's tag"
echo -e "      ${GREEN}git push --follow-tags${NC}"
