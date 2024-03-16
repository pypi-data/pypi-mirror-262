#  Copyright (c) 2020 Caliber Data Labs.
#  All rights reserved.
#

from typing import Optional, List
from scipy.spatial.transform import Rotation as R

from shared.tools.misc import euler_to_quaternion
from ...constants import (AnnotationProviders, AnnotationTypes, AssetsConstants, AnnotationGroups,
                                       AnnotationWorkflow)
from ...custom_exceptions import InvalidAnnotationError
from ...models.annotation import Annotation, AnnotationEntity
from ...models.object_access import ObjectAccess
from ...tools import time_utils
from ...tools.misc import get_md5_from_string


def convert_to_scale_format(annotation_metadata: dict) -> [List[dict], List[str]]:
    annotation_type = annotation_metadata.get("annotation_type")
    annotation_entities = annotation_metadata.get("annotation_entities")

    scale_annotations = []
    labels = []

    if annotation_type == AnnotationTypes.TWO_D_BOUNDING_BOX:
        for annotation_entity in annotation_entities:
            coordinates = annotation_entity["coordinates"]
            label = annotation_entity["label"]
            uid = annotation_entity["uid"]
            top, left = coordinates[0]["y"], coordinates[0]["x"]
            bottom, right = coordinates[2]["y"], coordinates[2]["x"]
            width = right - left
            height = bottom - top
            scale_bbox = {
                            "left": left,
                            "top": top,
                            "width": width,
                            "height": height,
                            "label": label.lower(),
                            "uuid": uid,
                            "annotation_id": annotation_metadata["id"]
                         }

            scale_annotations.append(scale_bbox)
            labels.append(label)

    elif annotation_type == AnnotationTypes.POLYGON:
        for annotation_entity in annotation_entities:
            label = annotation_entity["label"]
            uid = annotation_entity["uid"]
            coordinates = annotation_entity["coordinates"]
            scale_polygon = {
                                "vertices": coordinates,
                                "label": label.lower(),
                                "uuid": uid,
                                "annotation_id": annotation_metadata["id"]
                            }

            scale_annotations.append(scale_polygon)
            labels.append(label)

    elif annotation_type == AnnotationTypes.LINE:
        for annotation_entity in annotation_entities:
            label = annotation_entity["label"]
            uid = annotation_entity["uid"]
            coordinates = annotation_entity["coordinates"]
            scale_line = {
                                "vertices": coordinates,
                                "label": label.lower(),
                                "uuid": uid,
                                "annotation_id": annotation_metadata["id"]
                            }

            scale_annotations.append(scale_line)
            labels.append(label)

    elif annotation_type == AnnotationTypes.POINT:
        for annotation_entity in annotation_entities:
            label = annotation_entity["label"]
            uid = annotation_entity["uid"]
            coordinates = annotation_entity["coordinates"][0]
            scale_point = {
                                "x": coordinates["x"],
                                "y": coordinates["y"],
                                "label": label.lower(),
                                "uuid": uid,
                                "annotation_id": annotation_metadata["id"]
                            }

            scale_annotations.append(scale_point)
            labels.append(label)

    else:
        raise NotImplementedError

    return scale_annotations, list(set(labels))


