package proxy

import (
	"bytes"
	"fmt"
	"io"
	"log"
	"net"
	"time"
)

func Run() {
	listener, err := net.Listen("tcp", ":1337")
	if err != nil {
		log.Fatalf("Proxy: Failed to listen on port 8080: %v", err)
	}
	defer listener.Close()
	log.Println("Proxy: Listening on :1337")

	for {
		conn, err := listener.Accept()
		if err != nil {
			log.Printf("Proxy: Failed to accept connection: %v", err)
			continue
		}

		go handleConnection(conn)
	}
}

func handleConnection(clientConn net.Conn) {
	defer clientConn.Close()

	log.Println("Proxy: Accepted connection from", clientConn.RemoteAddr())

	// Set a timeout for the initial read
	clientConn.SetReadDeadline(time.Now().Add(5 * time.Second))

	buffer := make([]byte, 3)
	n, err := io.ReadFull(clientConn, buffer)

	// Reset the deadline
	clientConn.SetReadDeadline(time.Time{})

	if err != nil {
		if netErr, ok := err.(net.Error); ok && netErr.Timeout() {
			// Handle timeout scenario, possibly FTP
			handleFTPReady(clientConn)
			return
		}
		log.Printf("Proxy: Error reading from client: %v", err)
		return
	}

	backendAddress, err := determineBackend(buffer[:n])
	if err != nil {
		log.Printf("Proxy: Failed to determine backend: %v", err)
		clientConn.Write([]byte("Failed to detect known protocol"))
		clientConn.Close()
		return
	}

	// Dial the backend server
	backendConn, err := net.Dial("tcp", backendAddress)
	if err != nil {
		log.Printf("Proxy: Failed to connect to backend %s: %v", backendAddress, err)
		return
	}
	defer backendConn.Close()

	// Use MultiReader to prepend the read bytes back into the stream
	multi := io.MultiReader(bytes.NewReader(buffer[:n]), clientConn)

	// Use goroutine for bidirectional copy
	go io.Copy(backendConn, multi)
	io.Copy(clientConn, backendConn)
}

func handleFTPReady(clientConn net.Conn) {
	backendConn, err := net.Dial("tcp", "127.0.0.1:9003")
	if err != nil {
		log.Printf("Proxy: Failed to connect to backend 127.0.0.1:9003: %v", err)
		return
	}
	defer backendConn.Close()

	go io.Copy(backendConn, clientConn)
	io.Copy(clientConn, backendConn)
}

// determineBackend selects a backend based on the first 3 bytes
func determineBackend(data []byte) (string, error) {

	// HTTP obv
	if string(data) == "GET" || string(data) == "POS" {
		return "127.0.0.1:9001", nil
	}

	// SSH
	if string(data) == "SSH" {
		return "127.0.0.1:9002", nil
	}

	return "", fmt.Errorf("unknown protocol")
}
