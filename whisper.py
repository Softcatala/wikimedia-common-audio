import logging
import os
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import urllib.parse
import shutil
from faster_whisper import WhisperModel

model_size = "medium"


def main():
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    with open("audio-files-good.txt", "r") as f_audios, open(
        "detect-debug.txt", "w"
    ) as f_detect, open("detect_ca.txt", "w") as f_detect_ca:
        lines = f_audios.readlines()
        isCatalan = False
        for line in lines:
            components = line.split("\t")
            _file = components[0]
            _file = _file.replace("File:", "")
            _file = _file.replace(" ", "_")
            fullpath = os.path.join(f"files/{_file}")
            try:
                segments, info = model.transcribe(fullpath)

            except Exception as e:
                print(f"File: '{_file}'. Error '{e}'")
                continue

            print(
                "File: '%s'. Detected language '%s' with probability %f, duration %s"
                % (_file, info.language, info.language_probability, info.duration)
            )
            f_detect.write(
                f"{_file}, {info.language}, {info.language_probability}, {info.duration}\n"
            )

            catalan_path = f"catalan/{_file}"
            if info.language == "ca":
                MAX = 90 * 1024 * 1024
                size = os.path.getsize(fullpath)
                bigger = size > MAX
                if bigger:
                    msg = f"Discarted: {fullpath} - {size} - {MAX} - {bigger}"
                    print(msg)
                    f_detect.write(msg)
                    continue

                if info.language_probability < 0.5:
                    msg = f"Discarted: {fullpath} - {info.language}, {info.language_probability}"
                    print(msg)
                    f_detect.write(msg)
                    continue

                line = line.rstrip()
                line += f"\t{info.duration}\n"
                f_detect_ca.write(line)
                shutil.copy(fullpath, catalan_path)
                isCatalan = True

            if not isCatalan and os.path.exists(catalan_path):
                os.remove(catalan_path)
                msg = f"Removed: {fullpath}"
                print(msg)
                f_detect.write(msg)


if __name__ == "__main__":
    main()
