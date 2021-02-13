 
#!/bin/bash

# Check if gedit is running
# -x flag only match processes whose name (or command line if -f is
# specified) exactly match the pattern. 

if pgrep -x "mycroft-gui-app" > /dev/null
then
   echo "running" > /dev/null
   # killall mycroft-gui-app
else
    /usr/bin/mycroft-gui-app >nul 2>&1 & echo "mycroft-GUI" > /dev/null
    sleep 10
    /usr/bin/wmctrl -a mycroft.gui -b toggle,fullscreen

fi
