#!/bin/bash

curl -sS -k -u username:password --connect-timeout 5 -m 5 'http://127.0.0.1:32107/get_wplaces'
