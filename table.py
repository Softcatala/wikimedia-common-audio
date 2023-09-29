#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Author Jordi Mas i Hernandez <jmas@softcatala.org>

import os


def main():
    print("Builds a table with available audios")

    audios = 0
    with open("README.md", "w") as table_md, open("detect_ca.txt", "r") as f_detect:
        with open("header.md", "r") as f_header:
            lines = f_header.readlines()
            for line in lines:
                table_md.write(line)

        table_md.write(f"File | Description | License | Length (seconds)\n")
        table_md.write("|---|---|---|---\n")

        lines = sorted(f_detect.readlines())
        for line in lines:
            components = line.split("\t")
            if len(components) < 4:
                print(line)
                continue

            _filename = components[0].rstrip()
            _description = components[1].rstrip()
            _license = components[2].rstrip()
            _length = components[3].rstrip()
            _filename = _filename.replace(" ", "_")

            _length = float(_length)
            _length = f"{_length:.0f}"

            url = f"catalan/{_filename}"

            if len(_filename) > 20:
                _filename = f"{_filename[0:20]}...{_filename[-20:]}"

            entry = f"|[{_filename}]({url}) | {_description}| {_license} | {_length}\n"
            table_md.write(entry)
            audios += 1

        msg = f"Total number of files: {audios}\n"
        table_md.write(msg)
        print(f"\n{msg}")


if __name__ == "__main__":
    main()
