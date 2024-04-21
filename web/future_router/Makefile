SRC_DIR := ./challenge

FRIENDS := patrick spongebob squidward

REGISTRY := us.gcr.io
PROJECT_ID := umassctf2024
IMAGE_BASE_NAME := future-router-friends

# Build images
build-friends: $(FRIENDS)

$(FRIENDS):
	docker build -t $(REGISTRY)/$(PROJECT_ID)/$(IMAGE_BASE_NAME):$@ $(SRC_DIR)/$@

# Push images
push-friends: build
	$(foreach friend, $(FRIENDS), docker push $(REGISTRY)/$(PROJECT_ID)/$(IMAGE_BASE_NAME):$(friend);)

.PHONY: all build push $(FRIENDS)
