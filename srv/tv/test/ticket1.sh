#!/bin/bash

curl -sS -k -u tv01:e******1 --connect-timeout 5 -m 5 -X GET 'http://127.0.0.1:32109/ticket?p=6&t=3'

exit 0

