#!/bin/bash

GET="curl -sS -k -u username:password --connect-timeout 5 -m 5 http://192.168.124.132:32105/"
#echo $GET
echo $($GET)

exit 0