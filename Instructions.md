### Start docker image
docker run --rm -v ~/Documents/cloudreg/data/input:/data/input -v ~/Documents/cloudreg/data/output:/data/output -ti neurodata/cloudreg:local

### Inside docker image
- cd /root/
- git clone https://github.com/hding9/CloudReg.git
- cd CloudReg
- pip install --upgrade numpy
- python -m cloudreg.scripts.create_precomputed_volume_3d /data/input file:///data/output
- python3 -m cloudreg.scripts.registration -input_s3_path file:///data/output  --output_s3_path file:///data/output  -log_s3_path file:///data/output -orientation SLA
