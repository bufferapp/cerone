NAME := bufferapp/cerone-consumer:0.1.1

.PHONY: all
all: run

.PHONY: build
build:
	docker build -t $(NAME) .

.PHONY: run
run: build
	docker run -it --rm $(NAME)

.PHONY: dev
dev:
	docker run -it --rm $(NAME) bash
