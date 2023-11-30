#!/bin/bash

tar -xzf python310.tar.gz

# tar -xzf other packages

export PATH=$PWD/Python/bin:$PATH
export Py_HOME=$PWD/Python
export Py_LIBS=$PWD/packages

# run your script
python3 test.py $1