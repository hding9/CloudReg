### Start docker image
docker run --rm -v ~/Documents/cloudreg/data/input:/data/input -v ~/Documents/cloudreg/data/output:/data/output -ti neurodata/cloudreg:local

### Inside docker image
- cd ..
- git clone git@github.com:hding9/CloudReg.git
- cd CloudReg
- pip install --upgrade numpy
- python -m cloudreg.scripts.create_precomputed_volume_3d /data/input file:///data/output
