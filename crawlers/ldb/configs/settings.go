package configs

import (
	"log"
	"os"
	"strconv"
	"time"
)

var BLOCK_RANGE_REPORT uint64 = 100000

// Database configs
var MOONSTREAM_DB_MAX_IDLE_CONNS int = 30
var MOONSTREAM_DB_CONN_MAX_LIFETIME = 30 * time.Minute
var MOONSTREAM_DB_URI = os.Getenv("MOONSTREAM_DB_URI")

// Humber configs
var HUMBUG_LDB_CLIENT_ID = os.Getenv("HUMBUG_LDB_CLIENT_ID")
var HUMBUG_LDB_TOKEN = os.Getenv("HUMBUG_LDB_TOKEN")
var HUMBUG_LDB_BLOCK_RANGE_REPORT = os.Getenv("HUMBUG_LDB_BLOCK_RANGE_REPORT")

func init() {
	if HUMBUG_LDB_BLOCK_RANGE_REPORT != "" {
		ldbRangeReport, err := strconv.ParseUint(HUMBUG_LDB_BLOCK_RANGE_REPORT, 16, 64)
		if err != nil {
			log.Fatal(err)
		}
		BLOCK_RANGE_REPORT = ldbRangeReport
	}
}