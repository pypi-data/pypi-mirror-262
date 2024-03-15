import ants
import random

from .base_transform import BaseTransform


class Resample(BaseTransform):
    """
    img = ants.image_read(ants.get_ants_data('mni'))
    # resample voxel directly (fine if image has even dimensions.. not here though)
    my_tx = ResampleImage((60,60,60))
    img2 = my_tx(img)
    # resample with spacing so you dont have to figure out uneven dimensions
    my_tx2 = ResampleImage((4,4,4), use_spacing=True)
    img3 = my_tx2(img)
    """
    def __init__(self, params, use_spacing=False, interpolation='linear'):
        self.params = params
        self.use_spacing = use_spacing
        self.interpolation = 0 if interpolation != 'nearest_neighbor' else 1 
    
    def __call__(self, image):
        image = ants.resample_image(image, self.params, not self.use_spacing, self.interpolation)
        return image


class ResampleToTarget(BaseTransform):
    """
    img = ants.image_read(ants.get_ants_data('mni'))
    img2 = img.clone().resample_image((4,4,4))
    my_tx = ResampleImageToTarget(img2)
    img3 = my_tx(img)
    """
    def __init__(self, target, interpolation='linear'):
        self.target = target
        self.interpolation = 0 if interpolation != 'nearest_neighbor' else 1 
    
    def __call__(self, image):
        image = ants.resample_image_to_target(image, self.target, self.interpolation)
        return image


class Reorient(BaseTransform):
    """
    Reorient an image.
    
    Images are oriented along three axes:
    - Right (R) to Left (L)
    - Inferior (I) to Superior (S) 
    - Anterior (A) to Posterior (P)
    
    An image orientation consists of three letters - one from each
    of the three axes - with the letter for each axes determining
    where the indexing starts. Orientation is important for slicing.
    """
    def __init__(self, orientation='RAS'):
        self.orientation = orientation
    
    def __call__(self, image):
        image = ants.reorient_image2(image, self.orientation)
        

class Slice(BaseTransform):
    """
    Slice a 3D image into 2D. 
    """
    def __init__(self, axis, idx):
        self.axis = axis
        self.idx = idx
    
    def __call__(self, image):
        if self.idx is None:
            new_image = [image.slice_image(self.axis, idx) for idx in range(image.shape[self.axis])]
        else:
            new_image = image.slice_image(self.axis, self.idx)
        return new_image


class RandomSlice(BaseTransform):
    """
    Randomly slice a 3D image into 2D. 
    
    """
    def __init__(self, axis, allow_blank=True):
        self.axis = axis
        self.allow_blank = allow_blank
    
    def __call__(self, image):
        if not self.allow_blank:
            image = image.crop_image()
        
        idx = random.sample(range(image.shape[self.axis]))[0]
        new_image = image.slice_image(self.axis, idx)
        
        return new_image


class Crop(BaseTransform):
    """
    Crop an image to remove all blank space around the brain or
    crop based on specified indices.
    """
    def __init__(self, lower_indices=None, upper_indices=None):
        self.lower_indices = lower_indices
        self.upper_indices = upper_indices
    
    def __call__(self, image):
        if self.lower_indices and self.upper_indices:
            new_image = image.crop_indices(self.lower_indices,
                                           self.upper_indices)
        else:
            new_image = image.crop_image()
        return new_image


class RandomCrop(BaseTransform):
    """
    Randomly crop an image of the specified size
    
    Examples
    --------
    >>> import ants
    >>> from nitrain import transforms as tx
    >>> mni = ants.image_read(ants.get_data('mni'))
    >>> my_tx = tx.RandomCrop(size=(30,30,30))
    >>> mni_crop = my_tx(mni)
    >>> mni_crop.plot(domain_image_map=mni)
    >>> mni_orig = mni_crop.decrop_image(mni) # put image back
    """
    def __init__(self, size):
        self.size = size
    
    def __call__(self, image):
        size = self.size
        if isinstance(size, int):
            size = tuple([size for _ in range(image.dimension)])
            
        lower_indices = [random.sample(range(0, image.shape[i]-size[0]), 1)[0] for i in range(len(size))]
        upper_indices = [lower_indices[i] + size[i] for i in range(len(size))]
            
        new_image = image.crop_indices(lower_indices,
                                       upper_indices)
        return new_image


class Pad(BaseTransform):
    """
    Pad an image to a specified shape or by a specified amount.
    
    Example
    -------
    >>> import ants
    >>> from nitrain import transforms as tx
    >>> mni = ants.image_read(ants.get_data('mni'))
    >>> my_tx = tx.Pad((220,220,220))
    >>> mni_pad = my_tx(mni)
    """
    
    def __init__(self, shape=None, width=None, value=0.0):
        if shape is None and width is None:
            raise Exception('Either shape or width must be supplied to Pad transform.')
        self.shape = shape
        self.width = width
        self.value = value
    
    def __call__(self, image):
        new_image = image.pad_image(shape=self.shape,
                                    pad_width=self.width,
                                    value=self.value)
        return new_image