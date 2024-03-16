#  Copyright (c) 2020 Caliber Data Labs.
#  All rights reserved.
#
import io
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple

import numpy as np

from ..constants import (AnnotationMediaTypes, AnnotationTypes, AssetsConstants, AnnotationGroups,
                         AnnotationProviders, AssetIngestionLimits)
from ..custom_exceptions import InvalidAnnotationError
from ..tools import misc, time_utils
from ..tools.logger import get_logger
from .object_access import ObjectAccess
from ..tools.misc import get_md5_from_string, rotate_2d
from ..tools.naming import standardize_name

logger = get_logger(__name__)


class StructuredAnnotationEntity:
    """

        Attributes
        ----------
        uid:
            Optional. A unique id for the annotation entity. If not provided, scenebox
            will assign a guid to the entity.
        label:
            Name of the point.
        confidence:
            Labelling confidence. Must be between 0 and 1.
        attributes:
            Additional point metadata.
    """
    def __init__(self,
                 label: str = None,
                 uid: Optional[str] = None,
                 confidence: Optional[float] = None,
                 attributes: Optional[dict] = None
                 ):

        self.label = label
        self.uid = uid
        self.confidence = confidence
        self.attributes = attributes
        self.post_init()

    def post_init(self):
        # Validate inputs
        if self.confidence:
            assert 0 <= self.confidence <= 1, "Incorrect confidence value. Must be in range [0, 1]"


class Point(StructuredAnnotationEntity):
    """Holds the coordinates and metadata of a single keypoint.

        Several Points can be compiled together to form a PointAnnotation. Specifying a list of Points is also
        necessary to create a Pose.

        Attributes
        ----------
        left:
            x coordinate of the point. Must be positive.
        top:
            y coordinate of the point. Must be positive.
        label:
            Name of the point.
        category_id:
            Label category ID.
        confidence:
            Labelling confidence. Must be between 0 and 1.
        geometry:
            If available should be "point".
        attributes:
            Additional point metadata.
    """
    def __init__(self,
                 label: str = None,
                 uid: Optional[str] = None,
                 confidence: Optional[float] = None,
                 attributes: Optional[dict] = None,
                 left: float = None,
                 top: float = None,
                 category_id: Optional[int] = None,
                 geometry: Optional[str] = None
                 ):
        self.left = left
        self.top = top
        self.category_id = category_id
        self.geometry = geometry
        super(Point, self).__init__(label=label, uid=uid, confidence=confidence, attributes=attributes)
        self.point_post_init()

    def point_post_init(self):
        assert self.left is not None, "left cannot be None"
        assert self.top is not None, "top cannot be None"
        assert self.label, "Label string required"
        assert all(x >= 0 for x in [self.left, self.top]), "Coordinates need to be non-negative"

    def to_dic(self):
        """
        return a dictionary object representative of Point
        :return: dictionary object
        """
        return {
            "label": self.label,
            "uid": self.uid,
            "confidence": self.confidence,
            "attributes": self.attributes,
            "left": self.left,
            "top": self.top,
            "category_id": self.category_id,
            "geometry": self.geometry
        }


class BoundingBox(StructuredAnnotationEntity):
    """Holds the coordinates and metadata of a single bounding box.

       Several BoundingBoxes can be compiled together to form a BoundingBoxAnnotation.

       Attributes
       ----------
       x_min:
           Minimum bounding box x coordinate. Must be a positive value.
       x_max:
           Maximum bounding box x coordinate. Must be a positive value.
       y_min:
           Minimum bounding box y coordinate. Must be a positive value.
       y_max:
           Maximum bounding box y coordinate. Must be a positive value.
       label:
           Name of the region encapsulated by the bounding box.
       category_id:
           Label category ID.
       confidence:
           Labelling confidence. Must be between 0 and 1.
       attributes:
           Additional bounding box metadata.
     """
    def __init__(self,
                 label: str = None,
                 uid: Optional[str] = None,
                 confidence: Optional[float] = None,
                 attributes: Optional[dict] = None,
                 x_min: float = None,
                 x_max: float = None,
                 y_min: float = None,
                 y_max: float = None,
                 category_id: Optional[int] = None
                 ):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.category_id = category_id
        super(BoundingBox, self).__init__(label=label, uid=uid, confidence=confidence, attributes=attributes)
        self.boundingbox_post_init()

    def boundingbox_post_init(self):
        # Validate inputs
        assert self.x_min is not None, "x_min cannot be None"
        assert self.x_max is not None, "x_max cannot be None"
        assert self.y_min is not None, "y_min cannot be None"
        assert self.y_max is not None, "y_max cannot be None"

        assert all(x >= 0 for x in [self.x_min, self.x_max, self.y_min, self.y_max]), "Coordinates need " \
                                                                                      "to be non-negative"
        assert self.x_max >= self.x_min
        assert self.y_max >= self.y_min
        assert self.label, "Label string required"


class Polygon(StructuredAnnotationEntity):
    """Holds the coordinates and metadata of a single Polygon.

        Several Polygons can be compiled together to form a PolygonAnnotation.

        Attributes
        ----------
        coordinates:
            An ordered list of each coordinate inside the polygon.  Each coordinate must be provided in the form
            (x, y). Every x, y value must be positive. Connections are assumed between consecutive coordinates.
        label:
            Name of the region encapsulated by the polygon.
        category_id:
            Label category ID.
        confidence:
            Labelling confidence. Must be between 0 and 1.
        attributes:
            Additional polygon metadata.
      """
    def __init__(self,
                 label: str = None,
                 uid: Optional[str] = None,
                 confidence: Optional[float] = None,
                 attributes: Optional[dict] = None,
                 coordinates: List[Tuple[float, float]] = None,
                 category_id: Optional[int] = None
                 ):
        self.coordinates = coordinates
        self.category_id = category_id
        super(Polygon, self).__init__(label=label, uid=uid, confidence=confidence, attributes=attributes)
        self.polygon_post_init()

    def polygon_post_init(self):
        # Validate inputs
        assert self.coordinates, "Coordinates cannot be None"
        assert all(x >= 0 and y >= 0 for (x, y) in self.coordinates), "Coordinates need to be non-negative"
        assert self.label, "Label string required"
        assert len(self.coordinates) <= AssetIngestionLimits.MAX_POLYGON_COORDINATES, "A polygon object " \
               "can have no more than {} vertices".format(AssetIngestionLimits.MAX_POLYGON_COORDINATES)


