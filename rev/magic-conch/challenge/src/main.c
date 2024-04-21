// Standard
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>

// Threading
#include <pthread.h>

// Networking
#include <arpa/inet.h>
#include <sys/socket.h>

// Crypto
#include <openssl/sha.h>


#define DGST_LEN 32 // sha256 returns 32 bytes

// Both set in EntryPoint based on environment variable
char* FLAG = NULL;
int PORT = 0;

const char* welcome = "Welcome! You may ask the Magic Conch ~two~ queries\n";
const char* errmsg  = "ERROR: The Magic Conch cannot be reached right now\n";
const char* fail    = "The Magic Conch did not find your queries interesting, try again\n";
const char* repeat  = "The Magic Conch does not like repeated queries, begone!\n";

// Convert raw hash bytes to printable hex string
void bytes_to_hex(unsigned char *hash, unsigned char *out) {
    for(int i=0; i < DGST_LEN; i++) {
        sprintf((unsigned char*) out + 2*i, "%02x", (unsigned char) hash[i]);
    }
    out[2*DGST_LEN] = '\0';
}


// Fills buffer out with x XORed with y.
void Xor(char* x, char* y, char* out, int len) {
    for (int i=0; i < len; i++) {
        out[i] = x[i] ^ y[i];
    }
}

// Returns pointer to hash of input.
// Returns null if input is 0 length.
char* HASH(char* input) {
    char* hash_value;
    char X[DGST_LEN / 2];
    char Y[DGST_LEN / 2];
    char Z[DGST_LEN];

    memset(X, 0, DGST_LEN / 2);
    memset(Y, 0, DGST_LEN / 2);
    memset(Z, 0, DGST_LEN);

    memcpy(X, input, DGST_LEN/2);
    memcpy(Y, input + DGST_LEN/2, DGST_LEN/2);
    Xor(X, Y, Z, DGST_LEN/2);
    
    hash_value = (char *) malloc(DGST_LEN);
    SHA256(Z, DGST_LEN, hash_value);
    return hash_value;
}


// Thread callback
void* thread_start(void* thread_args) {
    // Buffers to read queries into
    char q1[DGST_LEN + 1];
    char q2[DGST_LEN + 1];
    // Buffers to store hex encoded hash response
    char hex1[2*DGST_LEN + 1];
    char hex2[2*DGST_LEN + 1];
    // Buffers to store response messages.
    char resp1[256];
    char resp2[256];

    // Zero out all buffers
    memset(q1, 0, DGST_LEN + 1);
    memset(q2, 0, DGST_LEN + 1);
    memset(hex1, 0, 2*DGST_LEN + 1);
    memset(hex2, 0, 2*DGST_LEN + 1);
    memset(resp1, 0, 256);
    memset(resp2, 0, 256);
    
    // Argument is client socket fd
    int client_sock = *((int*) thread_args);

    // Welcome message
    send(client_sock, welcome, strlen(welcome), 0);
    
    // Handle first query
    send(client_sock, "Query 1: ", 9, 0);
    recv(client_sock, q1, DGST_LEN+1, 0);
    char* hash1 = HASH(q1);
    if (hash1 == NULL) {
        send(client_sock, errmsg, strlen(errmsg), 0);
        goto end;
    }
    bytes_to_hex(hash1, hex1);
    sprintf(resp1, "Magic Conch says: %s\n", hex1);
    send(client_sock, resp1, strlen(resp1), 0);

    // Handle second query
    send(client_sock, "Query 2: " , 9, 0);
    recv(client_sock, q2, DGST_LEN+1, 0);
    char* hash2 = HASH(q2);
    if (hash2 == NULL) {
        send(client_sock, errmsg, strlen(errmsg), 0);
        free(hash1);
        goto end;
    }
    bytes_to_hex(hash2, hex2);
    sprintf(resp2, "Magic Conch says: %s\n", hex2);
    send(client_sock, resp2, strlen(resp2), 0);


    // Check if inputs were equal
    if (memcmp(q1, q2, DGST_LEN) == 0) {
        send(client_sock, repeat, strlen(repeat), 0);
    }
    // Check for hash collision
    else if(memcmp(hash1, hash2, DGST_LEN) == 0) {
            char win[256] = {0};
            sprintf(win, "The Magic Conch is pleased with your queries. Here is your reward: %s\n", FLAG);
            send(client_sock, win, strlen(win), 0);
    }
    else {
        send(client_sock, fail, strlen(fail), 0);
    }

    free(hash1);
    free(hash2);
end:    
    close(client_sock);
    pthread_exit(0);
}

int EntryPoint(int argc, char *argv[]) {

    // Check to make sure FLAG env variable is set
    FLAG = getenv("FLAG");
    if (FLAG == NULL) {
        printf("ERROR: Environment variable FLAG not set\n");
        exit(1);
    }

    char* port_string = getenv("PORT");
    if (port_string == NULL) {
        printf("ERROR: Environment variable PORT not set\n");
        exit(1);
    }
    PORT = atoi(port_string);

    // Socket setup
    int sock;
    struct sockaddr_in address;
    socklen_t addrlen = sizeof(address);
 
    // Creating socket
    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        //printf("ERROR: Could not create socket\n");
        exit(1);
    }
 
    // Bind socket
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);
    if (bind(sock, (struct sockaddr*) &address, sizeof(address)) < 0) {
        //printf("ERROR: socket bind failed\n");
        exit(1);
    }

    // Listen
    if (listen(sock, 10) < 0) {
        //printf("ERROR: Listening failed\n");
        exit(1);
    }
    printf("Listening on port %d...\n", PORT);

    // Accept connections
    while (1) {
        int client_sock;
        struct sockaddr_in client_addr;
        if ((client_sock = accept(sock, (struct sockaddr*)&client_addr, &addrlen)) < 0) {
            //printf("ERROR: could not accept connection\n");
            exit(1);
        }
        pthread_t tid;
        pthread_create(&tid, NULL, thread_start, &client_sock);
        //printf("New thread: %u\n", tid);        
    }
 
    // Close listener
    close(sock);
    return 0;

}