#!/usr/bin/env python
import logging

log = logging.getLogger(__name__)

from validation import *

streams = Schema(Dict({
    "name": Text(),
    "attributes": Dict({
        "geolocked": Bool(default=False),
        "region": AnyOf(Null(), Text(), default=None),
        "language": Text(default="und"),
        "authentication": Bool(default=False),
        "drm": Bool(default=False),
        "hd": Bool(default=False),
        "subscription": Bool(default=False)
    }, default={}),
    "streams": Repeating(
        Dict({
            "name": Text(),
            "title": Text(),
            "url": Text(),
            "attributes": Dict({
                Optional("geolocked"): Bool(),
                Optional("region"): AnyOf(Null(), Text()),
                Optional("language"): Text(),
                Optional("authentication"): Bool(),
                Optional("drm"): Bool(),
                Optional("hd"): Bool(),
                Optional("subscription"): Bool()
            }, default={})
        })
    )
}))
