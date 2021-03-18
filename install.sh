#!/bin/bash

# Install python dependencies
pip install psycopg2-binary
pip install pandas

# Setting up database login file
user=$(whoami)
chmod +x db_datagenerator.py
./db_datagenerator.py $user

# Creating required directories if not exists.
mkdir -p ~/.local/bin

# Copying over files.
cp note ~/.local/bin
cp -r notehandler ~/.local/bin

# Installing postgresql and activating database.
sudo pacman -S postgresql --needed --noconfirm
sudo -iu postgres initdb -D /var/lib/postgres/data

# Enabling postgresql on boot
sudo systemctl enable --now postgresql.service

# Creating postgres user and database.
sudo -iu postgres psql postgres -c "CREATE ROLE $user login;"
sudo -iu postgres psql postgres -c "CREATE DATABASE mynotes OWNER $user;"

# Restarting postgresql.
sudo systemctl restart postgresql.service
