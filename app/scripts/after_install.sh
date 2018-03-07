#!/bin/bash

cd "$(dirname "$0")"
chmod u+x ssm_replacements.py

./ssm_replacements.py /var/www/html/config.php
