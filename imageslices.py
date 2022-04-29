import SimpleITK as sitk
import numpy as np
from glob import glob
from tqdm import tqdm
from PIL import Image
import re
import nibabel as nib
import tifffile as tif



def read_nii_bysitk(input_path, peel_info=True):
    """ read nii to numpy through simpleitk
        peelinfo: taking direction, origin, spacing and metadata out
    """
    img_obj = sitk.ReadImage(input_path)
    img_np = sitk.GetArrayFromImage(img_obj).astype(np.uint16)
    if peel_info:
        info_obj = {
                "spacing": img_obj.GetSpacing(),
                "origin": img_obj.GetOrigin(),
                "direction": img_obj.GetDirection(),
                "array_size": img_np.shape
                }
        return img_np, info_obj
    else:
        return img_np

def nii2tif_slices(input_path, output_path, slice_path, factor=1):
    """
    input_path: hackathon data path contains original data
    output_path: path that contains slices of the data.
    factor: downsample factor, indicates which file in input_data to be sliced.
    """
    file_paths = glob(f"{input_path}/*.nii.gz")
    for i, f_path in enumerate(file_paths):
        if factor == 1:
            if re.search(r"SLA.nii.gz", f_path):
                file_path = f_path
                break
            else:
                raise FileNotFoundError
        else:
            if f"down{factor}" in f_path:
                file_path = f_path
            else:
                if i >= len(file_paths):
                    raise FileNotFoundError



    file_path = file_path.replace('\\', '/')
    print(f"[DEBUG] Target file: {file_path}")
    # cannot handle multiple nii images when they have different pixel sizes
    # thus read only the first image by default
    # img, info = read_nii_bysitk(file_path, peel_info=True)
    img = nib.load(file_path)

    ############################# NOTE ############################
    # numpy array returned by SimpleITK GetArrayFromImage is in ZYX shape
    # The moving image I am testing is in SLA orientation, here
    # X -> S (Superior); Y -> L (Left); Z -> A (Anterior)
    #############################  ############################
    
    # img_size = info['array_size']
    img_size = img.shape
    print(f"[DEBUG] img_size is {img_size}")
    # print(f"[DEBUG] numpy array size is {img.shape}")
    
    # The original image voxel size is in mm scale, convert to micron(um) scale to
    # be the same with average template.
    # Based on comments in create_precomputed_volume function,
    # Voxel size of image is in X,Y,Z in microns
    # voxel_size = [s*1000 for s in info['spacing']][::-1]
    voxel_size = [s * 1000 for s in img.header['pixdim']]
    z = img_size[1]

    digits = 0
    z_total = z
    while (z_total > 0):
        digits +=1
        z_total = int(z_total / 10)
    
    # dd = 10 ** (digits-1)
    # dd = int(z / dd) * 10
    dd = 1
    
    # in order to make the new tif image looks the same as the nii.gz image
    img = img.get_fdata().astype(np.uint16).transpose(1,0,2)

    tif.imwrite(output_path, img)

    file_name = file_path.split('/')[-1].strip('.nii.gz')
    for i in tqdm(np.arange(0, z, dd), desc="Saving slices"):
        im = Image.fromarray(img[i,...])
        im.save(f"{slice_path}/{file_name}_{str(i).zfill(digits)}.tif")
        
    return voxel_size



if __name__ == "__main__":
    input_path = "data/hackathon_data"
    slice_path = "data/raw"
    output_path = "autofluorescence_data.tif"
    factor = 2

    voxel_size = nii2tif_slices(input_path, output_path, slice_path, factor)
    print(f"Voxel_size is {voxel_size}")