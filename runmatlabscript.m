is_windows = 0;
niter=10;
sigmaR=5000.0;
missing_data_correction=1;
grid_correction=0;
bias_correction=1;
if is_windows == 1
    base_path='C:/Users/chemh/Documents/Workspaces/gitRepos/rootvol';
    target_name='C:/Users/chemh/Documents/Workspaces/gitRepos/rootvol/autofluorescence_data.tif';
    registration_prefix='C:/Users/chemh/Documents/Workspaces/gitRepos/rootvol/data_processed_registration/';
    atlas_prefix='C:/Users/chemh/Documents/Workspaces/gitRepos/rootvol/CloudReg/cloudreg/registration/atlases/';
    dxJ0=[9.999999776482582, 9.999999776482582, 9.999999776482582];
else
    base_path='/home/exx/Documents/rootvol';
    target_name='/home/exx/Documents/rootvol/rootvol/autofluorescence_data.tif';
    registration_prefix='/home/exx/Documents/rootvol/data_processed_registration/';
    atlas_prefix='/home/exx/Documents/rootvol/CloudReg/cloudreg/registration/atlases/';
    dxJ0=[19.999999552965164, 19.999999552965164, 19.999999552965164];
end
fixed_scale=[1.0, 1.0, 1.0];
% initial_affine=[0.0, -1.0, 0.0, 0.0; 0.0, 0.0, -1.0, 0.0; -1.0, 0.0, 0.0, 0.0; 0.0, 0.0, 0.0, 1.0];
if is_windows == 1
    parcellation_voxel_size=[10.0, 10.0, 10.0];
    parcellation_image_size=[1320, 800, 1140];
else
    parcellation_voxel_size=[25.0, 25.0, 25.0];
    parcellation_image_size=[528, 320, 456];
end
    
run('C:/Users/chemh/Documents/Workspaces/gitRepos/rootvol/CloudReg/cloudreg/registration/map_nonuniform_multiscale_v02_mouse_gauss_newton.m');