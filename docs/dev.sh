#!/bin/sh

bundle exec jekyll serve --livereload --drafts --future --port 5000 --livereload_port 35729 "$@"