class Line(StructuredAnnotationEntity):
    """Holds the coordinates and metadata of a single Line.

        Several Lines can be compiled together to form a Line annotation.

        Attributes
        ----------
        coordinates:
            An ordered list of each coordinate inside the line.  Each coordinate must be provided in the form
            (x, y). Every x, y value must be positive. Connections are assumed between consecutive coordinates.
        label:
            Name of the region highlighted with the Line.
        complete:
            If True, denotes that the annotation is complete.  Otherwise, categorizes the annotation as incomplete.
        category_id:
            Label category ID.
        confidence:
            Labelling confidence.  Must be between 0 and 1.
        attributes:
            Additional line metadata.
    """
    def __init__(self,
                 label: str = None,
                 uid: Optional[str] = None,
                 confidence: Optional[float] = None,
                 attributes: Optional[dict] = None,
                 coordinates: List[Tuple[float, float]] = None,
                 complete: Optional[bool] = False,
                 category_id: Optional[int] = None
                 ):
        self.coordinates = coordinates
        self.complete = complete
        self.category_id = category_id
        super(Line, self).__init__(label=label, uid=uid, confidence=confidence, attributes=attributes)
        self.line_post_init_()

    def line_post_init_(self):
        # Validate inputs
        assert self.coordinates, "Coordinates cannot be None"
        assert all(x >= 0 and y >= 0 for (x, y) in self.coordinates), "Coordinates need to be non-negative"
        assert self.label, "Label string required"
        assert len(self.coordinates) <= AssetIngestionLimits.MAX_LINE_COORDINATES, "A line object " \
            "can have no more than {} line endpoint tuples".format(AssetIngestionLimits.MAX_LINE_COORDINATES)


class Label:
    """Holds the coordinates and metadata of a Label.

        Several Labels can be compiled together to form a ClassificationAnnotation.

        Attributes
        ----------
        label:
            Name of the labelled region.
        class_name:
            Name of the class that the label belongs to.
        category_id:
            Label category ID.
        confidence:
            Labelling confidence.  Must be between 0 and 1.
    """
    def __init__(self,
                 label: str,
                 class_name: Optional[str] = None,
                 category_id: Optional[int] = None,
                 confidence: Optional[float] = None
                 ):

        self.label = label
        self.class_name = class_name
        self.category_id = category_id
        self.confidence = confidence
        self.post_init()

    def post_init(self):
        # Validate inputs
        assert self.label, "Label string required"
        if self.confidence:
            assert 0 <= self.confidence <= 1, "Incorrect confidence value. Must be in range [0, 1]"


class Connection:
    """Specifies the starting/ending indices of connected keypoints of a single Pose. Only to be used when creating
    pose annotations.

        Poses have a class attribute named ``keypoints``: a list of coordinates. To form Pose annotations, the connections
        between these keypoints must be specified. Each Connection class instance represents a connection between the
        keypoint at position ``start_index`` and position ``end_index`` in the ``keypoints`` list.

    Attributes
    ----------
    start_index:
        The list index in the Pose attribute ``keypoints`` where the connection starts.
    end_index:
        The list index in the Pose attribute ``keypoints`` where the connection ends.
    confidence:
        Labelling confidence.  Must be between 0 and 1.
    """
    def __init__(self,
                 start_index: int,
                 end_index: int,
                 confidence: Optional[float] = None
                 ):
        self.start_index = start_index
        self.end_index = end_index
        self.confidence = confidence
        self.post_init()

    def post_init(self):
        # Validate inputs
        if self.confidence:
            assert 0 <= self.confidence <= 1, "Incorrect confidence value. Must be in range [0, 1]"

    def to_dic(self):
        return {
            "start_index": self.start_index,
            "end_index": self.end_index,
            "confidence": self.confidence
        }


class Pose:
    """Holds the coordinates and metadata of a Pose.

        Several Poses can be compiled together to form a PoseAnnotation.

        Attributes
        ----------
        label:
            Name of the pose.
        keypoints:
            All Points contained in the pose.
        connections:
            Defines the directed connections between the Points (coordinates) specified in ``keypoints``.
        attributes:
            Additional pose metadata.
        """
    def __init__(self,
                 label: str,
                 keypoints: List[Point],
                 connections: List[Connection],
                 attributes: Optional[dict] = None
                 ):
        self.label = label
        self.keypoints = keypoints
        self.connections = connections
        self.attributes = attributes
        self.post_init()

    def post_init(self):
        # Validate inputs
        assert len(self.keypoints) <= AssetIngestionLimits.MAX_POSE_KEYPOINTS, "A pose object" \
            "can have no more than {} keypoints".format(AssetIngestionLimits.MAX_POSE_KEYPOINTS)
        assert len(self.connections) <= AssetIngestionLimits.MAX_POSE_CONNECTIONS, "A pose object" \
            "can have no more than {} connection".format(AssetIngestionLimits.MAX_POSE_CONNECTIONS)

        for conn in self.connections:
            if not(0 <= conn.start_index <= len(self.keypoints)):
                raise AssertionError("Start index for connection {} is "
                                     "out of range".format(conn))
            if not(0 <= conn.end_index <= len(self.keypoints)):
                raise AssertionError("End index for connection {} is "
                                     "out of range".format(conn))


class Cuboid2D(StructuredAnnotationEntity):
    """Holds the coordinates and metadata of a Cuboid in two-dimensions.

        Several Cuboids can be compiled together to form a Cuboid2DAnnotation.  Cuboids are made
        of two squares specifying the front and back of the object. Connecting lines are
        drawn between the vertices of the squares to form a cuboid.

           (tl2)---------o(tr2)
          /|............./|
         /.|............/.|
        o(tl1)---------o(tr1)
        |..o(bl2)------|--o(br2)
        |./............|./
        |/.............|/
        o(bl1)--------o(br1)

        Attributes
        ----------
        tl1:
            Top left coordinate of the front square.
        bl1:
            Bottom left coordinate of the front square.
        tr1:
            Top right coordinate of the front square.
        br1:
            Bottom right coordinate of the front square.
        tl2:
            Top left coordinate of the back square.
        bl2:
            Bottom left coordinate of the back square.
        tr2:
            Top right coordinate of the back square.
        br2:
            Bottom right coordinate of the back square.
        label:
            Name of the cuboid.
        category_id:
            Label category ID.
        confidence:
            Labelling confidence.  Must be between 0 and 1.
        attributes:
            Additional cuboid metadata.
    """

    def __init__(self,
                 label: str = None,
                 uid: Optional[str] = None,
                 confidence: Optional[float] = None,
                 attributes: Optional[dict] = None,
                 tl1: Tuple[float, float] = None,
                 bl1: Tuple[float, float] = None,
                 tr1: Tuple[float, float] = None,
                 br1: Tuple[float, float] = None,
                 tl2: Tuple[float, float] = None,
                 bl2: Tuple[float, float] = None,
                 tr2: Tuple[float, float] = None,
                 br2: Tuple[float, float] = None,
                 category_id: Optional[int] = None
                 ):
        self.tl1 = tl1
        self.bl1 = bl1
        self.tr1 = tr1
        self.br1 = br1
        self.tl2 = tl2
        self.bl2 = bl2
        self.tr2 = tr2
        self.br2 = br2
        self.category_id = category_id
        super(Cuboid2D, self).__init__(label=label, uid=uid, confidence=confidence, attributes=attributes)
        self.post_init()

    def post_init(self):
        # Validate inputs
        assert self.tl1, "tl1 cannot be None"
        assert self.bl1, "bl1 cannot be None"
        assert self.tr1, "tr1 cannot be None"
        assert self.br1, "br1 cannot be None"
        assert self.tl2, "tl2 cannot be None"
        assert self.bl2, "bl2 cannot be None"
        assert self.tr2, "tr2 cannot be None"
        assert self.br2, "br2 cannot be None"
        assert self.label, "Label string required"


