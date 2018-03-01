destination = ~/.config/change_system_state/change_state.sh
executable = True
-----------------------------------------------------------
#! /bin/sh
states="Shutdown|Restart|Lock|Suspend|Logout"

res=$(echo "$states" | rofi -sep "|" -color-window "{{colors:primaryDD}}, {{colors:accent}}, {{colors:primaryDD}}" -color-normal "{{colors:primaryDD}}, {{colors:primary}}, {{colors:primaryDD}}, {{colors:accent}}, {{colors:primaryD}}" -dmenu -p ":" -i -lines 5)

sleep 0.2

case "$res" in
  Shutdown)
    systemctl poweroff
    ;;
  Restart)
    systemctl reboot
    ;;
  Lock)
    "$XDG_CONFIG_HOME"/change_system_state/lock/lock.sh &
    ;;
  Suspend)
    systemctl suspend
    ;;
  Logout)
    bspc quit
    ;;
  *)
    exit 1
esac
