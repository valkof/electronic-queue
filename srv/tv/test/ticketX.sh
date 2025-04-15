#!/bin/bash

curl -sS -k -u username:password --connect-timeout 5 -m 5 -X GET 'http://127.0.0.1:32109/ticket?p=123&t=F333'

exit 0