class Cuboid3D(StructuredAnnotationEntity):
    """Holds the coordinates and metadata of a Cuboid in three-dimension.

        Several Cuboids can be compiled together to form a Cuboid3DAnnotation.  Cuboids are made
        of two squares specifying the front and back of the object. Connecting lines are
        drawn between the vertices of the squares to form a cuboid.

           (tl2)---------o(tr2)
          /|............./|
         /.|............/.|
        o(tl1)---------o(tr1)
        |..o(bl2)------|--o(br2)
        |./............|./
        |/.............|/
        o(bl1)--------o(br1)

        Attributes
        ----------
        tl1:
            Top left coordinate of the front square.
        bl1:
            Bottom left coordinate of the front square.
        tr1:
            Top right coordinate of the front square.
        br1:
            Bottom right coordinate of the front square.
        tl2:
            Top left coordinate of the back square.
        bl2:
            Bottom left coordinate of the back square.
        tr2:
            Top right coordinate of the back square.
        br2:
            Bottom right coordinate of the back square.
        label:
            Name of the cuboid.
        category_id:
            Label category ID.
        confidence:
            Labelling confidence.  Must be between 0 and 1.
        attributes:
            Additional cuboid metadata.
    """
    def __init__(self,
                 label: str = None,
                 uid: Optional[str] = None,
                 confidence: Optional[float] = None,
                 attributes: Optional[dict] = None,
                 tl1: Tuple[float, float, float] = None,
                 bl1: Tuple[float, float, float] = None,
                 tr1: Tuple[float, float, float] = None,
                 br1: Tuple[float, float, float] = None,
                 tl2: Tuple[float, float, float] = None,
                 bl2: Tuple[float, float, float] = None,
                 tr2: Tuple[float, float, float] = None,
                 br2: Tuple[float, float, float] = None,
                 category_id: Optional[int] = None
                 ):
        self.tl1 = tl1
        self.bl1 = bl1
        self.tr1 = tr1
        self.br1 = br1
        self.tl2 = tl2
        self.bl2 = bl2
        self.tr2 = tr2
        self.br2 = br2
        self.category_id = category_id
        super(Cuboid3D, self).__init__(label=label, uid=uid, confidence=confidence, attributes=attributes)
        self.cuboid3d_post_init()

    def cuboid3d_post_init(self):
        # Validate inputs
        assert self.tl1, "tl1 cannot be None"
        assert self.bl1, "bl1 cannot be None"
        assert self.tr1, "tr1 cannot be None"
        assert self.br1, "br1 cannot be None"
        assert self.tl2, "tl2 cannot be None"
        assert self.bl2, "bl2 cannot be None"
        assert self.tr2, "tr2 cannot be None"
        assert self.br2, "br2 cannot be None"
        assert self.label, "Label string required"


class Ellipse(StructuredAnnotationEntity):
    """Annotation model for a single Ellipse. Several such Ellipse objects can be compiled
       together in a list to form a EllipseAnnotation.

       Attributes
       ----------
       centre_x:
           X-axis coordinate for the centre. Must be a positive value.
       centre_y:
           Y-axis coordinate for the centre. Must be a positive value.
       radius_x:
           Distance of the farthest point on the ellipse along the x-axis. Must be a positive value.
       radius_y:
           Distance of the farthest point on the ellipse along the y-axis. Must be a positive value.
       rotation:
           Angle of rotation with respect to the positive x-axis in degrees.
       label:
            A label for the ellipse.
       confidence:
           Labelling confidence. Must be between 0 and 1.
       attributes:
           Additional bounding box metadata.
     """
    def __init__(self,
                 label: str = None,
                 uid: Optional[str] = None,
                 confidence: Optional[float] = None,
                 attributes: Optional[dict] = None,
                 centre_x: float = None,
                 centre_y: float = None,
                 radius_x: float = None,
                 radius_y: float = None,
                 rotation: float = None):
        self.centre_x = centre_x
        self.centre_y = centre_y
        self.radius_x = radius_x
        self.radius_y = radius_y
        self.rotation = rotation
        super(Ellipse, self).__init__(label=label, uid=uid, confidence=confidence, attributes=attributes)
        self.ellipse_post_init()

    def ellipse_post_init(self):
        # Validate inputs
        assert self.centre_x is not None, "centre_x cannot be None"
        assert self.centre_y is not None, "centre_y cannot be None"
        assert self.radius_x is not None, "radius_x cannot be None"
        assert self.radius_y is not None, "radius_y cannot be None"

        assert all(x >= 0 for x in [self.radius_x, self.radius_y]), "Ellipse radii" \
            " need to be non-negative."
        assert self.label, "Label string required"


