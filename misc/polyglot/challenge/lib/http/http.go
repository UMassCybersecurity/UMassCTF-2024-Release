package http

import (
	"log"
	"net/http"
)

func Run() {
	// Define the handler function
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		// Serve from the directory /home/haylin/
		http.FileServer(http.Dir("/home/haylin/Public/")).ServeHTTP(w, r)
	})

	// Define the port to listen on
	port := "9001"
	log.Printf("HTTP: Listening on :%s\n", port)

	// Start the HTTP server on port 9001
	err := http.ListenAndServe(":"+port, nil)
	if err != nil {
		log.Printf("HTTP: Error starting server: %s\n", err)
		return
	}
}
