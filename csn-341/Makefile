all: src/packet.go
	GOOS=linux go build -o bin/packet.elf src/packet.go 
	GOOS=windows go build -o bin/packet.exe src/packet.go 
	GOOS=darwin go build -o bin/packet src/packet.go

linux: src/packet.go
	GOOS=linux go build -o bin/packet.elf src/packet.go 

windows: src/packet.go
	GOOS=windows go build -o bin/packet.exe src/packet.go 

mac: src/packet.go
	GOOS=darwin go build -o bin/packet src/packet.go
