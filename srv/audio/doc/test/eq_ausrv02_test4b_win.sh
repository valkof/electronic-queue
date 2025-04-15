#!/bin/bash

GET="curl -sS -k -u username:password --connect-timeout 5 -m 5 http://127.0.0.1:32105/1%2C2%2C%D0%9F99%2C3,k_kabinetu"
#echo $GET
echo $($GET)

exit 0