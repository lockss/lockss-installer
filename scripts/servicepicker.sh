#!/bin/sh
# Select which LOCKSS service should be run.
#
tmp_file=$(tempfile 2>/dev/null) || tmp_file=/tmp/test$$
trap "rm -f $tmp_file" 0 1 2 5 15

# Display message with option to cancel
dialog --title "SERVICE PICKER" \
--clear \
--checklist "Select lockss components to install:" 16 60 9 \
	1	"LOCKSS Configuration Service" on \
	2	"LOCKSS Metadata Service" on \
	3	"LOCKSS Metadata Extraction Service" on \
	4	"LOCKSS Poller Service" on \
	5	"LOCKSS Repository" on \
	5	"LOCKSS Postgres Service" on \
	7	"LOCKSS SOLR Service" on \
	8	"HDFS Storage" off \
	9	"PY Wayback Service" on\
	2> $tmp_file


retval=$?
case $retval in
  0)
    echo "'$choice is your selection";;
  1)
    echo "Cancel pressed.";;
  255)
    echo "ESC pressed.";;
esac
