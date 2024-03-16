from dataclasses import dataclass
import io
import os
from typing import Optional, Union, List
from datetime import datetime

from ..constants import AssetsConstants, AssetIngestionLimits
from ..custom_exceptions import EmbeddingError
from ..models.annotation import Annotation
from ..tools.logger import get_logger
from ..tools.misc import get_md5_from_json_object, hash_string_into_positive_integer_reproducible, get_guid
from ..tools.naming import get_similarity_index_name, standardize_name, assert_standardized, convert_booleans_to_string

logger = get_logger(__name__)

try:
    import numpy as np
except ImportError as e:
    logger.warning("Could not import package: {}".format(e))


class UnstructuredInputAsset:
    def __init__(self,
                 id: Optional[str] = None,
                 path: Optional[str] = None,
                 url: Optional[str] = None,
                 uri: Optional[str] = None,
                 bytes: Optional[Union[io.BytesIO, bytes, str]] = None,
                 sensor: Optional[str] = None,
                 timestamp: Optional[Union[str, datetime]] = None,
                 session_uid: Optional[str] = None,
                 aux_metadata: Optional[dict] = None
                 ):
        self.id = id
        self.path = path
        self.url = url
        self.uri = uri
        self.bytes = bytes
        self.sensor = sensor
        self.timestamp = timestamp
        self.session_uid = session_uid
        self.aux_metadata = aux_metadata
        self.post_init()

    def post_init(self):
        # Validate inputs
        assert sum(x is not None for x in [self.path, self.url, self.uri, self.bytes]) == 1, \
            "One and only one of [path, url, uri, bytes] should be specified"

        if self.id is None:
            self.id = get_guid()
        else:
            self.id = standardize_name(self.id)

        assert isinstance(self.id, str), "asset id should be a string"

        if self.timestamp is None:
            self.timestamp = datetime.utcnow()

        if self.path:
            assert os.path.exists(self.path), f"path {self.path} does not exist"

        if self.aux_metadata:
            self.aux_metadata = convert_booleans_to_string(self.aux_metadata)


class Image(UnstructuredInputAsset):
    """Create a SceneBox Image asset.

        Parameters
        ----------
        id:
            Optional, string. An identifier that is unique for the image asset throughout SceneBox.
        path:
            String. The local path to the image to upload. If not None, url, uri,
            and bytes should all be None.
        url:
            String. The URL of the image to upload. Images must be publicly available.
            If not None, url, uri, and path should all be None.
        uri:
            String. The URI of the image to upload. Can be from a private source.
            If not None, url, path, and bytes should all be None.
        bytes:
            io.BytesIO or bytes, string. The image bytes to upload.
            If not None, path, url, and uri should all be None.
        sensor:
            Optional, string. The sensor associated with the image.
        timestamp:
            Optional, either a string or a datetime. The time at which the image was taken.
        session_uid:
            Optional, string. The session associated with the image.
        aux_metadata:
            Optional, dict. Auxiliary metadata associated with the image.
        annotations:
            Optional, List of scenebox Annotation objects.
            Annotations associated with the image. Each item in the passed list must be of an object of the
            scenebox.models.annotation classes
    """
    def __init__(self,
                 id: Optional[str] = None,
                 path: Optional[str] = None,
                 url: Optional[str] = None,
                 uri: Optional[str] = None,
                 bytes: Optional[Union[io.BytesIO, bytes, str]] = None,
                 sensor: Optional[str] = None,
                 timestamp: Optional[Union[str, datetime]] = None,
                 session_uid: Optional[str] = None,
                 aux_metadata: Optional[dict] = None,
                 annotations: Optional[List[Annotation]] = None):
        self.annotations = annotations
        super(Image, self).__init__(id=id, path=path, url=url, uri=uri, bytes=bytes, sensor=sensor, timestamp=timestamp, session_uid=session_uid, aux_metadata=aux_metadata)
        self.image_post_init()

    def image_post_init(self):
        if self.annotations:
            for annotation in self.annotations:
                assert annotation.media_type == AssetsConstants.IMAGES_ASSET_ID


