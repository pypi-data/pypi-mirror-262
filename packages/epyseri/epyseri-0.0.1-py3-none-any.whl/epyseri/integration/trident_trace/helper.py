from typing import List, Union

import cv2
import numpy as np
from numpy import ndarray

from .schemas import MetadataVisionSchema


class Wrapper:
    # we can't have a non-default-constructible Metric implementation at module level
    class ColorMetric:
        def __init__(
            self,
            color_name: str,
            hue_filters: Union[List, List[List]],
            saturation_filters=[50, 255],
            value_filters=[20, 255],
        ):
            self.color_name = color_name
            self.hue_filters = hue_filters
            self.saturation_filters = saturation_filters
            self.value_filters = value_filters

            hsv_test = all(
                0 <= item <= 179 for item in self.__flatten_nested_lists(hue_filters)
            )
            if not hsv_test:
                raise ValueError("Hue parameter should be in [0, 179]")

            saturation_test = all(0 <= item <= 255 for item in saturation_filters)
            if not saturation_test:
                raise ValueError("Saturation parameter should be in [0, 255]")

            value_test = all(0 <= item <= 255 for item in value_filters)
            if not value_test:
                raise ValueError("Value parameter should be in [0, 255]")

        def __flatten_nested_lists(self, nested_list):
            out = []

            for item in nested_list:
                if isinstance(item, list):
                    out.extend(self.__flatten_nested_lists(item))
                else:
                    out.append(item)
            return out

        def compute(self, image_rgb: ndarray):
            image = image_rgb
            if self.color_name.lower() != "red":
                mask = cv2.inRange(
                    image,
                    np.array(
                        [
                            self.hue_filters[0],
                            self.saturation_filters[0],
                            self.value_filters[0],
                        ]
                    ),
                    np.array(
                        [
                            self.hue_filters[1],
                            self.saturation_filters[1],
                            self.value_filters[1],
                        ]
                    ),
                )
                ratio = np.sum(mask > 0) / (image.shape[0] * image.shape[1])

            else:
                lower_spectrum = [
                    np.array(
                        [
                            self.hue_filters[0][0],
                            self.saturation_filters[0],
                            self.value_filters[0],
                        ]
                    ),
                    np.array(
                        [
                            self.hue_filters[0][1],
                            self.saturation_filters[1],
                            self.value_filters[1],
                        ]
                    ),
                ]
                upper_spectrum = [
                    np.array(
                        [
                            self.hue_filters[1][0],
                            self.saturation_filters[0],
                            self.value_filters[0],
                        ]
                    ),
                    np.array(
                        [
                            self.hue_filters[1][1],
                            self.saturation_filters[1],
                            self.value_filters[1],
                        ]
                    ),
                ]

                lower_mask = cv2.inRange(image, lower_spectrum[0], lower_spectrum[1])
                upper_mask = cv2.inRange(image, upper_spectrum[0], upper_spectrum[1])
                mask = lower_mask + upper_mask
                ratio = np.sum(mask > 0) / (image.shape[0] * image.shape[1])
            return ratio

# Inputs for new color algorithm
class RedMetric(Wrapper.ColorMetric):
    def __init__(self):
        super(RedMetric, self).__init__("Red", hue_filters=[[0, 10], [170, 179]])

class GreenMetric(Wrapper.ColorMetric):
    def __init__(self):
        super(GreenMetric, self).__init__("Green", hue_filters=[35, 75])

class BlueMetric(Wrapper.ColorMetric):
    def __init__(self):
        super(BlueMetric, self).__init__("Blue", hue_filters=[90, 130])

class FeaturesImage:
    @staticmethod
    def area(image: ndarray):
        return image.shape[0] * image.shape[1]

    @staticmethod
    def aspect_ratio_hw(image: ndarray):
        h, w, c = image.shape
        return h / w

    @staticmethod
    def aspect_ratio_wh(image: ndarray):
        h, w, c = image.shape
        return w / h

    @staticmethod
    def blur(image_rgb: ndarray):
        gray = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)
        return 1 - cv2.Laplacian(gray, cv2.CV_64F).var()

    @staticmethod
    def sharpness(image_rgb: ndarray):
        gray = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)
        return cv2.Laplacian(gray, cv2.CV_64F).var()

    @staticmethod
    def brightness(image_rgb: ndarray):
        return image_rgb.mean() / 255

    @staticmethod
    def contrast(image_rgb: ndarray):
        return image_rgb.std() / 255

    @staticmethod
    def saturation(image_rgb: ndarray):
        hsv = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2HSV)
        saturation_mean, saturation_std = cv2.meanStdDev(hsv[:, :, 1])
        return saturation_mean[0][0], saturation_std[0][0]

    @staticmethod
    def red_values(image_rgb: ndarray):
        return RedMetric().compute(image_rgb)

    @staticmethod
    def green_values(image_rgb: ndarray):
        return GreenMetric().compute(image_rgb)

    @staticmethod
    def blue_values(image_rgb: ndarray):
        return BlueMetric().compute(image_rgb)

    @staticmethod
    def compute_features(image_bgr: ndarray) -> dict:
        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        sat_mean_std = FeaturesImage.saturation(image_rgb)
        metadatafeatures = {
            "image_size_kb": image_rgb.size / 1024,
            "area": FeaturesImage.area(image_rgb),
            "aspect_ratio_hw": FeaturesImage.aspect_ratio_hw(image_rgb),
            "width": image_rgb.shape[1],
            "height": image_rgb.shape[0],
            "channels": image_rgb.shape[2],
            "blur": FeaturesImage.blur(image_rgb),
            "sharpness": FeaturesImage.sharpness(image_rgb),
            "brightness": FeaturesImage.brightness(image_rgb),
            "contrast": FeaturesImage.contrast(image_rgb),
            "red_values": FeaturesImage.red_values(image_rgb),
            "green_values": FeaturesImage.green_values(image_rgb),
            "blue_values": FeaturesImage.blue_values(image_rgb),
            # "aspect_ratio_wh": FeaturesImage.aspect_ratio_wh(image_rgb),
            "saturation_mean": sat_mean_std[0],
            "saturation_std": sat_mean_std[1],
        }
        return metadatafeatures
        