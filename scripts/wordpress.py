#!/usr/bin/env python3

#
# (C) 2023 - ntop
#

import subprocess
import re
import sys
import os

if(len(sys.argv) != 2):
    print("Usage: wordpress.py <filename>")
    exit(0)


filename = sys.argv[1]

f = subprocess.Popen(['tail','-n', '0', '-F',filename], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
#f = subprocess.Popen(['cat',filename], stdout=subprocess.PIPE,stderr=subprocess.PIPE)

# Note that (?=...).+ stand for an "and" of conditions
# Matches sql injections that are like that: a=b AND| b=c
regex = re.compile(r"(?=(=)).+(?=([ ])).+(?=(\bOR\b|\bAND\b|\bUNION\b)).+(?=([ ])).+(?=(=))",  flags=re.IGNORECASE)
# Matches sql injections that are like that: a=b%20AND%20= or a=b%20AND%20'
regex2 = re.compile(r"(?=(=)).+(?=([ ]|\b%20\b)).+(?=(%20OR\b|%20AND\b|%20UNION\b)).+(?=([ ]|\b%20\b)).+(?=(\b%27\b|=))",  flags=re.IGNORECASE)

try:
    while True:
        line = f.stdout.readline()
        if(len(line) == 0):
            break
        else:
            line = line.decode('utf-8').strip()

        if regex.search(line):
            res = line.split(" ")
            ip =  res[0]
            print(ip, flush=True)
        if regex2.search(line):
            res = line.split(" ")
            ip =  res[0]
            print(ip, flush=True)
        # match attempts to access hidden files/folders
        if "/." in line:
            res = line.split(" ")
            ip =  res[0]
            print(ip, flush=True)
        if(("/wp-login" in line) or ("/wp-admin" in line) or ("/wp-config" in line)):
            #  1.2.3.4 - - [09/Jan/2023:14:03:02 +0100] "GET /wp-admin/ HTTP/1.1" 401 583
            res = line.split(" ")
            ip =  res[0]
            print(ip, flush=True)

except:
    print("")

