#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR

pylint --rcfile=pylintrc ./crt | tee ./pylint.output || true
