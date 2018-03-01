destination = ~/.config/wallpapers/launch.sh
executable = True
------------------------------------------
#! /bin/sh
wallpaper_source="$XDG_CONFIG_HOME"/wallpapers/default_wallpaper.jpg
if [ -d "$XDG_CONFIG_HOME"/wallpapers/{{colors:primary_name}} ]; then
  wallpaper_source=$(shuf -n1 -e "$XDG_CONFIG_HOME"/wallpapers/{{colors:primary_name}}/*)
fi

feh --bg-scale --no-fehbg "$wallpaper_source"
