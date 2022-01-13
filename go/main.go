package main

import (
	"log"
	"os"
	)

func main() {
	// logging:
	log.SetPrefix("phonetest ")
	log.SetFlags(log.Ldate|log.Lmicroseconds|log.LUTC|log.Lshortfile)
	log.SetOutput(os.Stderr)
	video()
	rfkill()
	thermal()
	event()
}
