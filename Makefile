.PHONY: all

build:
	docker build --rm=false -f Dockerfile -t chaliy/tokenize-ms .

run:
	docker run -it -p 8080:8080 chaliy/tokenize-ms

dev:
	docker run -it -p 8080:8080 -v .://app chaliy/tokenize-ms sh
