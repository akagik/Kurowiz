tell application "System Events"
	key down {command}
		keystroke tab
		delay 0.2 
		keystroke tab
	key up {command}
--   keystroke tab using {command down}
--   keystroke tab using {command down}
end tell

