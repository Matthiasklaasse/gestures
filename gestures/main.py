print('Loading code...')
import handtracking

print('Loading fake mouse input')
try:
    import pyautogui
except ImportError:
    print("pyautogui not found. Installing...")
    try:
        import subprocess
        subprocess.check_call(['pip', 'install', 'pyautogui'])
        import pyautogui
        print("pyautogui installed successfully.")
    except Exception as e:
        print("Failed to install pyautogui:", str(e))
        exit(1)

print('Loaded fake mouse input')
import time
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

sensitivity = float(config['Important']['mouse_sensitivity'])
pyautogui.FAILSAFE = False

pinch_started = False
last_position = None
screen_width, screen_height = pyautogui.size()
hand_detected = False
previous_actions = []

print('Ready')
while True:
    action = False
    frame = handtracking.get_and_parse_frame()
    if frame.multi_hand_landmarks:
        if not(hand_detected):
            print('Hand detected')
            hand_detected = True
            
        if handtracking.check_for_click(frame):
            pyautogui.mouseDown()
            print("Mouse down")
            previous_actions.append('mouse_down')
            action = True
            time.sleep(0.05)
        else:
            pyautogui.mouseUp()

        if handtracking.check_for_right_click(frame):
            pyautogui.rightClick()
            previous_actions.append('mouse_up')
            print("Right click")
            action = True
            time.sleep(0.05)

        if handtracking.check_for_scroll_click(frame) and False: #not for now...
            pyautogui.mouseDown(button='middle')
            previous_actions.append('mouse_middle')
            print("Scroll down")

        previous_actions = previous_actions[-3:]

        if previous_actions == ['mouse_down', 'mouse_down', 'mouse_down']:
            previous_actions.append("double")
            print('Double click')
            action = True
            pyautogui.doubleClick()

        if not(action):
            is_pinching = handtracking.check_for_grab(frame)
            if is_pinching:
                if not pinch_started:
                    pinch_started = True
                    last_position = list(handtracking.get_hand_position(is_pinching))
                else:
                    current_position = list(handtracking.get_hand_position(is_pinching))
                    previous_actions.append('mouse_move')

                    if current_position and last_position:
                        x, y, z = current_position
                        x -= last_position[0]
                        y -= last_position[1]

                        x *= sensitivity
                        y *= sensitivity

                        x = int(x * screen_width) * -1
                        y = int(y * screen_height)

                        pyautogui.moveRel(x, y, duration = int(config['Important']['mouse_speed']) - 10)
                        last_position = current_position

            else:
                pinch_started = False
                last_position = None
    elif hand_detected:
        print("Hand not longer detected")
        hand_detected = False
