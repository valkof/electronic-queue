#!/bin/bash
#while true
# do
# ping -c 3 zeromis.tutmed.by
# if [[ $? -eq 0 ]]; then
#  break
# fi
# sleep 1
#done
# infokiosk
/usr/lib64/firefox/firefox --kiosk "http://127.0.0.1:86/ochered/ochered.html"

#sleep 2

# local
#/usr/lib64/firefox/firefox "http://127.0.0.1/cgi-bin/ping.cgi?sfil_n=123&sit_l=201" &
#/usr/lib64/firefox/firefox --kiosk "http://127.0.0.1:88/cgi-bin/ping.cgi?sfil_n=123&sit_l=201" &

# infokiosk
#/usr/lib64/firefox/firefox "http://zeromis.tutmed.by/cgi-bin/is10_02?sSd_=0&sfil_n=123&shead_=0&svid_=5&sgr_l=530&sit_l=120" &

#sleep 2
#xdotool search --sync --onlyvisible --class "Firefox" windowactivate key F11
