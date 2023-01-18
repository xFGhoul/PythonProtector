#!/bin/bash

echo -------------------------------------

echo [*] Starting Format Process


echo -------------------------------------

cd ..

black -v .

echo -------------------------------------

autopep8 --in-place --aggressive --aggressive --recursive -v .


echo -------------------------------------

autoflake --in-place --remove-unused-variables .

echo -------------------------------------

echo [*] Formatted All Files.

exit