class Annotation(object):
    def __init__(self, **kwargs):
        """Base annotation class. Inherited by all ``*Annotation`` classes.

            Only specify one of asset/image/video/lidar_id.

            Keyword Args
            ------------
            asset_id: Optional[str]
                ID of the existing asset to associate with the annotation.
            image_id: Optional[str]
                ID of the existing image to associate with the annotation.
            video_id: Optional[str]
                ID of the existing video to associate with the annotation.
            lidar_id: Optional[str]
                ID of the existing lidar to associate with the annotation.
            media_type: Optional[str]
                Media type (image, object, etc.) of the asset specified in ``asset/image/video/lidar_id``.  Choose from
                ``scenebox.constants.AnnotationMediaTypes.VALID_TYPES``.
            annotation_type: Optional[str]
                Annotation type (bounding box, polygon, etc.). Choose from
                ``scenebox.constants.AnnotationTypes.VALID_TYPES``.
            provider: Optional[str]
                The name of the annotation model or source.
            annotation_entities: Optional[AnnotationEntity]
                Annotation objects. Not necessary to fill when using the Point/PointAnnotation,
                BoundingBox/BoundingBoxAnnotation, etc. wrapper classes, and necessary otherwise.  Using this argument
                bypasses all argument validity pre-checks.
            annotation_meta: Optional[Dict[str, Any]]
                Any primary annotation metadata.
            sets: Optional[List[str]]
                Dataset IDs to associate with the annotation.
            session_uid: Optional[str]
                Session UID to associate with the annotation.
            sensor: Optional[str]
                The sensor with which the annotation was captured with.
            version: Optional[str]
                The annotation model version.
            annotation_group: Optional[str]
                The annotation source type (GT, Model, etc.) Choose from ``scenebox.constants.AnnotationGroups``.
            masks: Optional[Dict[str, ObjectAccess]]
                All mask ObjectAccess objects.  Helps SceneBox to access valid addresses for the mask image files.
            tags: Optional[List[str]]
                Any tags to associate with the annotation.
            frame: Optional[int]
                Video frame number associated with the annotation.  Must be specified if annotating video.
            aux: Optional[List[str]]
                Any auxiliary annotation metadata.
            raw_annotation_str: Optional[str]
                string payload of the raw annotation
            raw_annotation_json: Optional[JSON]
                json payload of the raw annotation
            raw_annotation_url: Optional[str]
                url of the raw annotation
            raw_annotation_uri: Optional[str]
                uri of the raw annotation
        """
        self.id: str = standardize_name(kwargs.get("id") or misc.get_guid())
        self.timestamp: datetime = kwargs.get("timestamp") or datetime.utcnow()

        self.asset_id: str = kwargs.get("asset_id") or kwargs.get("image_id") or \
                             kwargs.get("video_id") or kwargs.get("lidar_id")
        if not self.asset_id:
            raise InvalidAnnotationError("asset_id (image, video, lidar) should be specified")

        # assert_standardized(self.asset_id)  # remove in the future
        self.asset_id = standardize_name(self.asset_id)

        self.media_type: str = kwargs.get("media_type") or AssetsConstants.IMAGES_ASSET_ID
        if self.media_type not in AnnotationMediaTypes.VALID_TYPES:
            raise InvalidAnnotationError(
                "invalid annotation type {}".format(self.media_type)
            )

        self.annotation_type: str = kwargs.get("annotation_type")
        if self.annotation_type not in AnnotationTypes.VALID_TYPES:
            raise InvalidAnnotationError(
                "invalid annotation type {}".format(self.annotation_type)
            )

        self.provider: Optional[str] = kwargs.get("provider") or AnnotationProviders.DEFAULT_PROVIDER
        self.annotation_entities: List[AnnotationEntity] = kwargs.get("annotation_entities") or []
        self.annotation_meta: Dict = kwargs.get("annotation_meta") or {}
        self.sets: List[str] = kwargs.get("sets", [])
        if "set_id" in kwargs:
            self.sets.append(kwargs.get("set_id"))
        self.session_uid: Optional[str] = kwargs.get("session_uid")
        self.sensor: Optional[str] = kwargs.get("sensor")
        self.version: Optional[str] = kwargs.get("version")
        self.annotation_group: str = kwargs.get("annotation_group", AnnotationGroups.GROUND_TRUTH)
        self.masks: Dict[str, ObjectAccess] = kwargs.get("masks", {})
        self.tags: List[str] = kwargs.get("tags", [])
        self.frame: Optional[int] = kwargs.get("frame")
        self.label_status = kwargs.get("label_status")
        self.aux: Optional[List[str]] = kwargs.get("aux", [])
        self.raw_annotation_str = kwargs.get("raw_annotation_str")
        raw_annotation_json = kwargs.get("raw_annotation_json")
        self.raw_annotation_url = kwargs.get("raw_annotation_url")
        self.raw_annotation_uri = kwargs.get("raw_annotation_uri")
        if sum(_ is not None for _ in [self.raw_annotation_str,
                                       raw_annotation_json,
                                       self.raw_annotation_url,
                                       self.raw_annotation_uri]) > 1:
            raise InvalidAnnotationError("only one of raw_annotation_str, json, uri, or url should be specified")
        if raw_annotation_json is not None:
            self.raw_annotation_str = json.dumps(raw_annotation_json).encode('utf-8')
        if self.media_type in [AssetsConstants.VIDEOS_ASSET_ID] and self.frame is None:
            raise InvalidAnnotationError(
                "{} annotation need frame".format(self.media_type)
            )

    def finalize(self):
        self.set_annotation_entities()
        self.__sanity_check()

    def set_annotation_entities(self):
        pass

    def post_upload(self, annotations_amc, owner_organization_id: str):
        pass

    def __sanity_check(self):
        pass

    def to_dic(self):
        """
        return a dictionary object representative of Annotation
        :return: dictionary object
        """
        annotation_entities_ = []
        labels = set()
        for annotation_entity in self.annotation_entities:
            annotation_entities_.append(annotation_entity.to_dic())
            labels.add(annotation_entity.label)
        return {
            "session_uid": self.session_uid,
            "timestamp": time_utils.datetime_or_str_to_iso_utc(self.timestamp),
            "asset_id": self.asset_id,
            "media_type": self.media_type,
            "provider": self.provider,
            "annotation_type": self.annotation_type,
            "annotation_entities": annotation_entities_,
            "sets": self.sets,
            "labels": list(labels),
            "label_status": self.label_status,
            "sensor": self.sensor,
            "version": self.version,
            "annotation_group": self.annotation_group,
            "masks": {k: v.to_dic() for k, v in self.masks.items()},
            "frame": self.frame,
            "tags": self.tags,
            "aux": self.aux
        }


class RelatedAnnotation(object):
    # initialize a related annotation object(
    def __init__(self, related_annotation_dic):
        try:
            # annotation label
            self.uid = related_annotation_dic["uid"]

            # the unique (worldwide) id of the entity
            self.relationship = related_annotation_dic["relationship"]
            if self.relationship not in {"parent", "child", "sibling"}:
                raise InvalidAnnotationError(
                    "unrecognized relation {}".format(self.relationship)
                )

        except KeyError as e:
            raise InvalidAnnotationError(str(e))

    def to_dic(self):
        """
        return a dictionary object representative of Annotation entity
        :return: dictionary object
        """
        return {"uid": self.uid, "relationship": self.relationship}


