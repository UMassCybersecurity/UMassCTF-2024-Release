package ftp

import (
	"log"

	filedriver "github.com/goftp/file-driver"
	"github.com/goftp/server"
)

// Allow auth with username "haylin" and no password
type simpleAuth struct {
}

func (a *simpleAuth) CheckPasswd(user, pass string) (bool, error) {
	return user == "haylin", nil
}

// Logger that does nothing
type noOpLogger struct{}

func (l *noOpLogger) Print(sessionID string, message interface{}) {
}

func (l *noOpLogger) Printf(sessionID string, format string, v ...interface{}) {
}

func (l *noOpLogger) PrintCommand(sessionID string, command string, params string) {
}

func (l *noOpLogger) PrintResponse(sessionID string, code int, message string) {
}

func Run() {
	var (
		root = "/home/haylin/"
		port = 9003
		host = "127.0.0.1"
	)

	factory := &filedriver.FileDriverFactory{
		RootPath: root,
		Perm:     server.NewSimplePerm("haylin", "haylin"),
	}

	opts := &server.ServerOpts{
		Factory:        factory,
		Port:           port,
		Hostname:       host,
		Auth:           &simpleAuth{},
		Logger:         &noOpLogger{},
		PassivePorts:   "30000-30020",
		WelcomeMessage: "",
	}

	log.Printf("FTP: starting on  :%v", opts.Port)
	server := server.NewServer(opts)
	err := server.ListenAndServe()
	if err != nil {
		log.Fatal("FTP: Error starting server:", err)
	}
}
