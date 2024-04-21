package main

import (
	"github.com/hamptonmoore/multiproto/lib/ftp"
	"github.com/hamptonmoore/multiproto/lib/http"
	"github.com/hamptonmoore/multiproto/lib/proxy"
	"github.com/hamptonmoore/multiproto/lib/ssh"
)

func main() {
	go http.Run()
	go ftp.Run()
	go ssh.Run()
	go proxy.Run()

	// Block forever
	select {}
}
