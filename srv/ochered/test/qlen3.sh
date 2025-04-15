#!/bin/bash

curl -sS -k -u 'eq01:e******1' --connect-timeout 5 -m 5 'http://127.0.0.1:32107/qlen?q=3'

exit 0

