#!/bin/bash
# string upper tell to open with bash (not comment)

# Pipline to choose scripts

bash ./megrge \
    ./filter \
    ./uniques \
    ./otus \
    ./otutable

less -S otutable
