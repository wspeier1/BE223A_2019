source venv/bin/activate
set -ueo pipefail


DATA_DIR=/Users/akre96/Documents/GradSchool/Class/BE223A/BE223A_2019/data
SUBJECT_NAME=subject_2
SUBJECT_DIR=$DATA_DIR/$SUBJECT_NAME
CT=$SUBJECT_DIR/preopCT*.nii
HULL=$SUBJECT_DIR/hull.mat


python segment_skull.py \
  --ct $CT \
  --hull $HULL \
  --output-dir SKULL_NII \
  --subject-name $SUBJECT_NAME \
  -p





