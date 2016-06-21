#!/usr/bin/env bash
set -e

deployFolder="_deploy"

cd ..

rm -rf $deployFolder &&

bundle exec jekyll build &&
bundle exec htmlproofer $deployFolder --disable-external