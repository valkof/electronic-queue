#!/bin/bash

curl -sS -k -u 'eq01:e******1' --connect-timeout 5 -m 5 -X GET 'http://127.0.0.1:32107/tcurr?w=12'

exit 0

