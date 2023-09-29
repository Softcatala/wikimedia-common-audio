.PHONY: build

build:
	python extract.py
	cp audio-files.txt audio-files-good.txt
	python whisper.py
	git commit -a -m "Fix" && git push	
