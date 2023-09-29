#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2023 Jordi Mas i Hernandez <jmas@softcatala.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

import logging
import xml.etree.ElementTree
import json
import os
import gc

import logging
from io import StringIO
import re

import fnmatch
import os


class FindFiles(object):
    def find_recursive(self, directory, pattern):
        filelist = []

        for root, dirs, files in os.walk(directory):
            for basename in files:
                if fnmatch.fnmatch(basename, pattern):
                    filename = os.path.join(root, basename)
                    filelist.append(filename)

        filelist.sort()
        return filelist


class TextExtract:
    def __init__(self, text):
        self.text = text

    def GetDescription(self):
        catalan = False
        DESCRIPTION_REGEX = r"description.*{{ca.*=(.*)}}.*"
        LICENSE_REG1 = r"{{[Ss]elf\|([^\|}]*).*}"
        LICENSE_REG2 = r"{{(.*)}}"
        description = ""
        license = ""
        next_license = False

        buf = StringIO(self.text)
        while True:
            s = buf.readline()
            if len(s) == 0:
                break

            s = s.replace("{{Ràdio Godella}}", "")
            s = s.replace("{{Ràdio Godella-imatge}}", "")
            s = s.replace("{{Sonoro Fermín Pardo}}", "")            
            s = s.replace("{{IVAM}}", "")
            s = s.replace("[[:ca:Yasmina Drissi i Sales|Yasmina Drissi i Sales]]", "Yasmina Drissi i Sales")
            
            
            if len(s.strip()) == 0:
                continue

            if next_license:
                match = re.search(LICENSE_REG1, s)
                #                print(f"s: {s} - l: {license} - m:{match}")
                if match:
                    license = match.group(1)
                else:
                    match = re.search(LICENSE_REG2, s)
                    if match:
                        license = match.group(1)
                    else:
                        license = s

            if "description" in s:
                match = re.search(DESCRIPTION_REGEX, s)
                if match:
                    description = match.group(1)

            next_license = "int:license-header" in s

        if len(description) > 0:
            return self.text, description.rstrip(), license.rstrip()
        else:
            return "", "", ""


class Definitions:
    def _get_revision_text(self, revision):
        for child in revision:
            if "text" in child.tag:
                return child.text

        return ""

    def process_definitions(self, filename, f_audios, f_debug):
        msg = f"** Read {filename}"
        f_debug.write(f"{msg}\n")
        print(msg)
        e = xml.etree.ElementTree.parse(filename).getroot()

        definitions = 0

        for page in e:
            is_verb = False
            text = ""
            title = ""

            for page_element in page:
                if "title" in page_element.tag:
                    title = page_element.text

                if "revision" in page_element.tag:
                    text = self._get_revision_text(page_element)

                    # if text is not None and '{{ca-verb' in text:
                    #    is_verb = True

            if text is None:
                text = ""

            if "File:" not in title:
                page.clear()
                continue

            title = title.replace("File:", "")

            if ".ogg" not in title and ".mp3" not in title:
                page.clear()
                continue

            textExtract = TextExtract(text)
            ca_desc, description, license = textExtract.GetDescription()

            if len(ca_desc) == 0:
                continue

            f_debug.write("-------------------------------\n")
            f_debug.write(f"title: {title}\n")
            f_debug.write(f"license: {license}\n")
            f_debug.write(f"description: {description}\n")
            f_debug.write(f"full text: {ca_desc}\n")

            f_audios.write(f"{title}\t{description}\t{license}\n")
            definitions += 1
            page.clear()

        e.clear()
        return definitions


def main():
    files = FindFiles().find_recursive("data/", "*")
    total = 0
    d = Definitions()
    with open("audio-files.txt", "w") as f_audios, open("extract-debug.txt", "w") as f_debug:
        for file in files:
            if "commonswiki-latest-pages-meta-current6.xml-p80043930p81543929" in file:
                continue
            defs = d.process_definitions(file, f_audios, f_debug)
            total += defs
            gc.collect()

            # if total > 2:
            #    break

    print(f"total: {total}")


if __name__ == "__main__":
    main()