class Video(UnstructuredInputAsset):
    """Create a SceneBox Video asset.

        Parameters
        ----------
        id:
            Optional, string. An identifier that is unique for the video asset throughout SceneBox.
        path:
            String. The local path to the video to upload. If not None, url, uri,
            and bytes should all be None.
        url:
            String. The URL of the video to upload. Videos must be publicly available.
            If not None, url, uri, and path should all be None.
        uri:
            String. The URI of the video to upload. Can be from a private source.
            If not None, url, path, and bytes should all be None.
        bytes:
            io.BytesIO or bytes, string. The video bytes to upload.
            If not None, path, url, and uri should all be None.
        sensor:
            Optional, string. The sensor associated with the video.
        timestamp:
            Optional, either a string or a datetime. The time at which the video was taken.
        session_uid:
            Optional, string. The session associated with the video.
        aux_metadata:
            Optional, dict. Auxiliary metadata associated with the video.
        annotations:
            Optional, list of scenebox Annotation objects.
            Annotations associated with the video. Each item in the passed list must be of an object of the
            scenebox.models.annotation classes
        tags:
            Optional, list of strings. Labels associated with the video. Allows for easy video search.
        start_timestamp:
            Optional, either a string or a datetime. The time at which the video recording began.
    """
    def __init__(self,
                 id: Optional[str] = None,
                 path: Optional[str] = None,
                 url: Optional[str] = None,
                 uri: Optional[str] = None,
                 bytes: Optional[Union[io.BytesIO, bytes, str]] = None,
                 sensor: Optional[str] = None,
                 timestamp: Optional[Union[str, datetime]] = None,
                 session_uid: Optional[str] = None,
                 aux_metadata: Optional[dict] = None,
                 annotations: Optional[List[Annotation]] = None,
                 tags: Optional[List[str]] = None,
                 start_timestamp: Optional[Union[str, datetime]] = None
                 ):
        self.annotations = annotations
        self.tags = tags
        self.start_timestamp = start_timestamp
        super(Video, self).__init__(id=id, path=path, url=url, uri=uri, bytes=bytes, sensor=sensor, timestamp=timestamp, session_uid=session_uid, aux_metadata=aux_metadata)
        self.video_post_init()

    def video_post_init(self):
        if self.annotations:
            for annotation in self.annotations:
                assert annotation.media_type == AssetsConstants.VIDEOS_ASSET_ID
        if not self.start_timestamp:
            self.start_timestamp = self.timestamp
        else:
            self.timestamp = self.start_timestamp
        assert self.timestamp == self.start_timestamp


class Lidar(UnstructuredInputAsset):
    """Create a SceneBox Lidar asset.

        Parameters
        ----------
        id:
            Optional, string. An identifier that is unique for the lidar asset throughout SceneBox.
        path:
            String. The local path to the lidar to upload. If not None, url, uri,
            and bytes should all be None.
        url:
            String. The URL of the lidar to upload. Lidars must be publicly available.
            If not None, url, uri, and path should all be None.
        uri:
            String. The URI of the lidar to upload. Can be from a private source.
            If not None, url, path, and bytes should all be None.
        bytes:
            io.BytesIO or bytes, string. The lidar bytes to upload.
            If not None, path, url, and uri should all be None.
        sensor:
            Optional, string. The sensor associated with the lidar.
        timestamp:
            Optional, either a string or a datetime. The time at which the lidar was taken.
        session_uid:
            Optional, string. The session associated with the lidar.
        aux_metadata:
            Optional, dict. Auxiliary metadata associated with the lidar.
        format:
           The format in which the LIDAR was embedded. pcd|numpy|binary. Default is pcd. PCD files
           are expected to be valid. Support for binary files is experimental.
        binary_format:
            Optional, string. Experimental. For binary data, a decoder to decode each packet to
            x,y,z,intensity,epoch. Format should be compatible with struct
            (https://docs.python.org/3/library/struct.html) library.
        related_images:
            Optional, list of strings. Strings are the ids of the related images to be associated
            with the lidar scene.
        num_fields:
            Optional, int. The number of fields exists in LIDAR file to reshape numpy array for displaying.
            Required for numpy formats
    """
    def __init__(self,
                 id: Optional[str] = None,
                 path: Optional[str] = None,
                 url: Optional[str] = None,
                 uri: Optional[str] = None,
                 bytes: Optional[Union[io.BytesIO, bytes, str]] = None,
                 sensor: Optional[str] = None,
                 timestamp: Optional[Union[str, datetime]] = None,
                 session_uid: Optional[str] = None,
                 aux_metadata: Optional[dict] = None,
                 format: Optional[str] = None,
                 binary_format: Optional[str] = None,
                 related_images: Optional[List[str]] = None,
                 num_fields: Optional[int] = None
                 ):
        self.format = format
        self.binary_format = binary_format
        self.related_images = related_images
        self.num_fields = num_fields
        super(Lidar, self).__init__(id=id, path=path, url=url, uri=uri, bytes=bytes, sensor=sensor, timestamp=timestamp, session_uid=session_uid, aux_metadata=aux_metadata)
        self.lidar_post_init__()

    def lidar_post_init__(self):

        if not self.format:
            self.format = "pcd"
        if self.format == "numpy":
            assert self.num_fields, "num_fields is needed for numpy data"
        elif self.format == "binary":
            assert self.binary_format, "binary_format is needed for binary data"
        else:
            assert self.format == "pcd", "format should be pcd, numpy, or binary"

        if self.related_images:
            self.related_images = [standardize_name(_) for _ in self.related_images]


