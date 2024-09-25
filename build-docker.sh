#!/usr/bin/env bash

# Force docker to use linux/amd64
export DOCKER_DEFAULT_PLATFORM=linux/amd64

# Name of the container registry or docker hub namespace
cr="stephenturner"

## sed to get v number and pkg name
pkg=$(awk '/^name/{print $3}' pyproject.toml | sed 's/["]//g')
ver=$(awk '/^version/{print $3}' pyproject.toml | sed 's/["]//g')

## build the image and tag with version *and* latest, and tag with container registry also
cmd="docker build $@ -t ${pkg}:latest -t ${pkg}:${ver} -t ${cr}/${pkg}:latest -t ${cr}/${pkg}:${ver} ."

# Echo the build command, build the image
echo $cmd
eval $cmd

# Echo the push command to the terminal
echo
echo "Build command:"
echo $cmd
echo
echo "Push command copied to clipboard:"
echo "docker push --all-tags ${cr}/${pkg}" | tee >(pbcopy)
echo
