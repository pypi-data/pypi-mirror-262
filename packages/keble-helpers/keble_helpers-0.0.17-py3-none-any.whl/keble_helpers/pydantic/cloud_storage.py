from pydantic import BaseModel, AnyHttpUrl
from .config import PydanticModelConfig
from enum import Enum
from typing import Optional

class CloudStorageType(str, Enum):
    AWS_S3 = "AWS_S3"
    ALIYUN_OSS = "ALIYUN_OSS"


class CloudStorageObjectType(str, Enum):
    IMAGE = "IMAGE",
    VIDEO = "VIDEO",
    EXCEL = "EXCEL",
    CSV = "CSV",
    OTHER = "OTHER",


class CloudStorageBase(BaseModel):
    """Provide a universal CloudStorage Class for different
    cloud service platform"""

    model_config = PydanticModelConfig.default()

    # key for AWS is straightforward, for aliyun, it is name/or oss path.
    # they all refer as key
    key: str

    # endpoint of the cloud storage
    # base_url + key should be the URL of the cloud storage
    base_url: AnyHttpUrl

    # type of cloud service
    type: CloudStorageType

    # type of file
    object_type: CloudStorageObjectType

    # original file name
    original_file_name: Optional[str]