class AnnotationEntity(object):

    def __init__(self,
                 label: str,
                 annotation_type: str,
                 class_name: Optional[str] = None,
                 coordinates: Optional[List] = None,
                 confidence: Optional[float] = None,
                 mask_color: Optional[str] = None,
                 mask_id: Optional[str] = None,
                 uid: Optional[str] = None,
                 category_id: Optional[int] = None,
                 related_annotations: Optional[List[RelatedAnnotation]] = None,
                 attributes: Optional[dict] = None,
                 mask_type: Optional[str] = None,
                 keypoints: Optional[List[Point]] = None,
                 connections: Optional[List[Connection]] = None):

        """Initialize a singular annotation entity (an annotation component such as a singular bounding box, polygon,
            etc.)

            Several annotation entities can be saved into the attributes of a single Annotation instance (either
            manually using the Annotation class, or automatically using any class that inherits Annotation such as
            BoundingBoxAnnotation/PolygonAnnotation/etc.). These entities appear on
            SceneBox under one provider/model as a union of all passed annotation entities.

            Parameters
            -----------
            label:
                Name of the point/region that the annotation highlights.
            annotation_type:
                Annotation type (bounding box, polygon, etc.). Choose from
                ``scenebox.constants.AnnotationTypes.VALID_TYPES``.
            class_name:
                Name of the class that the label belongs to.
            coordinates:
                An ordered list of each coordinate inside the annotation (if creating bounding box, polygon, line,
                etc.). Each coordinate must be provided in the form (x, y) for two-d annotations and (x, y, z) for
                three-d annotations. Connections are assumed between consecutive coordinates. For cuboid annotations,
                coordinate values are assumed to be world-normalized and can be negative. For point, line, polygon
                and bounding-box annotations, the coordinates need to be positive.
            confidence:
                Labelling confidence. Must be between 0 and 1.
            mask_color:
                If creating a mask/segmentation, represents the color of the mask region to be
                extracted in the mask source image.
            mask_id:
                If creating a mask/segmentation, represents the annotation ID to give to the mask
            uid:
                The globally unique ID to give to the annotation entity
            category_id:
                Label category ID.
            related_annotations:
                Any related annotations to the annotation.
            attributes:
                Optional auxiliary annotation entity attributes.
            mask_type:
                Denotes the mask image color scheme. There are two accepted mask color schemes: "MultiColor", or
                "SingleColor". A "MultiColor" mask image may contain several colors (and must include its respective
                mask_colors color). A "SingleColor" mask is transparent and white (White denotes mask region).
                All list entries must be "Multicolor" or "SingleColor".
            keypoints:
                If creating a Pose annotation, represents all Points contained in the pose.
            connections:
                Defines the directed connections between the Points (coordinates) specified in ``keypoints``.
        """
        # annotation label
        self.label = label
        self.category_id = category_id
        self.class_name = class_name
        if mask_color:
            self.mask_color = mask_color.lower()
            if not misc.is_valid_hex(self.mask_color):
                raise InvalidAnnotationError(
                    "invalid hex color {}".format(mask_color))
        else:
            self.mask_color = None

        # the unique (worldwide) id of the entity
        self.uid = standardize_name(uid) if uid else misc.get_guid()
        self.mask_id = mask_id

        if isinstance(confidence, float):
            self.confidence = confidence
            if self.confidence < 0 or self.confidence > 1:
                raise InvalidAnnotationError(
                    "confidence {} should be between 0 and 1".format(
                        self.confidence))
        elif confidence is None:
            self.confidence = None
        else:
            raise InvalidAnnotationError(
                "invalid confidence format {}".format(type(confidence))
            )

        if annotation_type not in AnnotationTypes.VALID_TYPES:
            raise InvalidAnnotationError(
                "invalid annotation type {}".format(annotation_type)
            )
        else:
            self.annotation_type = annotation_type

        # x, y coordinates
        self.coordinates = []

        for point in coordinates or []:
            if annotation_type == AnnotationTypes.THREE_D_CUBOID:
                self.coordinates.append(
                    {"x": float(point["x"]), "y": float(point["y"]), "z": float(point["z"])})
            else:
                self.coordinates.append(
                    {"x": float(point["x"]), "y": float(point["y"])})

        # coordinate checks for various geometry types:
        if self.annotation_type == AnnotationTypes.POINT and len(
                self.coordinates) != 1:
            raise InvalidAnnotationError(
                "point annotations should exactly have 1 point"
            )

        if self.annotation_type == AnnotationTypes.TWO_D_BOUNDING_BOX and len(
                self.coordinates) != 4:
            raise InvalidAnnotationError(
                "bounding_box annotations should exactly have 4 points"
            )

        if self.annotation_type in [AnnotationTypes.TWO_D_CUBOID, AnnotationTypes.THREE_D_CUBOID]\
                and len(self.coordinates) != 8:
            raise InvalidAnnotationError(
                "cuboid annotations should exactly have 8 points"
            )

        if self.annotation_type in {
                AnnotationTypes.POLYGON,
                AnnotationTypes.LINE} and not self.coordinates:
            raise InvalidAnnotationError(
                "empty coordinates for annotation_type = {}".format(
                    self.annotation_type))

        if self.annotation_type == AnnotationTypes.SEGMENTATION and not self.mask_color:
            raise InvalidAnnotationError(
                "mask color should be specified for segmentation"
            )

        # get all related_annotations
        self.related_annotations = []

        for related_annotation in related_annotations or []:
            self.related_annotations.append(
                RelatedAnnotation(related_annotation))

        # optional attributes of an entity
        self.attributes = attributes or {}

        self.mask_type = mask_type

        # composition makes sense for key point annotations only
        self.keypoints = keypoints or []
        if self.keypoints and self.annotation_type not in [AnnotationTypes.TWO_D_POSE]:
            raise InvalidAnnotationError("keypoints {} cannot be defined for {}".format(
                self.keypoints,
                self.annotation_type)
            )

        # Connections make sense for pose annotations and compositions only
        self.connections = connections or []
        if self.connections and not self.keypoints:
            raise InvalidAnnotationError("connections {} cannot be defined without "
                                         "keypoints".format(self.connections))

    def to_dic(self):
        """
        return a dictionary object representative of Annotation entity
        :return: dictionary object
        """
        related_annotations_ = []
        for related_annotation in self.related_annotations:
            related_annotations_.append(related_annotation.to_dic())

        dic = {
            "uid": self.uid,
            "label": self.label,
            "annotation_type": self.annotation_type,
            "attributes": self.attributes,
            "related_annotations": related_annotations_,
            "category_id": self.category_id,
        }
        if self.coordinates:
            dic["coordinates"] = self.coordinates
        if self.confidence:
            dic["confidence"] = self.confidence
        if self.mask_id:
            dic["mask_id"] = self.mask_id
        if self.mask_color:
            dic["mask_color"] = self.mask_color
        if self.class_name:
            dic["class_name"] = self.class_name
        if self.mask_type:
            dic["mask_type"] = self.mask_type
        if self.keypoints:
            kp_list = []
            for point in self.keypoints:
                kp_list.append(point.to_dic())
            dic["keypoints"] = kp_list
        if self.connections:
            conns_list = []
            for conn in self.connections:
                conns_list.append(conn.to_dic())
            dic["connections"] = conns_list
        return dic

    @classmethod
    def from_dict(cls, annotation_entity_dic: dict):

        confidence = annotation_entity_dic.get("confidence")
        if isinstance(confidence, float):
            if confidence < 0 or confidence > 1:
                raise InvalidAnnotationError(
                    "confidence {} should be between 0 and 1".format(
                        confidence))
        elif confidence is None:
            pass
        else:
            raise InvalidAnnotationError(
                "invalid confidence format {}".format(type(confidence))
            )

        coordinates = []

        try:
            for point in annotation_entity_dic.get("coordinates", []):
                coordinates.append(
                    {"x": float(point["x"]), "y": float(point["y"])})

        except KeyError:
            raise InvalidAnnotationError(str(KeyError))

        related_annotations = []
        for related_annotation in annotation_entity_dic.get(
                "related_annotations", []):
            related_annotations.append(RelatedAnnotation(related_annotation))

        keypoints = annotation_entity_dic.get("keypoints", [])
        keypoints_point_objects = []
        for point_dict in keypoints:
            keypoints_point_objects.append(Point(**point_dict))

        connections = annotation_entity_dic.get("connections", [])
        connections_objects = []
        for conn_dict in connections:
            connections_objects.append(Connection(**conn_dict))

        return cls(
            label=annotation_entity_dic["label"],
            category_id=annotation_entity_dic.get(
                "category_id"),
            uid=annotation_entity_dic.get("uid", misc.get_guid()),
            annotation_type=annotation_entity_dic["annotation_type"],
            mask_id=annotation_entity_dic.get("mask_id"),
            confidence=confidence,
            mask_color=annotation_entity_dic.get("mask_color"),
            mask_type=annotation_entity_dic.get("mask_type"),
            coordinates=coordinates,
            attributes=annotation_entity_dic.get("attributes"),
            class_name=annotation_entity_dic.get("class_name"),
            related_annotations=related_annotations,
            keypoints=keypoints,
            connections=connections,
        )

