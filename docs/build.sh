#!/bin/sh

 NODE_ENV=production ./node_modules/.bin/postcss ./assets/app.source.css -o ./assets/app.css
 bundle exec jekyll build
