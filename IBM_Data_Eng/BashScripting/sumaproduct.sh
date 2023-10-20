#!/bin/bash

echo -n "Enter an integer: "
read n1
echo -n "Enter another integer: "
read n2
sum=$(($n1 + $n2))
product=$(($n1 * $n2))
echo "The sum of $n1 and $n2 is $sum"
echo "The product of $n1 and $n2 is $product."

if [ "$n1" -lt "$n2" ]; then
    echo "$n1 is less than $n2"
elif [ "$n1" -gt "$n2" ]; then
    echo "$n1 is greater than $n2"
else
    echo "$n1 is equal to $n2"
fi

