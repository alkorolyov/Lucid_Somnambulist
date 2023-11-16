#!/bin/bash

# create tmp dir
mkdir $TMP_DIR

# copy coords
x2t $1 > $TMP_DIR/coord
cd $TMP_DIR

define <<EOF


a coord
*
no
b all $2
*
eht



dft
on
func b3-lyp
*
*
EOF

# single point
#dscf coord

# geometry optimization
uff
jobex