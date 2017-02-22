#!/usr/bin/env python
import argparse
import codecs
import glob
import json
import logging
import os.path
from collections import defaultdict

from jinja2 import Environment, FileSystemLoader, select_autoescape

from schamas import streams

log = logging.getLogger(__name__)


def combine_streams(streams_dir):
    streams_out = defaultdict(list)
    for file in glob.glob(os.path.join(streams_dir, "*.json")):
        with open(file) as fd:
            sdata = streams.validate(json.load(fd))
            for s in sdata["streams"]:
                a = dict(sdata["attributes"])
                a.update(s.get("attributes", {}))
                s["attributes"] = a
                if s["attributes"]["subscription"]:
                    s["attributes"]["authentication"] = True
                streams_out[sdata["name"]].append(s)
    return streams_out


if __name__ == "__main__":
    def main():
        parser = argparse.ArgumentParser()
        parser.add_argument("template_path")
        parser.add_argument("streams_path")
        parser.add_argument("outpath")

        args = parser.parse_args()

        env = Environment(
            loader=FileSystemLoader(args.template_path),
            autoescape=select_autoescape(['html'])
        )

        template = env.get_template("index.html.j2")

        data = combine_streams(args.streams_path)

        with codecs.open(os.path.join(args.outpath, "index.html"), "wb", encoding="utf8") as ofd:
            ofd.write(template.render(streams=data, sorted=sorted))

    main()