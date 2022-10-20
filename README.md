This script compresses .log files located in the directory /var/logs periodically every 30 days
using the gzip module. (.gz files created, original files deleted)

Prerequisites
Python 3

Used modules and libraries
os
gzip
shutil
date
unittest

How to run the script
Create cron job 0 2 * * * python3.10 /path/to/script/main.py to run job daily at 2 a.m
(or any other time, but periodically one time per day).

Example of the script result
File example.log will be changed to 20221020_example.log.gz (20221020 means today date)


Items to discuss and/or improve:
Should we create a folder for .gz files, or store in the log directory (as is)?

It is not possible to configure cron to run every 30 days. Can we run job every month, not every 30 days?

Which type of files will be located in /val/log directory? Which type of files should we compress? 
Currently the only files with .log extensions are compressing.