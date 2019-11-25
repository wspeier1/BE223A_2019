DATA_DIR="/Users/hwz62/Desktop/alignment"
SUBJECT_DIR="/Users/hwz62/Desktop/alignment/subject_1"
CT="/Users/hwz62/Desktop/alignment/subject_1/preopCT*.nii"
HULL="/Users/hwz62/Desktop/alignment/subject_1/hull.mat"
python3 segment_skull.py \
  --ct ${CT} \
  --hull ${HULL} \
  --output-dir output \
  --subject-name subject_1 \
  -p