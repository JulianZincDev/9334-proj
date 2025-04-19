#!/bin/sh

test_num_start=$1
test_num_end=$2
seed_start=$3
seed_end=$4


for i in $(seq $test_num_start $test_num_end)
do
    for seed in $(seq $seed_start $seed_end)
    do
        python3 main.py $i $seed $seed
    done
done

for i in $(seq $test_num_start $test_num_end)
do
    python3 trace_smoother.py $i $seed_start $seed_end
done
