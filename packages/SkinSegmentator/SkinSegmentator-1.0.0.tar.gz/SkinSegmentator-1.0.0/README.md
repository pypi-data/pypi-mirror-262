# SkinSegmentator


### Installation

SkinSegmentator works on Ubuntu, Mac, and Windows and on CPU and GPU.

Install dependencies:
* Python >= 3.9
* [Pytorch](http://pytorch.org/) >= 2.0.0

Optionally:
* if you use the option `--preview` you have to install xvfb (`apt-get install xvfb`)


Install SkinSegmentator
```
pip install SkinSegmentator
```


### Usage
```
SkinSegmentator -i mr.nii.gz -o segmentations
```
> Note: A Nifti file or a folder with all DICOM slices of one patient is allowed as input

> Note: If you run on CPU use the option `--fast` or `--roi_subset` to greatly improve runtime.

> Note: This is not a medical device and is not intended for clinical usage.



### Python API
You can run SkinSegmentator via Python:
```python
import nibabel as nib
from SkinSegmentator.python_api import SkinSegmentator

if __name__ == "__main__":
    # option 1: provide input and output as file paths
    SkinSegmentator(input_path, output_path)

    # option 2: provide input and output as nifti image objects
    input_img = nib.load(input_path)
    output_img = SkinSegmentator(input_img)
    nib.save(output_img, output_path)
```
You can see all available arguments [here](https://github.com/reubendo/SkinSegmentator/blob/master/SkinSegmentator/python_api.py). Running from within the main environment should avoid some multiprocessing issues.

The segmentation image contains the names of the classes in the extended header. If you want to load this additional header information you can use the following code:
```python
from SkinSegmentator.nifti_ext_header import load_multilabel_nifti

segmentation_nifti_img, label_map_dict = load_multilabel_nifti(image_path)
```
The above code requires `pip install xmltodict`.


### Install latest master branch (contains latest bug fixes)
```
pip install git+https://github.com/reubendo/SkinSegmentator.git
```


### Typical problems

**ITK loading Error**
When you get the following error message
```
ITK ERROR: ITK only supports orthonormal direction cosines. No orthonormal definition was found!
```
you should do
```
pip install SimpleITK==2.0.2
```

Alternatively you can try
```
fslorient -copysform2qform input_file
fslreorient2std input_file output_file
```


### Reference
TODO

