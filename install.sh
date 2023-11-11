# miniforge3
CONDA='anaconda3' # IDE can automatically detect conda
wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh
bash Miniforge3-Linux-x86_64.sh -b -p $CONDA
source ~/$CONDA/etc/profile.d/conda.sh
source ~/$CONDA/etc/profile.d/mamba.sh

# somn
git clone https://github.com/alkorolyov/Lucid_Somnambulist
cd Lucid_Somnambulist/Lucid_Somnambulist
mamba env create --name somn --file somn.yml
conda activate somn
wget https://github.com/SEDenmarkLab/molli_firstgen/archive/refs/heads/main.zip -O ~/molli.zip 
pip install ~/molli.zip #molli package

pip install . -e # editable mode

# Check installation
python3 -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
python3 -c "import somn"
