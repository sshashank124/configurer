destination = ~/.config/display/change_display.sh
executable = True
--------------------------------------------------
#!/usr/bin/sh
states="Primary|Secondary|Extend|Mirror|144 Hz"
res=$(echo "$states" | {{cmd:rofi}} -sep "|" -p "Display")
$XDG_CONFIG_HOME/display/set_display.sh "$res"
