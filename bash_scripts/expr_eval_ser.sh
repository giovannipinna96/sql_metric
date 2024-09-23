#!/bin/bash

EXPR_PATH="/mnt/data/gpinna/sql_metric/sql_metric/src/pipeline/base_pipeline.py"

cd /mnt/data/gpinna/sql_metric/sql_metric/src

# for model in "sergeyvi4ev/all-MiniLM-RAGSQL-code" "s2593817/sft-sql-embedding"
# do
    for weight in $(seq 0.25 0.25 0.75)
    do
        for percentage in $(seq 0 0.10 0.90)
        do
            echo "Running expr.py with model = $model, weight = $weight, and percentage = $percentage"
            output_file="/mnt/data/gpinna/sql_metric/sql_metric/results/expr_model${model}_weightTable${weight}_percentage${percentage}.txt"
            python "$EXPR_PATH" --model_name "sergeyvi4ev/all-MiniLM-RAGSQL-code" --weight_final_score_table $weight --max_extra_information_percentage $percentage > "$output_file"
            echo "Output saved to $output_file"
            echo "------------------------"
        done
    done
# done