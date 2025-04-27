#!/usr/bin/env python3

"""
This file is a modified version of the file available here:
https://github.com/flatpak/flatpak-builder-tools/blob/master/poetry/flatpak-poetry-generator.py

The file above has a long-standing issue pulling dependencies for Pyside6. This modified version
is hard-coded to work with Pyside6. Hopefully there is a better long-term fix in the future.

Chase Christiansen, 04/13/2024
"""
__license__ = "MIT"

import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
from collections import OrderedDict

import toml


def get_pypi_source(name: str, version: str, hashes: list) -> tuple:
    """Get the source information for a dependency.

    Args:
        name (str): The package name.
        version (str): The package version.
        hashes (list): The list of hashes for the package version.

    Returns (tuple): The url and sha256 hash.

    """
    url = "https://pypi.org/pypi/{}/json".format(name)
    print("Extracting download url and hash for {}, version {}".format(name, version))
    with urllib.request.urlopen(url) as response:
        body = json.loads(response.read().decode("utf-8"))
        for release, source_list in body["releases"].items():
            if release != version:
                continue

            for source in source_list:
                if (
                    name == "pyside6-addons"
                    or name == "pyside6-essentials"
                    or name == "shiboken6"
                ):
                    if (
                        source["filename"].endswith("x86_64.whl")
                        and "manylinux" in source["filename"]
                    ):
                        return source["url"], source["digests"]["sha256"]
                if (
                    source["packagetype"] == "bdist_wheel"
                    and "py3" in source["python_version"]
                    and source["digests"]["sha256"] in hashes
                ):
                    return source["url"], source["digests"]["sha256"]
            for source in source_list:
                if (
                    source["packagetype"] == "sdist"
                    and "source" in source["python_version"]
                    and source["digests"]["sha256"] in hashes
                ):
                    return source["url"], source["digests"]["sha256"]
        else:
            raise Exception("Failed to extract url and hash from {}".format(url))


def get_module_sources(parsed_lockfile: dict, include_devel: bool = True) -> list:
    """Gets the list of sources from a toml parsed lockfile.

    Args:
        parsed_lockfile (dict): The dictionary of the parsed lockfile.
        include_devel (bool): Include dev dependencies, defaults to True.

    Returns (list): The sources.

    """
    sources = []
    hash_re = re.compile(r"(sha1|sha224|sha384|sha256|sha512|md5):([a-f0-9]+)")
    for section, packages in parsed_lockfile.items():
        if section != "package":
            continue

        for package in packages:
            if "category" in package and (
                    package.get("category") != "dev" or not include_devel or package.get("optional")) and (
                    package.get("category") != "main" or package.get("optional")):
                continue

            hashes = []
            # Check for old metadata format (poetry version < 1.0.0b2)
            if "hashes" in parsed_lockfile["metadata"]:
                hashes = parsed_lockfile["metadata"]["hashes"][package["name"]]
            # metadata format 1.1
            elif "files" in parsed_lockfile["metadata"]:
                hashes.append(get_sources_11(package, parsed_lockfile, hash_re))
            # metadata format 2.0
            else:
                hashes.append(get_sources_13(package, hash_re))

            url, hash = get_pypi_source(
                package["name"], package["version"], hashes
            )
            source = {"type": "file", "url": url, "sha256": hash}
            sources.append(source)
    return sources


def get_sources_11(package, parsed_lockfile, hash_re) -> list:
    hashes = []
    for package_name in parsed_lockfile["metadata"]["files"]:
        if package_name != package["name"]:
            continue

        package_files = parsed_lockfile["metadata"]["files"][
            package["name"]
        ]
        num_files = len(package_files)
        for num in range(num_files):
            match = hash_re.search(package_files[num]["hash"])
            if not match:
                continue

            hashes.append(match.group(2))

    return hashes


def get_sources_13(package, hash_re) -> list:
    hashes = []

    for file in package["files"]:
        match = hash_re.search(file["hash"])
        if not match:
            continue

        hashes.append(match.group(2))

    return hashes


def get_dep_names(parsed_lockfile: dict, include_devel: bool = True) -> list:
    """Gets the list of dependency names.

    Args:
        parsed_lockfile (dict): The dictionary of the parsed lockfile.
        include_devel (bool): Include dev dependencies, defaults to True.

    Returns (list): The dependency names.

    """
    dep_names = []
    for section, packages in parsed_lockfile.items():
        if section != "package":
            continue

        for package in packages:
            if "category" in package and (
                    package.get("category") != "dev" or not include_devel or package.get("optional")) and (
                    package.get("category") != "main" or package.get("optional")):
                continue

            dep_names.append(package["name"])

    return dep_names


def main():
    parser = argparse.ArgumentParser(description="Flatpak Poetry generator")
    parser.add_argument("lockfile", type=str)
    parser.add_argument(
        "-o", type=str, dest="outfile", default="generated-poetry-sources.json"
    )
    parser.add_argument("--production", action="store_true", default=False)
    args = parser.parse_args()

    include_devel = not args.production
    outfile = args.outfile
    lockfile = args.lockfile

    print('Scanning "%s" ' % lockfile, file=sys.stderr)

    with open(lockfile, "r") as f:
        parsed_lockfile = toml.load(f)
        dep_names = get_dep_names(parsed_lockfile, include_devel=include_devel)
        pip_command = [
            "pip3",
            "install",
            "--no-index",
            '--find-links="file://${PWD}"',
            "--prefix=${FLATPAK_DEST}",
            " ".join(dep_names),
        ]
        main_module = OrderedDict(
            [
                ("name", "poetry-deps"),
                ("buildsystem", "simple"),
                ("build-commands", [" ".join(pip_command)]),
            ]
        )
        sources = get_module_sources(parsed_lockfile, include_devel=include_devel)
        main_module["sources"] = sources

    print(" ... %d new entries" % len(sources), file=sys.stderr)

    print('Writing to "%s"' % outfile)
    with open(outfile, "w") as f:
        f.write(json.dumps(main_module, indent=4))


if __name__ == "__main__":
    main()
