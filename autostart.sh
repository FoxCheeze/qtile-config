#!/bin/bash

# Disable auto sleep and hibernate
sudo systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target

# Enable Night Mode (blue light filter)
redshift -Po -t 3600K:3600K

