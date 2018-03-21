#!/bin/bash
cd /home/cse/
for i in $(ls)
do
	ls $i >> /home/cse/$2/$1/username.txt
done
