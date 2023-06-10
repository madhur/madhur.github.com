---
layout: blog-post
title: "Process huge log files"
excerpt: "Process huge log files"
disqus_id: /2023/06/10/processing-huge-log-files/
tags:
    - Go
---

Recently, I was faced with a situation where I had to process huge (in order of several gigabytes) log files.

The log files consisted of either [CSV format](https://en.wikipedia.org/wiki/Comma-separated_values) or [AWS ALB logs format](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-access-logs.html)

Here the process means, I had to process each row to either filter it or store the valuable information from it for later analysis.


First, I attempted with python to parse it with the simple logic

```python
file_name = home + '/Downloads/huge_file.csv'
filtered_rows = []
with open('./filtered.csv', 'w', newline='') as csvfile:
     dict_writer = csv.DictWriter(csvfile, ["client_ip", "target_processing_time", "target_status_code", "received_bytes", "request_url", "request_creation_time", "ssl_protocol", "trace_id" ])
     with open(file_name, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            # Do some processing
            filtered_rows.append(obj)
            dict_writer.writerow(obj)
```

The above program reads the CSV line by line and optionally writes few columns of it to another file.


This was done on a 12 GB CSV file and it took 4-5 hours.

I was not satisfied with it as I had to do multiple iterations on multiple such files. There had to be a better way.

Turned to [Go](https://go.dev/) due to its concurrency features

There is a [encoding/csv](https://pkg.go.dev/encoding/csv) package in go which can help read the CSV files. However, it is signle threaded and does not make use of multiple goroutines.

Came across another package [github.com/actforgood/bigcsvreader](https://github.com/actforgood/bigcsvreader) which can help read the big CSV files with the use of multiple routines.

Quickly wrote a program which reads the bunch of huge CSV files in a folder and applies processing logic to it. Below is the sample snippet:

The below program reads the folder of log files and processes each one after another. However, since the reading is done using multiple goroutines, the below program can process 12 GB of ALB log file in matter of few seconds. The log files in my case was the list of ALB log files from AWS. Note that ALB log files are space character separated.

Also, if the files are huge, we need to increase the buffer space in library so that its heap memory does not runs out.



```go
bigCSV.ColumnsDelimiter = ' '
bigCSV.BufferSize = 81920

```

The `processRow()` function receives each row and based on the process / filtering criteria publishes the data of type `ALBLog` on the `resultChan` channel.

There is another inline goroutine which reads all the data from `resultChan` channel and writes it to `filtered.csv`


```go
package main

import (
	"context"
	"encoding/csv"
	"fmt"
	"log"
	"os"
	"strings"
	"sync"
	"sync/atomic"
	"github.com/actforgood/bigcsvreader"
	"net/url"
)

const noOfColumns = 29
var rowCount = 0

type ALBLog struct {
	ClientIP             string
	TargetProcessingTime string
	TargetStatusCode     string
	ReceivedBytes        string
	RequestUrl           string
	RequestCreationTime  string
	SSLProtocol          string
	TraceID              string
	RawRow               []string
}

type count32 int32

func (c *count32) inc() int32 {
	return atomic.AddInt32((*int32)(c), 1)
}
func (c *count32) get() int32 {
	return atomic.LoadInt32((*int32)(c))
}
func (c *count32) reset()  {
	atomic.StoreInt32((*int32)(c), 0)
}
var counter count32

func main() {

	homedir, _ := os.UserHomeDir()
	csvLocation := homedir + "/logs/"
	entries, err := os.ReadDir(csvLocation)
	if err != nil {
		log.Fatal(err)
	}

	var TotalProcessRows int32
	var FilteredProcessedRows int
	
	f, err := os.Create("filtered.csv")
	w := csv.NewWriter(f)
	w.Write([]string{"request_url", "target_processing_time"})
	w.Flush()
	f.Close()

	for _, e := range entries {
		if strings.HasSuffix(e.Name(), ".log") {
			totalRows, filteredRows := processFile(csvLocation, e.Name())
			TotalProcessRows = TotalProcessRows + totalRows
			FilteredProcessedRows = FilteredProcessedRows + filteredRows
		}
	}

	fmt.Fprintf(os.Stdout, "Total Rows: %d Filtered Rows: %d", TotalProcessRows, FilteredProcessedRows)
}

func processFile(csvLocation string, fileName string) (int32, int) {

	counter.reset()
	// initialize the big csv reader
	bigCSV := bigcsvreader.New()
	bigCSV.SetFilePath(csvLocation + fileName)
	bigCSV.ColumnsCount = noOfColumns
	bigCSV.MaxGoroutinesNo = 16
	bigCSV.BufferSize = 81920
	bigCSV.FileHasHeader = true
	bigCSV.ColumnsDelimiter = ' '

	ctx, cancelCtx := context.WithCancel(context.Background())
	defer cancelCtx()
	var wg sync.WaitGroup
	var filteredRows int
	// start multi-thread reading
	rowsChans, errsChan := bigCSV.Read(ctx)
	resultChan := make(chan ALBLog)

	for i := 0; i < len(rowsChans); i++ {
		wg.Add(1)
		go rowWorker(rowsChans[i], &wg, resultChan)
	}

	wg.Add(1)
	go errWorker(errsChan, &wg)

	var writeCSVWaitGroup sync.WaitGroup
	go func() {
		writeCSVWaitGroup.Add(1)
		var result []ALBLog
		for filteredLog := range resultChan {
			result = append(result, filteredLog)
		}
		fmt.Fprintf(os.Stdout, "%s Filtered rows %d\n", fileName, len(result))
		filteredRows = len(result)

		f, err := os.OpenFile("filtered.csv", os.O_APPEND|os.O_WRONLY|os.O_CREATE, 0600)
		defer f.Close()

		if err != nil {
			log.Fatalln("failed to open file", err)
		}

		w := csv.NewWriter(f)
		defer w.Flush()

		if err != nil {
			log.Fatal(err)
		}

		for _, row := range result {
			w.Write(row.RawRow)
		}

		writeCSVWaitGroup.Done()

	}()

	wg.Wait()
	close(resultChan)

	writeCSVWaitGroup.Wait()
	fmt.Fprintf(os.Stdout, " %s Total rows: %d\n", fileName, counter.get())

	return counter.get(), filteredRows
}

func rowWorker(rowsChan bigcsvreader.RowsChan, waitGr *sync.WaitGroup, resultChan chan<- ALBLog) {
	for row := range rowsChan {
		processRow(row, resultChan)
	}
	waitGr.Done()
}

func errWorker(errsChan bigcsvreader.ErrsChan, waitGr *sync.WaitGroup) {
	for err := range errsChan {
		handleError(err)
	}
	waitGr.Done()
}

// processRow can be used to implement business logic
// like validation / converting to a struct / persisting row into a storage.
func processRow(row []string, resultChan chan<- ALBLog) {
	clientIP := strings.Split(row[3], ":")[0]
	requestUrl := strings.Split(row[12], " ")[1]
	urlObject, err := url.Parse(requestUrl)

	counter.inc()

	RawRow := []string {urlObject.Path, row[6]}
	alblog := ALBLog{
		ClientIP:             clientIP,
		TargetProcessingTime: row[6],
		TargetStatusCode:     row[9],
		ReceivedBytes:        row[10],
		RequestUrl:           row[12],
		RequestCreationTime:  row[21],
		RawRow:               RawRow,
	}
	
	if doSomeFiltering() {
		resultChan <- alblog
	}
}

// handleError handles the error.
// errors can be fatal like file does not exist, or row related like a given row could not be parsed, etc...
func handleError(err error) {
	fmt.Println("error", err)
}
```