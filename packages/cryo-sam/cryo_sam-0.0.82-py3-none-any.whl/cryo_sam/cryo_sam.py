from segment_anything import SamAutomaticMaskGenerator, SamPredictor, sam_model_registry
from .structures import *
from .utils import *
import torch

class Csam:
    def __init__(self, model_name, model_checkpoint, device = "cuda", kwargs = None):
        if not kwargs:
            kwargs = {
                "points_per_side": 64,
                "pred_iou_thresh": 0.92,
                "stability_score_thresh": 0.96,
            }

        self.model = model_name
        self.checkpoint = model_checkpoint
        self.device = device

        self.__load_model(kwargs)

    def __load_model(self, kwargs):
        sam = sam_model_registry[self.model](checkpoint = self.checkpoint)
        sam.to(self.device)

        if kwargs:
            kwargs = kwargs
        else:
            kwargs = None

        self.mask_generator = SamAutomaticMaskGenerator(sam, **kwargs)
        self.predictor = SamPredictor(sam)   

    def square_finder(self, image, pixel_size = None,
                      upper_size = 800000,
                      lower_size = 50000):
        
        if self.device != "cpu":
            torch.cuda.empty_cache()
        
        image = Utils.smooth_normalize_image(image, 1)

        masks = self.mask_generator.generate(image)
        results = CryoImageResults(image, masks)

        if pixel_size:
            length = len(results.bounding_boxes)
            for i in range(length):
                result = results.bounding_boxes[length - i - 1]

                angstroms_width = result[2] * pixel_size
                angstroms_height = result[3] * pixel_size

                smallest = min(angstroms_width, angstroms_height)
                biggest = max(angstroms_width, angstroms_height)
                
                if lower_size > smallest or biggest > upper_size:
                    results.remove_idx(length - i - 1)
        else:
            results = Utils.trim_by_area(results, 2.5)

        Utils.remove_nested_bounding_boxes(results)

        return results
    
    def hole_finder(self, image, pixel_size = None,
                     upper_size = 30000,
                     lower_size = 20000):
        
        if self.device != "cpu":
            torch.cuda.empty_cache()

        image = Utils.smooth_normalize_image(image, 1)

        masks = self.mask_generator.generate(image)
        results = CryoImageResults(image, masks)

        if pixel_size:

            length = len(results.bounding_boxes)

            for i in range(length):
                result = results.bounding_boxes[length - i - 1]

                angstroms_width = result[2] * pixel_size
                angstroms_height = result[3] * pixel_size

                smallest = min(angstroms_width, angstroms_height)
                biggest = max(angstroms_width, angstroms_height)
                
                if lower_size > smallest or biggest > upper_size:
                    results.remove_idx(length - i - 1)

        else:
            results = Utils.trim_by_area(results, 2.0)

        Utils.remove_nested_bounding_boxes(results)

        return results
