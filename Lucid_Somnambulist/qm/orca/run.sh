#!/bin/bash

xyz_file="$1"
inp_file="input.inp"

# Check if the XYZ file exists
if [ ! -e "$xyz_file" ]; then
    echo "Error: XYZ file not found."
    exit 1
fi

# Create the input file
cat <<EOF >"$inp_file"
!B3LYP DEF2-SVP OPT
%pal nprocs 24 end
%geom
   MaxIter 100
   end

* xyz 0 1
EOF
# Append the coordinates from the XYZ file to the input file
tail -n +3 "$xyz_file" >> "$inp_file"
# Add the optimization and method sections
cat <<EOF >>"$inp_file"
*
EOF

echo "Input file '$inp_file' generated successfully."

mkdir .tmp
mv $inp_file .tmp
cd .tmp

/opt/orca-5.0.3/orca/orca input.inp --use-hwthread-cpus