class Embedding(object):
    def __init__(self,
                 data: Union[io.BytesIO, bytes, np.array, List[Union[float, int]]],
                 asset_id: str,
                 asset_type: str = AssetsConstants.IMAGES_ASSET_ID,
                 model: str = "default",
                 version: str = "v1",
                 timestamp: Optional[Union[str, datetime]] = None,
                 layer: Optional[Union[int, str]] = None,
                 dtype: Optional[Union[type(np.float32), type(np.float64), type(float)]] = np.float32,
                 ndim: Optional[int] = None,
                 session_uid: Optional[str] = None
                 ):
        """Create an Embedding.

            Parameters
            ----------
            data:
                Embeddings data.
            model:
                The name of the embeddings model.  Helps to differentiate from other models.
            version:
                The version of the embeddings model.  Helps to differentiate several versions of the same model.
            asset_id:
                The asset ID associated with the embedding passed in `data`. Must refer to an asset ID available on
                SceneBox.
            asset_type:
                The type of the asset referred to in `asset_id`.  Currently, only images and objects are supported.
            timestamp:
                timestamp of the embeddings. if not provided, ingestion timestamp is used.
            layer:
                Layer associated with the embedding.
            dtype:
                The datatype of the embedding.  Helps to cast data.  If not listed, assumed to be `np.float32`.
            ndim:
                Number of dimensions in `data`.  Helps to assert that the dimension calculated by
                the platform is correct.  Raises an error of the calculated dimensions does not match this field.
                The largest embedding ndim supported is 8192.
            session_uid:
                The unique identifier of the session that the asset with asset_id belongs to.
        """

        if isinstance(data, io.BytesIO) or isinstance(data, bytes):
            # Enforce a cast to float32
            embedding_array = np.float32(np.frombuffer(data, dtype=dtype))
        elif isinstance(data, np.ndarray):
            embedding_array = np.float32(data)
        elif isinstance(data, list) and all([isinstance(datum, float) or isinstance(datum, int)
                                                   for datum in data]):
            embedding_array = np.float32(np.array(data))
        else:
            raise NotImplementedError("Supported data types are io.BytesIO, bytes, np.array, List[float]")

        if embedding_array.size <= 0:
            raise EmbeddingError("no embedding bytes were detected")

        self.ndim = embedding_array.reshape(1, -1).shape[1]
        if self.ndim <= 0:
            raise EmbeddingError("dimension of the embedding = {}. Must be a positive integer".format(self.ndim))

        if self.ndim > AssetIngestionLimits.MAX_EMBEDDINGS_NDIM:
            raise EmbeddingError("Embedding dimensions should be no more than {}".format(
                AssetIngestionLimits.MAX_EMBEDDINGS_NDIM))

        if not asset_id:
            raise ValueError("cannot create an embedding without an asset id")

        if ndim and self.ndim != ndim:
            raise EmbeddingError("ndim passed {} does not match the ndim in data {}".format(ndim, self.ndim))

        self.bytes = embedding_array.tobytes()
        self.embedding_array = embedding_array
        self.timestamp = timestamp or datetime.utcnow()
        assert_standardized(asset_id)  # remove in the future
        self.asset_id = standardize_name(asset_id)
        self.asset_type = asset_type
        self.model = model
        self.version = version
        self.layer = layer

        json_object_for_embedding_id = {
            'model': self.model,
            'version': self.version,
            'asset_id': self.asset_id,
            'ndim': self.ndim,
            'layer': self.layer}

        embeddings_hash = get_md5_from_json_object(json_object=json_object_for_embedding_id)
        self.id = str(hash_string_into_positive_integer_reproducible(embeddings_hash))
        self.metadata = {
                'id': self.id,
                'timestamp': self.timestamp,
                'tags': [self.layer] if self.layer else [],
                'media_type': self.asset_type,
                'asset_id': self.asset_id,
                'model': self.model,
                'version': self.version,
                'ndim': self.ndim,
                'index_name': get_similarity_index_name(
                    media_type=self.asset_type,
                    model=self.model,
                    version=self.version)}
        if session_uid:
            self.metadata["session_uid"] = session_uid

    def get_nparray(self) -> np.array:
        return self.embedding_array


@dataclass(frozen=False)
class TemplateOperation:
    """A unit of the pipeline used to define a template task in a campaign

        Parameters
        ----------
        operation_id:
            String. Unique string identifier for an operation chosen from the list of valid operations.

        task_step:
            Integer. Which step of the task to add this unit to.

        config_id:
            String. A unique identifier of a saved configuration for this operation.

        config:
            Dict. A dictionary that conforms to the config schema for this operation.
    """
    operation_id: str = None
    task_step: int = 0
    config_id: Optional[str] = None
    config: Optional[dict] = None

    def __post_init__(self):
        # Validate inputs
        assert self.operation_id
        assert self.task_step is not None
        # Exor operation. Only one of self.config or self.config_id is to be set
        assert ((self.config_id and not self.config) or (not self.config_id and self.config))

