"""Miscellaneous (catch all) tools Copyright 2020 Caliber Data Labs."""

#  Copyright (c) 2020 Caliber Data Labs.
#  All rights reserved.
#
from typing import NamedTuple, Optional

from .logger import get_logger

logger = get_logger(__name__)


class VideoProperties:
    def __init__(self,
                 width: int,
                 height: int,
                 fps: float,
                 duration: float,
                 num_frames: int,
                 num_read_frames: int):

        self.width = width
        self.height = height
        self.fps = fps
        self.duration = duration
        self.num_frames = num_frames
        self.num_read_frames = num_read_frames


def get_video_attributes(video_source: str,
                         fast: bool = True) -> Optional[VideoProperties]:
    try:
        import ffmpeg
        if fast:
            info = ffmpeg.probe(video_source)
        else:
            info = ffmpeg.probe(video_source, count_frames=None)
    except Exception as e:
        logger.warning("could not get properties from {} because {}".format(video_source, str(e)))
        return None

    info_stream = None
    for streams in info["streams"]:
        if streams.get("codec_type") == "video":
            info_stream = streams
            break

    if not info_stream:
        info_stream = info['streams'][0]

    return VideoProperties(
        width=int(info_stream.get('width') or 0),
        height=int(info_stream.get('height') or 0),
        duration=float(info_stream['duration']),
        num_frames=int(info_stream.get('nb_frames') or 0),
        fps=0 if info_stream['avg_frame_rate'] == '0/0' else eval(info_stream['avg_frame_rate']),
        num_read_frames=int(info_stream.get('nb_read_frames') or 0)
    )
