source venv/bin/activate
set -ueo pipefail


DATA_DIR=/Users/akre96/Documents/GradSchool/Class/BE223A/BE223A_2019/data
SUBJECT_NAME=subject_4
SUBJECT_DIR=$DATA_DIR/$SUBJECT_NAME
CT=$SUBJECT_DIR/postopCT*.nii
HULL=$SUBJECT_DIR/hull.mat


python segment_DBS.py \
  --ct $CT \
  --hull $HULL \
  --output-dir DBS_NII \
  --subject-name $SUBJECT_NAME \
  -p





