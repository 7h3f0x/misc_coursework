# Problem Statement 2

## About the code

The code has been written in the `go` programming language.

It uses the `net` library for looking up the hostname for an ip. There is a
function for this which returns the first name it finds, if any is found or
else returns the string ` --- `.

It also has a function to read all bytes from a file using the `os` library to
open the file and the `ioutil` library to read all the bytes.

Next we have the main function which takes the `.json` filename as command-line
arguement. It then reads all bytes from that file. It then uses the `json`
library to convert those bytes into `array` of `map` objects. We then take the 
destination addresses from all the packets and make a count of them. We ignore
the localhost address here. Next we find the top 3 counts from these. In the end
we just resolve these IPs into hostnames and print the IP, Hostname, count in a
nice tabular form.


## Readme for running the code

### Getting the `capture.json` file

1. Download wireshark from the [website](https://www.wireshark.org/download.html)

2. Open the capture.pcapng file in wireshark.

3. Apply the `tls` filter by typing `tls` in the filter toolbar.

4. Export these select packets by going to `File` in the menu toolbar. Then go
   to the option `Export Packet Dissections`. After that select the `As JSON`
   option and save the file as `capture.json`.

For convenience, `capture.json` has also been provided by me in the current
folder.

### Compiling the golang code

1. Get the golang compiler from the [website](https://golang.org/dl/).

2. Make sure to add the `go` binary to the path. This can be checked by doing
   `go version` on the command line. If this results in an error, add golang to
   your default path.

3. In the root folder of this project, run `go build src/packet.go`, this will
   create the necessary `packet.exe` (for windows) or `packet` (for
   linux/macOS), for your system.

For convenience, pre-built binaries have been provided in the `bin` folder in
this project. `packet.exe` is for windows, `packet.elf` is for linux and
`packet` is for macOS.

### Running the binary

To run the binary on the `capture.json` file, simply supply it as the second
arguement while running the binary.

- On windows, run `.\packet.exe capture.json`

- On linux run `./packet capture.json` if you have compiled yourself, else if
  you have used the `Makefile` or the prebuilt binaries, run `./packet.elf
  capture.json`

- On macOs, run `./packet capture.json`

### Using the Makefile

As a convenience, a Makefile has also been provided. Systems which support
Makefiles or the `make` can simply run `make all` from the root of this project
folder to compile binaries for all operating systems or run `make <OS>` where
`OS` can be `linux`, `windows`, or `mac`, to build for a particular operating
system.

