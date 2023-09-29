.PHONY: build

build:
	python extract.py
	cp audio-files.txt audio-files-good.txt
	python whisper.py