# TODO replace image_id with asset_id in all annotation classes


class SegmentationAnnotation(Annotation):
    def __init__(self,
                 labels: List[str],
                 mask_colors: List[str],
                 mask_urls: Optional[List[str]] = None,
                 mask_uris: Optional[List[str]] = None,
                 mask_file_paths: Optional[List[str]] = None,
                 mask_ids: Optional[List[str]] = None,
                 mask_types: Optional[List[str]] = None,
                 confidences: Optional[List[float]] = None,
                 attributes_list: Optional[List[dict]] = None,
                 **kwargs
                 ):
        """Create a Segmentation annotation.

            Mask segments are automatically extracted from the provided mask images (each containing colored segments)
            supplied in mask_url/uri/file_paths. Mask attributes are interpreted in the order passed (the first label
            listed in``labels`` is associated with the first mask color listed in ``mask_colors``, etc.)

            Parameters
            ----------
            labels:
                Names of each of the segmented regions.
            mask_colors:
                Colors of the segmented regions. Colors must be represented in hex format.
            mask_urls:
                URLs of the mask images. Each mask must contain its associated color listed in mask_colors.
            mask_uris:
                URIs of the mask images. Each mask must contain its associated color listed in mask_colors.
            mask_file_paths:
                Filepaths of the mask images. Each mask must contain its associated color listed in mask_colors.
            mask_ids:
                IDs to give to the generated masks.
            mask_types:
                Denotes the mask image color scheme. There are two accepted mask color schemes: "MultiColor", or
                "SingleColor". A "MultiColor" mask image may contain several colors (but must include its respective
                mask_colors color - these areas denote the mask region). A "SingleColor" mask only contains transparent
                and white colors (White areas denote the mask region).
                All entries of this list must be either "Multicolor" or "SingleColor".
            confidences:
                Labelling confidence.  Must be between 0 and 1.
            attributes_list:
                List of attributes
            **kwargs:
                Additional annotation attributes.  The keyword arguments are passed to ``scenebox.models.annotation``.
        """
        super().__init__(annotation_type=AnnotationTypes.SEGMENTATION, **kwargs)
        self.labels = labels
        self.mask_urls = mask_urls or [None] * len(labels)
        self.mask_uris = mask_uris or [None] * len(labels)
        self.mask_ids = mask_ids or [None] * len(labels)
        self.mask_file_paths = mask_file_paths or [None] * len(labels)
        self.mask_colors = mask_colors
        self.mask_types = mask_types or [None] * len(labels)
        self.confidences = confidences or [None] * len(labels)
        self.attributes_list = attributes_list or [None] * len(labels)
        self.mask_id_path_map = {}
        self.finalize()

    def post_upload(self, annotations_amc, owner_organization_id: str):
        for mask_id, mask_file_path in self.mask_id_path_map.items():
            with open(mask_file_path, 'rb') as f:
                file_obj = io.BytesIO(f.read())
            object_access = annotations_amc.put_file(
                id=mask_id,
                file_object=file_obj,
                owner_organization_id=owner_organization_id,
                content_type="image/png"
            )
            self.masks[mask_id] = object_access

    def set_annotation_entities(self):
        self.annotation_entities = []
        assert len(self.labels) == len(self.mask_urls)
        assert len(self.labels) == len(self.confidences)
        assert len(self.labels) == len(self.mask_colors)
        assert len(self.labels) == len(self.mask_uris)
        assert len(self.labels) == len(self.mask_file_paths)
        assert len(self.labels) == len(self.mask_ids)
        assert len(self.labels) == len(self.mask_types)
        masks = {}
        for label, url, confidence, mask_color, uri, mask_id, mask_file_path, mask_type, attributes in zip(
                self.labels, self.mask_urls, self.confidences, self.mask_colors, self.mask_uris,
                self.mask_ids, self.mask_file_paths, self.mask_types, self.attributes_list):
            if url:
                mask_id = mask_id or str(get_md5_from_string(url)).replace('-', '_')
                object_access = ObjectAccess(url=url)
            elif uri:
                mask_id = mask_id or str(get_md5_from_string(uri)).replace('-', '_')
                object_access = ObjectAccess(uri=uri)
            elif mask_file_path:
                mask_id = mask_id or str(get_md5_from_string(mask_file_path)).replace('-', '_')
                self.mask_id_path_map[mask_id] = mask_file_path
                object_access = None
            else:
                raise InvalidAnnotationError(
                    "either url or uri or mask file path should be specified for {}".format(
                        self.id))
            if not mask_id:
                mask_id = misc.get_guid()
            masks[mask_id] = object_access
            self.annotation_entities.append(
                AnnotationEntity(
                    label=label,
                    annotation_type=AnnotationTypes.SEGMENTATION,
                    mask_id=mask_id,
                    confidence=confidence,
                    mask_color=mask_color,
                    mask_type=mask_type or "MultiColor",
                    attributes=attributes
                )
            )
        self.masks = masks