class ScaleAnnotation(Annotation):
    def __init__(
            self,
            scale_response: dict,
            version: Optional[str] = None):

        self.scale_response = scale_response
        self.scaleapi_task = scale_response.get('task', {})
        self.scaleapi_params = self.scaleapi_task.get('params', {})
        self.scaleapi_type = self.scaleapi_task.get('type')
        self.scaleapi_annotations = self.scaleapi_task.get('response', {}).get('annotations', {})

        self.metadata = self.scaleapi_task.get('metadata', {})
        self.sets = [self.metadata.get("output_set_id")]
        self.workflow = self.metadata.get("workflow")

        if self.workflow == AnnotationWorkflow.FIX:
            receiving_strategy = self.metadata.get("receiving_strategy")
            assert receiving_strategy
            self.merge_update_hypothesis = (receiving_strategy == "merge_update_hypothesis")
            # Hypothesis annotations are pre-existing annotations we sent to Scale AI
            self.hypothesis = self.scaleapi_params.get("hypothesis", {}).get("annotations", {})

        if self.scaleapi_type == 'lidarannotation':
            media_type = AssetsConstants.LIDARS_ASSET_ID
            self.annotation_type = AnnotationTypes.THREE_D_CUBOID
        else:
            media_type = AssetsConstants.IMAGES_ASSET_ID

        if self.scaleapi_type == 'imageannotation':
            geometries = list(self.scaleapi_params["geometries"].keys())
            assert len(geometries) == 1
            if geometries[0] == "box":
                self.annotation_type = AnnotationTypes.TWO_D_BOUNDING_BOX
            elif geometries[0] == "line":
                self.annotation_type = AnnotationTypes.LINE
            elif geometries[0] == "polygon":
                self.annotation_type = AnnotationTypes.POLYGON
            elif geometries[0] == "point":
                self.annotation_type = AnnotationTypes.POINT
            else:
                raise InvalidAnnotationError('invalid geometry {} for annotation '
                                             'type {}'.format(geometries[0], self.scaleapi_type))

        elif self.scaleapi_type == 'segmentannotation':
            self.annotation_type = AnnotationTypes.SEGMENTATION

        else:
            raise InvalidAnnotationError('invalid annotation type {}'.format(
                    self.scaleapi_type))

        super().__init__(
            annotation_meta=self.scaleapi_task,
            asset_id=self.metadata.get("asset_id"),
            annotation_type=self.annotation_type,
            media_type=media_type,
            provider=AnnotationProviders.SCALE,
            version=version,
            annotation_group=AnnotationGroups.GROUND_TRUTH,
            id=self.scaleapi_task.get('task_id') + ".ann",
            timestamp=time_utils.string_to_datetime(self.scaleapi_task.get('created_at')),
            set_id=self.metadata.get("output_set_id"),
            raw_annotation_json=scale_response
        )

        if self.scaleapi_task.get('status') != 'completed':
            raise InvalidAnnotationError(
                'status {} is not completed'.format(
                    self.scaleapi_task.get('status')))

        self.finalize()


    def set_annotation_entities(self):

        self.annotations_to_accept = self.scaleapi_annotations
        if self.workflow == AnnotationWorkflow.FIX and self.merge_update_hypothesis:
            annotations_to_accept_dict = {annotation["uuid"]: annotation for annotation in self.hypothesis}
            # Overwrite hypothesis with any updates received
            for annotation in self.scaleapi_annotations:
                annotations_to_accept_dict[annotation["uuid"]] = annotation

            self.annotations_to_accept = list(annotations_to_accept_dict.values())

        if self.annotation_type == AnnotationTypes.TWO_D_BOUNDING_BOX:
            self.__set_bounding_box_annotation_entities()
        elif self.annotation_type == AnnotationTypes.POLYGON:
            self.__set_polygon_annotation_entities()
        elif self.annotation_type == AnnotationTypes.LINE:
            self.__set_line_annotation_entities()
        elif self.annotation_type == AnnotationTypes.POINT:
            self.__set_point_annotation_entities()
        elif self.annotation_type == AnnotationTypes.SEGMENTATION:
            self.__set_segmentation_annotation_entities()
        elif self.annotation_type == AnnotationTypes.THREE_D_CUBOID:
            self.__set_cuboid3d_annotation_entities()
        else:
            raise InvalidAnnotationError('invalid annotation type {}'.format(
                    self.scaleapi_type))


    def __set_bounding_box_annotation_entities(self):
        self.annotation_entities = []

        if not isinstance(self.annotations_to_accept, list):
            raise InvalidAnnotationError('bounding box annotation is expected to be list')

        for scaleapi_annotation in self.annotations_to_accept:
            try:
                width = scaleapi_annotation['width']
                height = scaleapi_annotation['height']
                left = scaleapi_annotation['left']
                top = scaleapi_annotation['top']
                label = scaleapi_annotation['label']
                uuid = scaleapi_annotation.get('uuid')
                attributes = scaleapi_annotation.get('attributes')

            except KeyError as e:
                raise InvalidAnnotationError(str(e))

            coordinates = [
                {
                    'x': left,
                    'y': top
                },
                {
                    'x': left + width,
                    'y': top
                },
                {
                    'x': left + width,
                    'y': top + height
                },
                {
                    'x': left,
                    'y': top + height
                }
            ]

            self.annotation_entities.append(AnnotationEntity(
                label=label,
                uid=uuid,
                annotation_type=AnnotationTypes.TWO_D_BOUNDING_BOX,
                coordinates=coordinates,
                attributes=attributes,
            ))

    def __set_polygon_annotation_entities(self):
        self.annotation_entities = []

        if not isinstance(self.annotations_to_accept, list):
            raise InvalidAnnotationError('polygon annotation is expected to be list')

        for scaleapi_annotation in self.annotations_to_accept:
            try:
                coordinates = scaleapi_annotation['vertices']
                label = scaleapi_annotation['label']
                uuid = scaleapi_annotation.get('uuid')
                attributes = scaleapi_annotation.get('attributes')
            except KeyError as e:
                raise InvalidAnnotationError(str(e))

            self.annotation_entities.append(AnnotationEntity(
                label=label,
                annotation_type=AnnotationTypes.POLYGON,
                coordinates=coordinates,
                attributes=attributes,
                uid=uuid
            ))

    def __set_line_annotation_entities(self):
        self.annotation_entities = []

        if not isinstance(self.annotations_to_accept, list):
            raise InvalidAnnotationError(
                'line annotation is expected to be list')

        for scaleapi_annotation in self.annotations_to_accept:
            try:
                coordinates = scaleapi_annotation['vertices']
                label = scaleapi_annotation['label']
                uuid = scaleapi_annotation.get('uuid')
                attributes = scaleapi_annotation.get('attributes')
            except KeyError as e:
                raise InvalidAnnotationError(str(e))

            self.annotation_entities.append(AnnotationEntity(
                label=label,
                annotation_type=AnnotationTypes.LINE,
                coordinates=coordinates,
                attributes=attributes,
                uid=uuid
            ))

    def __set_point_annotation_entities(self):

        self.annotation_entities = []

        if not isinstance(self.annotations_to_accept, list):
            raise InvalidAnnotationError(
                'lidar annotation is expected to be list')

        for scaleapi_annotation in self.annotations_to_accept:
            try:
                x = scaleapi_annotation['x']
                y = scaleapi_annotation['y']
                label = scaleapi_annotation['label']
                uuid = scaleapi_annotation.get('uuid')
            except KeyError as e:
                raise InvalidAnnotationError(str(e))

            coordinates = [
                {"x": x, "y": y}
            ]

            self.annotation_entities.append(AnnotationEntity(
                label=label,
                uid=uuid,
                annotation_type=AnnotationTypes.POINT,
                coordinates=coordinates,
                attributes=scaleapi_annotation.get('attributes')
            ))

    def __set_segmentation_annotation_entities(self):

        if not isinstance(self.scaleapi_annotations, dict):
            raise InvalidAnnotationError(
                'bounding box annotation is expected to be dict')

        self.annotation_entities = []

        if 'unlabeled' in self.scaleapi_annotations:
            url = self.scaleapi_annotations['unlabeled']
            mask_id = str(get_md5_from_string(url)).replace('-', '_')
            self.masks[mask_id] = ObjectAccess(url=url)
            self.annotation_entities.append(
                # TODO mask color needs to be specified here
                AnnotationEntity(
                    label='unlabeled',
                    annotation_type=AnnotationTypes.SEGMENTATION,
                    mask_id=mask_id,
                    mask_color="#ffffff"
                )
            )

        labeled_dic = self.scaleapi_annotations.get('labeled', {})
        for label in labeled_dic:
            value = labeled_dic[label]
            if isinstance(value, list):
                for url in value:
                    mask_id = str(get_md5_from_string(url)).replace('-', '_')
                    self.masks[mask_id] = ObjectAccess(url=url)
                    # TODO mask color needs to be specified here
                    self.annotation_entities.append(AnnotationEntity(
                        label=label,
                        annotation_type=AnnotationTypes.SEGMENTATION,
                        mask_id=mask_id,
                        mask_color="#ffffff")
                    )
            else:
                mask_id = str(get_md5_from_string(value)).replace('-', '_')
                self.masks[mask_id] = ObjectAccess(url=value)
                # TODO mask color needs to be specified here
                self.annotation_entities.append(AnnotationEntity(
                    label=label,
                    annotation_type=AnnotationTypes.SEGMENTATION,
                    mask_id=mask_id,
                    mask_color="#ffffff")
                )


    def _perform_rotation(self, centre, dimensions, yaw, pitch, roll):
        px = centre["x"]
        py = centre["y"]
        pz = centre["z"]

        dx = dimensions["x"] / 2
        dy = dimensions["y"] / 2
        dz = dimensions["z"] / 2

        zero_origin_corners = [[ dx,  dy,  dz],
                               [ dx,  dy, -dz],
                               [-dx,  dy, -dz],
                               [-dx,  dy,  dz],
                               [ dx, -dy,  dz],
                               [ dx, -dy, -dz],
                               [-dx, -dy, -dz],
                               [-dx, -dy,  dz]]

        quaternion = euler_to_quaternion(roll=roll, pitch=pitch, yaw=yaw, degrees=False)
        r = R.from_quat(quaternion)
        rotated_corners = r.apply(zero_origin_corners)

        # Translate points to cuboidal centre
        rotated_corners[:, 0] += px
        rotated_corners[:, 1] += py
        rotated_corners[:, 2] += pz

        return rotated_corners


    def __set_cuboid3d_annotation_entities(self):
        self.annotation_entities = []

        if not isinstance(self.annotations_to_accept, list):
            raise InvalidAnnotationError('cuboid annotations are expected to be list')

        for scaleapi_annotation in self.annotations_to_accept:
            cuboids = scaleapi_annotation["cuboids"]
            for cuboid in cuboids:
                try:
                    centre = cuboid["position"]
                    dimensions = cuboid["dimensions"]
                    yaw = cuboid["yaw"]
                    pitch = cuboid["pitch"]
                    roll = cuboid["roll"]
                    uuid = cuboid.get('uuid')
                    attributes = cuboid.get('attributes')
                    label = cuboid.get('label')
                    attributes["camera_used"] = cuboid.get('camera_used')
                    attributes["distance_to_device"] = cuboid.get('distance_to_device')

                except KeyError as e:
                    raise InvalidAnnotationError(str(e))

                # Rotate the cuboid by the yaw, pitch and roll
                corner_coordinates = self._perform_rotation(centre=centre,
                                                            dimensions=dimensions,
                                                            yaw=yaw,
                                                            pitch=pitch,
                                                            roll=roll)
                tr1 = corner_coordinates[0]
                br1 = corner_coordinates[1]
                bl1 = corner_coordinates[2]
                tl1 = corner_coordinates[3]
                tr2 = corner_coordinates[4]
                br2 = corner_coordinates[5]
                bl2 = corner_coordinates[6]
                tl2 = corner_coordinates[7]

                coords = [tl1, bl1, tr1, br1,
                          tl2, bl2, tr2, br2]

                self.annotation_entities.append(AnnotationEntity(
                    label=label,
                    uid=uuid,
                    annotation_type=AnnotationTypes.THREE_D_CUBOID,
                    coordinates=coords,
                    attributes=attributes,
                ))
