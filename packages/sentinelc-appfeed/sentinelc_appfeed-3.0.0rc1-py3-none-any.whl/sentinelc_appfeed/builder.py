import argparse
from genericpath import isdir
import json
from os import listdir

from .utils.ArgparseCustomTypes import ArgparseCustomTypes

from .validator import validate

version = 3


def build_feed(manifest_path):
    apps = []

    # List valid apps
    for folder in listdir(manifest_path):
        item = f"{manifest_path}/{folder}"
        if isdir(item):
            apps.append(validate(manifest_path, folder))

    # sort
    apps.sort(key=lambda x: x["name"])

    feed = {"version": version, "apps": apps}

    return feed


def main():

    parser = argparse.ArgumentParser(
        description="""
        Builds a sentinelc app feed JSON file from a manifest folder container one or more apps.

        how to use
        -------------

        `applib-builder -p [manifests] -f [feed.json]`
        Creates a feed based on the manifests folder and output the feed as feed.json
        """  # noqa: W293 E501
    )

    parser.add_argument(
        "-p",
        "--path",
        action="store",
        help='Specify the root of the manifest folder. Default: "manifests"',
        type=ArgparseCustomTypes.dir_path,
        default="manifests",
    )

    parser.add_argument(
        "-f",
        "--filename",
        action="store",
        help='Specify the name of the output file. Default: "feed.json"',
        default="feed.json",
    )

    args = parser.parse_args()

    feed = build_feed(args.path)

    with open(args.filename, "w") as outfile:
        json.dump(feed, outfile, indent=4)


if __name__ == "__main__":
    main()