class BoundingBoxAnnotation(Annotation):
    def __init__(self, bounding_boxes: List[BoundingBox], **kwargs):
        """Create a Bounding Box annotation.

            Created from a union of one or more BoundingBoxes.

            Parameters
            ----------
            bounding_boxes:
                All BoundingBoxes to include in the BoundingBoxAnnotation.
            **kwargs:
                Additional annotation attributes.  The keyword arguments are passed to ``scenebox.models.annotation``.
        """
        super().__init__(annotation_type=AnnotationTypes.TWO_D_BOUNDING_BOX, **kwargs)
        self.bounding_boxes = bounding_boxes
        self.finalize()

    def set_annotation_entities(self):
        self.annotation_entities = []

        if not isinstance(self.bounding_boxes, list):
            raise InvalidAnnotationError(
                "bounding box annotation is expected to be list"
            )

        for bounding_box in self.bounding_boxes:
            if bounding_box.attributes:
                assert isinstance(bounding_box.attributes, dict), \
                    "attributes should be of type dict {} provided".format(type(bounding_box.attributes))
            if bounding_box.attributes:
                if bounding_box.attributes.get("track_id"):
                    assert isinstance(bounding_box.attributes["track_id"], int), \
                        "track_id should be of type int {} provided".format(type(bounding_box.attributes["track_id"]))
            try:
                category_id = bounding_box.category_id
                left = float(bounding_box.x_min)
                top = float(bounding_box.y_max)
                bottom = float(bounding_box.y_min)
                right = float(bounding_box.x_max)
            except KeyError as e:
                raise InvalidAnnotationError(str(e))

            coordinates = [
                {"x": left, "y": bottom},
                {"x": right, "y": bottom},
                {"x": right, "y": top},
                {"x": left, "y": top},
            ]
            self.annotation_entities.append(
                AnnotationEntity(
                    label=bounding_box.label,
                    category_id=category_id,
                    annotation_type=AnnotationTypes.TWO_D_BOUNDING_BOX,
                    coordinates=coordinates,
                    confidence=bounding_box.confidence,
                    attributes=bounding_box.attributes,
                    uid=bounding_box.uid
                )
            )


class EllipseAnnotation(Annotation):
    def __init__(self, ellipses: List[Ellipse], **kwargs):
        """Create an Ellipse  annotation.

            Created from a union of one or more Ellipse objects.

            Parameters
            ----------
            ellipses:
                All Ellipses to include in the EllipseAnnotation.
            **kwargs:
                Additional annotation attributes. The keyword arguments are passed to ``scenebox.models.annotation``.
        """
        super().__init__(annotation_type=AnnotationTypes.ELLIPSE, **kwargs)
        self.ellipses = ellipses
        self.finalize()

    def set_annotation_entities(self):
        self.annotation_entities = []

        if not isinstance(self.ellipses, list):
            raise InvalidAnnotationError(
                "ellipses are expected to be provided in a list"
            )

        for ellipse in self.ellipses:
            if ellipse.attributes:
                assert isinstance(ellipse.attributes, dict), \
                    "attributes should be of type dict {} provided".format(type(ellipse.attributes))
            try:
                centre_x = float(ellipse.centre_x)
                centre_y = float(ellipse.centre_y)
                radius_x = float(ellipse.radius_x)
                radius_y = float(ellipse.radius_y)
                rotation = float(ellipse.rotation)
            except KeyError as e:
                raise InvalidAnnotationError(str(e))

            # Four extreme coordinates oriented along x-axis clockwise in 3D centred at origin
            coordinates = [[radius_x, 0],
                           [0, radius_y],
                           [-radius_x, 0],
                           [0, -radius_y]]
            coordinates = np.asarray(coordinates)
            rotated_coordinates = rotate_2d(coordinates=coordinates, angle=rotation, degrees=True)

            # Do translation
            rotated_coordinates[:, 0] = rotated_coordinates[:, 0] + centre_x
            rotated_coordinates[:, 1] = rotated_coordinates[:, 1] + centre_y
            coordinates[:, 0] = coordinates[:, 0] + centre_x
            coordinates[:, 1] = coordinates[:, 1] + centre_y

            # rotated_coordinates = np.round(rotate(coordinates, angle=rotation))
            coordinates = [
                {"x": rotated_coordinates[0][0], "y": rotated_coordinates[0][1]},
                {"x": rotated_coordinates[1][0], "y": rotated_coordinates[1][1]},
                {"x": rotated_coordinates[2][0], "y": rotated_coordinates[2][1]},
                {"x": rotated_coordinates[3][0], "y": rotated_coordinates[3][1]},
            ]

            self.annotation_entities.append(
                AnnotationEntity(
                    label=ellipse.label,
                    annotation_type=AnnotationTypes.ELLIPSE,
                    coordinates=coordinates,
                    confidence=ellipse.confidence,
                    attributes=ellipse.attributes,
                    uid=ellipse.uid
                )
            )


class PolygonAnnotation(Annotation):
    def __init__(self, polygons: List[Polygon], **kwargs):
        """Create a Polygon annotation.

            Created from a union of one or more Polygons.

            Parameters
            ----------
            polygons:
                All Polygons to include in the PolygonAnnotation.
            **kwargs:
                Additional annotation attributes.  The keyword arguments are passed to ``scenebox.models.annotation``.
        """
        super().__init__(annotation_type=AnnotationTypes.POLYGON, **kwargs)
        self.polygons = polygons
        self.finalize()

    def set_annotation_entities(self):
        self.annotation_entities = []

        if not isinstance(self.polygons, list):
            raise InvalidAnnotationError(
                "polygon annotation is expected to be list"
            )

        for polygon in self.polygons:
            try:
                category_id = polygon.category_id
                coords_ = polygon.coordinates
            except KeyError as e:
                raise InvalidAnnotationError(str(e))

            coordinates = []
            for c in coords_:
                coordinates.append({"x": c[0], "y": c[1]})
            self.annotation_entities.append(
                AnnotationEntity(
                    label=polygon.label,
                    category_id=category_id,
                    annotation_type=AnnotationTypes.POLYGON,
                    coordinates=coordinates,
                    confidence=polygon.confidence,
                    attributes=polygon.attributes
                )
            )


class PointAnnotation(Annotation):
    def __init__(self, points: List[Point], **kwargs):
        """Create a Point annotation.

            Created from a union of one or more Points.

            Parameters
            ----------
            polygons:
                All Points to include in the PointAnnotation.
            **kwargs:
                Additional annotation attributes.  The keyword arguments are passed to ``scenebox.models.annotation``.
        """
        super().__init__(annotation_type=AnnotationTypes.POINT, **kwargs)
        self.points = points
        self.finalize()

    def set_annotation_entities(self):
        self.annotation_entities = []

        if not isinstance(self.points, list):
            raise InvalidAnnotationError(
                "point annotation is expected to be list"
            )

        for point in self.points:
            try:
                category_id = point.category_id
                left = float(point.left)
                top = float(point.top)

            except KeyError as e:
                raise InvalidAnnotationError(str(e))

            coordinates = [
                {"x": left, "y": top}
            ]

            self.annotation_entities.append(
                AnnotationEntity(
                    label=point.label,
                    category_id=category_id,
                    annotation_type=AnnotationTypes.POINT,
                    coordinates=coordinates,
                    confidence=point.confidence,
                    attributes=point.attributes
                )
            )


