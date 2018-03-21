#!/bin/bash
ssh $1@ssh1.iitd.ac.in 'bash -s'  <username.sh $1 $2 
scp $1@ssh1.iitd.ac.in:username.txt ./
python3 find-malicious.py username.txt