package main

import (
    "os"
    "fmt"
    "io/ioutil"
    "encoding/json"
    "net"
    "strings"
)

func getHostnameFromIP(ip string) string {
    names, err := net.LookupAddr(ip)
    if err != nil {
        return " --- "
    }
    return names[0]
}

func readFile(fname string) []uint8 {
    fp, err := os.Open(fname)
    if err != nil {
        fmt.Fprintln(os.Stderr, err)
        os.Exit(1)
    }
    defer fp.Close()
    bytes, err := ioutil.ReadAll(fp)
    if err != nil {
        fmt.Fprintln(os.Stderr, err)
        os.Exit(1)
    }
    return bytes
}

func main() {
    if len(os.Args) < 2 {
        fmt.Fprintf(os.Stderr, "Usage: %s <path-to-json-file>\n", os.Args[0])
        os.Exit(1)
    }
    bytes := readFile(os.Args[1])
    var packets []map[string]interface{}
    err := json.Unmarshal([]byte(bytes), &packets)
    if err != nil {
        fmt.Fprintln(os.Stderr, err)
        os.Exit(1)
    }

    ips := make(map[string]int)

    // take counts of all destination IPs
    for _, packet := range packets {
        _source := packet["_source"]
        if _source != nil {
            layers := _source.(map[string]interface{})["layers"]
            if layers != nil {
                ip_layer := layers.(map[string]interface{})["ip"]
                if ip_layer != nil {
                    dst_ip := ip_layer.(map[string]interface{})["ip.dst"].(string)
                    if strings.HasPrefix(dst_ip, "192.168") {
                        continue
                    }
                    ips[dst_ip] += 1
                }
            }
        }
    }

    top3 := [3](string){"", "", ""}

    // find top 3 IP addresses
    for ip, num := range ips {
        if num > ips[top3[0]] {
            top3[2] = top3[1]
            top3[1] = top3[0]
            top3[0] = ip
        } else if num > ips[top3[1]] {
            top3[2] = top3[1]
            top3[1] = ip
        } else if num > ips[top3[2]] {
            top3[2] = ip
        }
    }

    // print in nice tabular form
    separator := ""
    for i := 0; i < (20 + 50 + 15 + 2 + 2 + 1 + 2 + 1 + 1); i++ {
        separator += "-"
    }
    fmt.Println(separator)
    fmt.Printf("| %20s | %50s | %15s |\n", "IP Address", "HostName", "Frequency")
    fmt.Println(separator)
    for _, ip := range top3 {
        fmt.Printf("| %20s | %50s | %15d |\n", ip, getHostnameFromIP(ip), ips[ip])
    }
    fmt.Println(separator)

}
