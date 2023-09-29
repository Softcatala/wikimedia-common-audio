import logging
import os
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import urllib.parse

class DownloadFile(object):
    def urlopen_with_retry(self, url):
        NTRIES = 3
        NOT_FOUND = 404
        TIMEOUT = 15

        timeout = TIMEOUT
        for ntry in range(NTRIES):
            try:
                req = Request(
                    url,
                    headers={
                        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64;) Gecko Firefox"
                    },
                )
                return urlopen(req, timeout=timeout)
            except HTTPError as e:
                logging.error(
                    f"HTTPError on urlopen_with_retry. URL: '{url}', error: '{e}'"
                )
                if e.code == NOT_FOUND:
                    return
            # May be server load that needs more time to compute the request
            except TimeoutError as e:
                if ntry + 1 == NTRIES:
                    logging.error(
                        f"Time out error on urlopen_with_retry. URL: '{url}', error: '{e}'"
                    )
                timeout = timeout * 4
            except Exception as e:
                print(type(e))
                logging.error(
                    f"Error on urlopen_with_retry. URL: '{url}', error: '{e}'"
                )

    def _remove_incomplete_file(self, filename):
        if os.path.exists(filename):
            os.remove(filename)

    def get_file(self, url, filename):
        try:
            msg = "Downloading file '{0}' to {1}".format(url, filename)
            logging.info(msg)

            infile = self.urlopen_with_retry(url)
            output = open(filename, "wb")
            output.write(infile.read())
            output.close()
        except Exception:
            msg = "Error downloading file '{0}' to {1}".format(url, filename)
            logging.error(msg)
            self._remove_incomplete_file(filename)


import hashlib


def main():
    d = DownloadFile()
    with open("audio-files-good.txt", "r") as f_audios:
        lines = f_audios.readlines()
        for line in lines:
            components = line.split("\t")
            _file = components[0]
            _file = _file.replace("File:", "")
            _file = _file.replace(" ", "_")
            print(_file)
            fullpath = os.path.join(f"files/{_file}")

            if os.path.exists(fullpath) and os.stat(fullpath).st_size > 0:
                print(f"File {fullpath} already exists")
                continue

            md5 = hashlib.md5(_file.encode("utf-8")).hexdigest()
            letter_1 = md5[0]
            letter_2 = md5[0:2]
            _file_url = urllib.parse.quote(_file)
            url = f"https://upload.wikimedia.org/wikipedia/commons/{letter_1}/{letter_2}/{_file_url}"
            print(url)
            d.get_file(url, fullpath)


if __name__ == "__main__":
    main()
