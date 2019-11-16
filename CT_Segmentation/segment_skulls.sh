source venv/bin/activate
set -ueo pipefail


DATA_DIR=/Users/akre96/Documents/GradSchool/Class/BE223A/BE223A_2019/data
SUBJECT_DIR=$DATA_DIR/subject_2
CT=$SUBJECT_DIR/preopCT*.nii
HULL=$SUBJECT_DIR/hull.mat


python segment_skull.py \
  --ct $CT \
  --hull $HULL \
  --output-dir output \
  --subject-name subject_2 \
  -p