class LineAnnotation(Annotation):
    def __init__(self, lines: List[Line], **kwargs):
        """Create a Line annotation.

            Created from a union of one or more Lines.

            Parameters
            ----------
            lines:
                All Lines to include in the LineAnnotation.
            **kwargs:
                Additional annotation attributes.  The keyword arguments are passed to ``scenebox.models.annotation``.
        """
        super().__init__(annotation_type=AnnotationTypes.LINE, **kwargs)
        self.lines = lines
        self.finalize()

    def set_annotation_entities(self):
        self.annotation_entities = []

        if not isinstance(self.lines, list):
            raise InvalidAnnotationError(
                "line annotation is expected to be list"
            )

        for line in self.lines:
            try:
                category_id = line.category_id
                coords_ = line.coordinates
            except KeyError as e:
                raise InvalidAnnotationError(str(e))

            coordinates = []
            for c in coords_:
                coordinates.append({"x": c[0], "y": c[1]})

            self.annotation_entities.append(
                AnnotationEntity(
                    label=line.label,
                    category_id=category_id,
                    annotation_type=AnnotationTypes.LINE,
                    coordinates=coordinates,
                    confidence=line.confidence,
                    attributes=line.attributes
                )
            )


class ClassificationAnnotation(Annotation):
    def __init__(self, labels: List[Label], **kwargs):
        """Create a Classification annotation.

            Created from a union of one or more Labels.

            Parameters
            ----------
            labels:
                All Labels to include in the ClassificationAnnotation.
            **kwargs:
                Additional annotation attributes.  The keyword arguments are passed to ``scenebox.models.annotation``.
        """
        super().__init__(annotation_type=AnnotationTypes.CLASSIFICATION, **kwargs)
        self.labels = labels
        self.finalize()

    def set_annotation_entities(self):
        self.annotation_entities = []
        for label in self.labels:
            self.annotation_entities.append(
                AnnotationEntity(
                    label=label.label,
                    category_id=label.category_id,
                    class_name=label.class_name,
                    annotation_type=AnnotationTypes.CLASSIFICATION,
                    confidence=label.confidence
                )
            )


class PoseAnnotation(Annotation):
    def __init__(self, poses: List[Pose], **kwargs):
        """Create a Pose annotation.

            Created from a union of one or more Poses.

            Parameters
            ----------
            poses:
                All Poses to include in the PoseAnnotation.
            **kwargs:
                Additional annotation attributes.  The keyword arguments are passed to ``scenebox.models.annotation``.
        """
        super().__init__(annotation_type=AnnotationTypes.TWO_D_POSE, **kwargs)
        self.poses = poses
        self.finalize()

    def set_annotation_entities(self):
        self.annotation_entities = []

        if not isinstance(self.poses, list):
            raise InvalidAnnotationError(
                "pose annotation is expected to be a list"
            )

        for pose in self.poses:
            self.annotation_entities.append(
                AnnotationEntity(
                    label=pose.label,
                    keypoints=pose.keypoints,
                    annotation_type=AnnotationTypes.TWO_D_POSE,
                    attributes=pose.attributes,
                    connections=pose.connections
                )
            )


class Cuboid2DAnnotation(Annotation):
    def __init__(self, cuboids: List[Cuboid2D], **kwargs):
        """Create a Cuboid annotation.

        Created from a union of one or more Cuboids.

        Parameters
        ----------
        cuboids:
            All Cuboids2Ds to include in the Cuboid2DAnnotation.
        **kwargs:
            Additional annotation attributes.  The keyword arguments are passed to ``scenebox.models.annotation``.
        """
        super().__init__(annotation_type=AnnotationTypes.TWO_D_CUBOID, **kwargs)
        self.cuboids = cuboids
        self.finalize()

    def set_annotation_entities(self):
        self.annotation_entities = []

        if not isinstance(self.cuboids, list):
            raise InvalidAnnotationError(
                "cuboids annotation is expected to be list"
            )

        for cuboid in self.cuboids:
            try:
                category_id = cuboid.category_id
                coords_ = [cuboid.tl1, cuboid.bl1, cuboid.tr1, cuboid.br1,
                           cuboid.tl2, cuboid.bl2, cuboid.tr2, cuboid.br2]
            except KeyError as e:
                raise InvalidAnnotationError(str(e))

            coordinates = []
            for c in coords_:
                coordinates.append({"x": c[0], "y": c[1]})
            self.annotation_entities.append(
                AnnotationEntity(
                    label=cuboid.label,
                    category_id=category_id,
                    annotation_type=AnnotationTypes.TWO_D_CUBOID,
                    coordinates=coordinates,
                    confidence=cuboid.confidence,
                    attributes=cuboid.attributes
                )
            )


class Cuboid3DAnnotation(Annotation):
    def __init__(self, cuboids: List[Cuboid3D], **kwargs):
        """Create a Cuboid annotation in three-dimensions.

        Created from a union of one or more Cuboids.

        Parameters
        ----------
        cuboids:
            All Cuboid3Ds to include in the Cuboid3DAnnotation.
        **kwargs:
            Additional annotation attributes.  The keyword arguments are passed to ``scenebox.models.annotation``.
        """
        super().__init__(annotation_type=AnnotationTypes.THREE_D_CUBOID,
                         media_type=AssetsConstants.LIDARS_ASSET_ID,
                         **kwargs)
        self.cuboids = cuboids
        self.finalize()

    def set_annotation_entities(self):
        self.annotation_entities = []

        if not isinstance(self.cuboids, list):
            raise InvalidAnnotationError(
                "cuboids annotation is expected to be list"
            )

        for cuboid in self.cuboids:
            try:
                category_id = cuboid.category_id
                coords_ = [cuboid.tl1, cuboid.bl1, cuboid.tr1, cuboid.br1,
                           cuboid.tl2, cuboid.bl2, cuboid.tr2, cuboid.br2]
            except KeyError as e:
                raise InvalidAnnotationError(str(e))

            coordinates = []
            for c in coords_:
                coordinates.append({"x": c[0], "y": c[1], "z": c[2]})

            self.annotation_entities.append(
                AnnotationEntity(
                    label=cuboid.label,
                    category_id=category_id,
                    annotation_type=AnnotationTypes.THREE_D_CUBOID,
                    coordinates=coordinates,
                    confidence=cuboid.confidence,
                    attributes=cuboid.attributes
                )
            )
