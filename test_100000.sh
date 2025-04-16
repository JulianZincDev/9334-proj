#!/bin/sh


for i in $(seq 1000)
do
    dash run_test.sh 5
    dash run_test.sh 6
    dash run_test.sh 7
    # sleep 0.01
    
    out1=$(python3 cf_output_with_ref.py 5)
    echo ${i}: $out1 >> test5out.txt
    out2=$(python3 cf_output_with_ref.py 6)
    echo ${i}: $out2 >> test6out.txt
    out3=$(python3 cf_output_with_ref.py 7)
    echo ${i}: $out3 >> test7out.txt
done

