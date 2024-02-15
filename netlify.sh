#!/bin/bash

set -e

git remote add origin https://github.com/org-id/register.git || true

git fetch

pip install datatig

export PYTHONPATH=$(pwd)

echo "Building site ..."
python -m datatig.cli build . --staticsiteoutput out

if [ "$HEAD" != "main" ]
then
  echo "Building versioned site ..."
  python -m datatig.cli versionedbuild --staticsiteoutput out/versioned --staticsiteurl /versioned --refs origin/main,origin/$HEAD  --defaultref origin/main . || true
fi
