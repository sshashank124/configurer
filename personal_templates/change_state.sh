destination = ~/.config/change_system_state/change_state.sh
executable = True
-----------------------------------------------------------
#! /bin/zsh
states="Lock|Suspend|Logout|Shutdown|Restart"

res=$(echo "$states" | {{cmd:rofi}} -sep "|" -p "System")

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
