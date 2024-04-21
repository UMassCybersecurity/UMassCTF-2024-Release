chal:
	docker build -t magic-conch-base -f build.Dockerfile .
	rm static/*
	docker create --name conchdummy magic-conch-base
	docker cp conchdummy:/home/magic_conch_user/static/magic_conch static/magic_conch
	docker rm -f conchdummy