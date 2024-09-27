#!/bin/bash

module load python/3.11.6--gcc--8.5.0

source $WORK/gpinna00/phd_project/sql_metric/sql/bin/activate

cd $WORK/gpinna00/phd_project/sql_metric/sql_metric/src

EXPR_PATH="$WORK/gpinna00/phd_project/sql_metric/sql_metric/src/pipeline/base_pipeline.py"

echo "start bash"
start=$(date +%s)
python3 "$EXPR_PATH" --model_name ${1} --weight_final_score_table ${2} --max_extra_information_percentage ${3}
end=$(date +%s)
