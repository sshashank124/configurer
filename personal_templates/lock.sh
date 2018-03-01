destination = ~/.config/change_system_state/lock/lock.sh
executable = True
-----------------------------------------------------------
#!/bin/sh
lock_dir="/tmp/lock_screen"
mkdir -p $lock_dir
scrot "$lock_dir"/bg.png
convert "$lock_dir"/bg.png -resize 10% -resize 1000% "$lock_dir"/bg.png
convert "$XDG_CONFIG_HOME"/change_system_state/lock/arch.png -fill "{{colors:primary}}" -colorize 100% "$lock_dir"/arch_colorized.png
convert "$lock_dir"/bg.png "$lock_dir"/arch_colorized.png -gravity center -composite -matte "$lock_dir"/lock_screen.png
i3lock -e -u -i "$lock_dir"/lock_screen.png
rm -r "$lock_dir"
