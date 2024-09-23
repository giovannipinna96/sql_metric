#!/bin/bash

EXPR_PATH="/mnt/data/gpinna/sql_metric/sql_metric/src/pipeline/base_pipeline.py"

cd /mnt/data/gpinna/sql_metric/sql_metric/src

# for model in "sergeyvi4ev/all-MiniLM-RAGSQL-code" "s2593817/sft-sql-embedding"
# do
    for weight in $(seq 0.25 0.25 0.75);
    do
        for percentage in $(seq 0 0.10 0.90);
        do
            echo "Running expr.py with model = $model, weight = $weight, and percentage = $percentage"
            output_file="/mnt/data/gpinna/sql_metric/sql_metric/results/expr_model1_weightTable${weight}_percentage${percentage}.txt"
            { python "$EXPR_PATH" --model_name "s2593817/sft-sql-embedding" --weight_final_score_table $weight --max_extra_information_percentage $percentage; } > "$output_file"
            echo "Output saved to $output_file"
            echo "------------------------"
        done
    done
# done

# python_script="ponyge.py"
# files=("improvements/G4/GPT4_problem1.txt" "improvements/G4/GPT4_problem2.txt" "improvements/G4/GPT4_problem3.txt" "improvements/G4/GPT4_problem5.txt" "improvements/G4/GPT4_problem6.txt" "improve>
# output_directory="/mnt/data/gpinna/damiano_pony/LLMGIpy/"

# iterations=10
# echo "ok"

# for file in "${files[@]}"; do
#     file_name=$(basename $file)
#     output_file="$output_directory/times_$file_name.txt"
#     for ((i=1; i<=$iterations; i++)); do
#         { time python "$python_script" "--parameters" "$file"; } 2>&1 | grep "real" >> "$output_file"
#     done
# done