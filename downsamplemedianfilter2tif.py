"""
Down sample hackathon nifti image and save to tif file.
Original image is 10 * 10 * 10 um in resolution.
Tif file doesn't have matadata, thus just save down graded
numpy into tif image.
"""
import os
import numpy as np
import nibabel as nib
import tifffile as tif
from glob import glob
from tqdm import tqdm
from scipy.ndimage import zoom
from scipy.signal import medfilt2d
from scipy.ndimage import median_filter

def slicer_downsample(img, factor):
    return img.slicer[::factor, ::factor, ::factor]


def medianfilter2d(img, size=3):
    """
    Param:
        img: 3d numpy array image stack
        kernelsize: int, default 3. kernel size of mean filter
    Return:
        New 3d numpy array image stack
    """

    for axis in range(img.ndim):
        s = (slice(None), ) * axis
        for ii in tqdm(range(img.shape[axis])):
            img[s+(ii,)] = median_filter(img[s+(ii,)], size=size)
        
    return img


if __name__ == "__main__":
    work_dir = "data/hackathon_data/"
    factor = 2
    file_paths = glob(os.path.join(work_dir, "*_SLA.nii.gz"))

    for f in file_paths:
        img = nib.load(f)
        img_data = np.array(img.dataobj).astype("uint16")   # (659, 1078, 1125)     ImageJ read it as (W, H, Z)

        img_down = zoom(img_data, (1/factor,)*3)            # (330, 539, 562)       ImageJ read it as (W, H, Z)
        img_down = img_down.transpose(1, 0, 2)              # (539, 339, 562)

        # for ii in tqdm(range(img_down.shape[2])):
        #     img_down[...,ii] = median_filter(img_down[...,ii], kernel_size=5)
        img_down = medianfilter2d(img_down, size=7)
        # img_down_obj = nib.Nifti1Image(img_down, affine=np.eye(4))
        # nib.save(img_down_obj, 'testk5.nii.gz')
        tif.imwrite('autofluorescence_data.tif', img_down)