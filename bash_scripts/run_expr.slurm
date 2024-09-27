#!/bin/bash
#SBATCH --nodes=1               
#SBATCH --ntasks-per-node=1 
#SBATCH --time=40:00:00         
#SBATCH --error=all_MiniLM_RAGSQL_code_025_0.err   
#SBATCH --output=all_MiniLM_RAGSQL_code_025_0.out  
#SBATCH --account=uts24_pinna       
#SBATCH --partition=boost_usr_prod
#SBATCH --gres=gpu:0                      
#SBATCH --cpus-per-task=5          
#SBATCH --mem=165gb   
#SBATCH --qos=boost_qos_lprod                 


cd $WORK/gpinna00/phd_project/sql_metric/sql_metric/bash_scripts

srun run_expr.sh "sergeyvi4ev/all-MiniLM-RAGSQL-code" 0.25 0