#!/bin/bash
#SBATCH --job-name=patent_classification
#SBATCH --output=slurm_outputs/job_patent_output.txt
#SBATCH --error=slurm_outputs/job_patent_output_lines.txt
#SBATCH --ntasks=1
#SBATCH --time=24:00:00
#SBATCH --mem=32G
#SBATCH --cpus-per-task=4                    
#SBATCH --gres=gpu:1 ##2                        
#SBATCH -o slurm_outputs/patent_classification-%j.out 
#SBATCH --partition=unkillable

# 1. Load the environment
module load anaconda

## 2. Load your environment
source activate CondaEnv

# 2. Launch the job: Run the code
python3 patent_classification.py 