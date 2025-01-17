# CUDA 11.8 and cuDNN 8.6
#wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-keyring_1.0-1_all.deb
#sudo dpkg -i cuda-keyring_1.0-1_all.deb
#sudo apt-get update
#sudo apt-get -y install cuda=11.8.0-1
#
#sudo apt-get install libcudnn8=8.6.0.163-1+cuda11.8
#sudo apt-get install libcudnn8-dev=8.6.0.163-1+cuda11.8
#sudo apt-get install libcudnn8-samples=8.6.0.163-1+cuda11.8

# miniforge3
#CONDA='anaconda' # IDE can automatically detect conda
wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh
bash Miniforge3-Linux-x86_64.sh -b
echo "source ~/miniforge3/etc/profile.d/conda.sh" >> ~/.bashrc
echo "source ~/miniforge3/etc/profile.d/mamba.sh" >> ~/.bashrc

# somn
cd
git clone https://github.com/alkorolyov/Lucid_Somnambulist
cd Lucid_Somnambulist/Lucid_Somnambulist
mamba env create --name somn --file somn.yml
conda activate somn
wget https://github.com/SEDenmarkLab/molli_firstgen/archive/refs/heads/main.zip -O ~/molli.zip 
~/miniforge3/envs/somn/bin/pip install ~/molli.zip #molli package

~/miniforge3/envs/somn/bin/pip install -e . # editable mode

# Check installation
# python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
python -c "import somn"
