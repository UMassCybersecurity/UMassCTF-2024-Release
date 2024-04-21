chal:
	docker build -t mits-are-awesome-base -f build.Dockerfile .
	rm static/*
	docker create --name mitdummy mits-are-awesome-base
	docker cp mitdummy:/home/user/src/wrapper static/wrapper
	docker cp mitdummy:/home/user/src/chall static/chall
	docker rm -f mitdummy
	cp challenge/src/chall.c static/
	cp challenge/src/wrapper.c static/
	cp static/chall challenge/static/chall
	cp static/wrapper challenge/static/wrapper