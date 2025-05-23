IMAGE_NAME=ghcr.io/mmarconi93/qrypsis
TAG=latest

build:
	docker build -t $(IMAGE_NAME):$(TAG) .

run:
	docker run --rm -v $(PWD):/app $(IMAGE_NAME):$(TAG)

publish:
	echo "${GHCR_TOKEN}" | docker login ghcr.io -u mmarconi93 --password-stdin
	docker push $(IMAGE_NAME):$(TAG)