## Start docker image
The image neurodata/cloudreg:local has many flaws. The one that causes me most of time to debug is the shared memory settings.

By default, it is set to a few mega bytes, which will cause "Bus error" when writing images with SimpleITK.

To check shared memory configuration:

```
docker inspect <image id> | grep -i shm
```


#### Option 1: use docker run
While checking "docker-compose.yml" in CloudReg official repository, the shm_size is set to 20gb.

Thus, add option "--shm-size=20gb" to `docker run` command

**Note**: 

Download high resolution annotation data from aws seems always have connection failure when I was testing. Thus, I cut the original numpy array into pieces and download them seperately with `CloudVolume`. Once the data size is shrinked, it seems there's no problem for connection.

```bash
docker run --rm -v ~/Documents/CloudReg/data/input:/data/input -v ~/Documents/CloudReg/data/output:/data/output -v ~/Documents/CloudReg:/root/CloudReg --shm-size=20gb -ti neurodata/cloudreg:local
```

#### Option 2: use docker-compose

This option starts both `neurodata/cloudreg:local` and `mathworks/matlab-deep-learning:latest` docker container.

The `numpy` package in `neurodata/cloudreg:local` is outdated, and there are also some folder mapping issue. First fix them by run image in interactive mode:

```bash
docker run --rm -it neurodata/cloudreg:local
```

Then, inside container console, remove the redundant `CloudReg` folder since we are going to mount the host folder as the volume.

```bash
cd /
rm -rf CloudReg/ \~/
```

Update `numpy` package,

```bash
pip install --upgrade numpy
```

At last, open another terminal
```bash
docker commit CONTAINER_ID neurodata/cloudreg:local
```

Then, start container with `docker-compose up -d` in `CloudReg` folder. To stop, type `docker-compose down`.

Two containers will build and run, `cloudreg-cloudreg-1` and `cloudreg-matlab-1`

To bash into one of the container:

```bash
docker exec -it cloudreg-cloudreg-1 bash
```


## Inside docker container
The basepath in `registration.py` is supposed to be "/root/" inside docker container.

Thus, first `cd` to `/root/`, then clone CloudReg.

`numpy` in `neurodata/cloudreg:local` container is outdated, which causes a bug when running python scripts. Also, it is stated in `Dockerfile` of the offical repository.


<pre><code>
<del>cd /root/ && \</del>
<del>git clone https://github.com/hding9/CloudReg.git && \</del>
<del>cd CloudReg && \</del>
<del>pip install --upgrade numpy\</del>
</pre></code>

Generate files to `output` folder.

```bash
python -m cloudreg.scripts.create_precomputed_volume_3d /data/input file:///data/output
```

Run registration.
```bash
python3 -m cloudreg.scripts.registration -input_s3_path file:///data/output  --output_s3_path file:///data/output  -log_s3_path file:///data/output -orientation SLA
```

The generated matlab command will be similar like:

```bash
matlab -nodisplay -nosplash -nodesktop -r "niter=3000;sigmaR=5000.0;missing_data_correction=1;grid_correction=0;bias_correction=1;base_path='/root/';target_name='/root//autofluorescence_data.tif';registration_prefix='/root//data_output_registration/';atlas_prefix='/root//CloudReg/cloudreg/registration/atlases/';dxJ0=[9.999999776482582, 9.999999776482582, 9.999999776482582];fixed_scale=[1.0, 1.0, 1.0];initial_affine=[0.0, -1.0, 0.0, 0.0; 0.0, 0.0, -1.0, 0.0; -1.0, 0.0, 0.0, 0.0; 0.0, 0.0, 0.0, 1.0];parcellation_voxel_size=[10.0, 10.0, 10.0];parcellation_image_size=[1320, 800, 1140];tic;run('~/CloudReg/cloudreg/registration/map_nonuniform_multiscale_v02_mouse_gauss_newton.m');toc;exit;"
```

**Note**: matlab may need to be run as elevated privileges since the code create directories.
