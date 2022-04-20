### Start docker image
The image neurodata/cloudreg:local has many flaws. The one that causes me most of time to debug is the shared memory settings.

By default, it is set to a few mega bytes, which will cause "Bus error" when writing images with SimpleITK.

To check shared memory configuration:

```
docker inspect <image id> | grep -i shm
```


While checking "docker-compose.yml" in CloudReg official repository, the shm_size is set to 20gb.

Thus, add option "--shm-size=20gb" to `docker run` command

**Note**: 

Download high resolution annotation data from aws seems always have connection failure when I was testing. Thus, I cut the original numpy array into pieces and download them seperately with `CloudVolume`. Once the data size is shrinked, it seems there's no problem for connection.

```bash
docker run --rm -v ~/Documents/CloudReg/data/input:/data/input -v ~/Documents/CloudReg/data/output:/data/output -v ~/Documents/CloudReg:/root/CloudReg --shm-size=20gb -ti neurodata/cloudreg:local
```

### Inside docker image
The basepath in `registration.py` is supposed to be "/root/" inside docker container.

Thus, first `cd` to `/root/`, then clone CloudReg.

`numpy` in `neurodata/cloudreg:local` container is outdated, which causes a bug when running python scripts. Also, it is stated in `Dockerfile` of the offical repository.


<pre><code>
<del>cd /root/ && \</del>
<del>git clone https://github.com/hding9/CloudReg.git && \</del>
<del>cd CloudReg && \</del>
pip install --upgrade numpy
</pre></code>

Generate files to `output` folder.

```bash
python -m cloudreg.scripts.create_precomputed_volume_3d /data/input file:///data/output
```

Run registration.
```bash
python3 -m cloudreg.scripts.registration -input_s3_path file:///data/output  --output_s3_path file:///data/output  -log_s3_path file:///data/output -orientation SLA
```
