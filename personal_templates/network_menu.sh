destination = ~/.config/networking/network_menu.sh
executable = True
-----------------------------------------------
#!/usr/bin/zsh
states="Start|Stop|Restart"
res=$(echo "$states" | {{cmd:rofi_dmenu}} -sep "|" -p "Wifi" -lines 3)
sudo $XDG_CONFIG_HOME/networking/networking.sh "$res"
