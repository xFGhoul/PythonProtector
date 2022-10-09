#!/bin/bash

echo -------------------------------------

echo [*] Starting Format Process


echo -------------------------------------

cd ..

black .

echo -------------------------------------

autopep8 --in-place --aggressive --aggressive --recursive .


echo -------------------------------------

echo [*] Formatted All Files.

exit