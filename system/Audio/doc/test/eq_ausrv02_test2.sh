#!/bin/bash

GET="curl -sS -k -u username:password --connect-timeout 5 -m 5 http://127.0.0.1:32105/99,88,А,7"
#echo $GET
echo $($GET)

exit 0