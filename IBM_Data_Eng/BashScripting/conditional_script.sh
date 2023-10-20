#!/bin/bash

echo 'Are you enjoying this course so far?'
echo -n "Enter \"y\" for yes, \"n\" for no."
read response
if [ "$response" = "y" ]
then
    echo "I'm pleased to hear you are enjoying the course!"
elif [ "$response" = "n" ]
then
    echo "Im sorry"
else
    echo "yes or no"
fi
