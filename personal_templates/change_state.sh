destination = ~/.config/change_system_state/change_state.sh
executable = True
-----------------------------------------------------------
#! /bin/sh
states="Lock|Suspend|Logout|Shutdown|Restart"

res=$(echo "$states" | rofi -sep "|" -color-window "{{colors:primaryDDD}}, {{colors:primaryD}}, {{colors:primaryDDD}}" -color-normal "{{colors:primaryDDD}}, {{colors:primaryL}}, {{colors:primaryDDD}}, {{colors:accent}}, {{colors:primaryDD}}" -dmenu -p ":" -i -lines 5)

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
