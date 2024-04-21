chal:
	docker build -t bench-225-image -f build.Dockerfile .
	rm -rf ./static/*
	docker create --name bench225dummy bench-225-image
	docker cp bench225dummy:/home/tmp_bench_225/bench-225 static/bench-225
	cp static/bench-225  challenge/static/bench-225
	docker rm -f bench225dummy
