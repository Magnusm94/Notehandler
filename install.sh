#!/bin/bash

pip install psycopg2-binary
pip install pandas
mkdir -p ~/.local/bin
cp note ~/.local/bin
cp -r notehandler ~/.local/bin
