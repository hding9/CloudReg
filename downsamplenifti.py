import os
import nibabel as nib
from glob import glob

def slicer_downsample(img, factor):
    return img.slicer[::factor, ::factor, ::factor]


if __name__ == "__main__":
    work_dir = "data/hackathon_data/"
    factor = 2
    file_paths = glob(os.path.join(work_dir, "*_SLA.nii.gz"))

    for f in file_paths:
        img = nib.load(f)
        img = slicer_downsample(img, factor)
        f_ds = f.split(".")[0]
        f_ds = f"{f_ds}_down{factor}.nii.gz"
        nib.save(img, f_ds)