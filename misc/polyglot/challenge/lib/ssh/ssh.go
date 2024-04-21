package ssh

import (
	"fmt"
	"io"
	"log"

	"strings"

	"github.com/gliderlabs/ssh"
	gossh "golang.org/x/crypto/ssh"
)

var adminKey = "AAAAC3NzaC1lZDI1NTE5AAAAINVBSiDCCv2zW3hYOnAQs7sze1rV/nLRvTcJ71Ivy5Vt"

func Run() {
	ssh.Handle(func(s ssh.Session) {
		authorizedKey := gossh.MarshalAuthorizedKey(s.PublicKey())
		io.WriteString(s, fmt.Sprintf("You found my SSH server! Welcome!\nSSH Key Used: %s\n", string(authorizedKey)))

		if strings.Contains(string(authorizedKey), adminKey) {
			io.WriteString(s, "Oh! Hey Haylin, here's the key UMASS{us1ng_4_tcp_t1me0ut_t0_d3t3ct_ftp_l0l}\n")
		} else {
			io.WriteString(s, "You are not using my admin key, Sorry...\n\n")
		}
	})

	publicKeyOption := ssh.PublicKeyAuth(func(ctx ssh.Context, key ssh.PublicKey) bool {
		return true // allow all keys, or use ssh.KeysEqual() to compare against known keys
	})

	log.Println("SSH: listening on port :9002")
	log.Fatal(ssh.ListenAndServe(":9002", nil, publicKeyOption))
}
