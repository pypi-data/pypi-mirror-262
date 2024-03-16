from typing import List, Optional
from pydantic import BaseModel

class InferenceSchema(BaseModel):
    business_domain: str = "string",
    limit: int = 0,
    offset: int = 0,
    service_domain_id: Optional[List[int]] = None,
    service_domain_slug: Optional[List[str]] = None,
    ai_domain: str = "string",
    ai_subdomain: str = "string",
    user: str = "string",
    group_id: str = "string",
    order_by: str = "string"

class MetadataVisionSchema(BaseModel):
    image_size_kb: float
    area: float
    aspect_ratio_hw: float
    blue_values: float
    blur: float
    brightness: float
    contrast: float
    green_values: float
    red_values: float
    sharpness: float
    height: int
    width: int
    channels: int
    confidence_threshold: float | None
    saturation_std: float
    saturation_mean: float