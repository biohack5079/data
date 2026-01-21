#!/bin/sh

# Make PyNEST available by prepending its path to PYTHONPATH in a safe way.
export PYTHONPATH="/home/s24156/data/.venv/lib/python3.13/site-packages${PYTHONPATH:+:$PYTHONPATH}"

# Make NEST executables available by prepending their path to PATH.
export PATH="/home/s24156/data/.venv/bin:${PATH}"
