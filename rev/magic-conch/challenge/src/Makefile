

# Key and IV for encrypting the payload 
KEY := $(shell echo -n "YELLOW SUBMARINE" | hexdump -ve '1/1 "%02x"')
IV := $(shell echo -n "*CHICKEN NUGGET*" | hexdump -ve '1/1 "%02x"')


all:
	# Create main program as dynamic library
	gcc main.c -O0 -shared -fPIC -lssl -lcrypto -lpthread -o ../build/payload.so

	# Encrypt library, then hex encode, output to payload.txt
	openssl enc -aes-128-cbc -K "$(KEY)" -iv "$(IV)" -e -in ../build/payload.so | hexdump -ve '1/1 "%02x"' > ../build/payload.txt

	# Does some string obfuscation and copy-pasting for us. Creates loader_final.c
	python preprocess.py

	# Compile and strip final binary
	gcc ../build/loader_final.c -lssl -lcrypto -ldl -lnsl -lc -o ../static/magic_conch
	strip ../static/magic_conch


# Same thing as above, just compiled with -g (debug symbols) and no stripping
debug:
	gcc main.c -g -O0 -shared -fPIC -lssl -lcrypto -lpthread -o ../build/payload.so

	openssl enc -aes-128-cbc -K "$(KEY)" -iv "$(IV)" -e -in ../build/payload.so | hexdump -ve '1/1 "%02x"' > ../build/payload.txt

	python preprocess.py

	gcc ../build/loader_final.c -g -lssl -lcrypto -ldl -lnsl -lc -o ../static/magic_conch


clean:
	rm ../build/*
	rm ../static/magic_conch