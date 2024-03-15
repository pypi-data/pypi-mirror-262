from datetime import datetime
import time
import pyautogui
from . import constants

#--------------------------------------------------
# move the mouse to a new position, then back 
#--------------------------------------------------
def move_mouse():
    # move mouse
    pause()
    x, y = pyautogui.position()
    pyautogui.moveTo(x + 1, y + 1)

    # move mouse back to original position
    pause()
    pyautogui.moveTo(x, y)

#--------------------------------------------------
# turn up / down the volume button (to prevent screen lock)
#--------------------------------------------------
def change_volume():
    pyautogui.press(constants.Keys.VOLUME_DOWN)
    pause()
    pyautogui.press(constants.Keys.VOLUME_UP)

#--------------------------------------------------
# report the mouse movement
#--------------------------------------------------
def report_movement():
    print_message_with_time('Mouse moved.')
    pause(constants.MIN_SLEEP_SECONDS)

#--------------------------------------------------
# print program data
#--------------------------------------------------
def print_program_data(num_minutes):
    print()
    print_message_with_time('Program started')
    print(f'Sleep cycle: {num_minutes} min.\n')

#--------------------------------------------------
# print the current time
#--------------------------------------------------
def print_message_with_time(message):
    current = datetime.now()
    output = current.strftime(constants.OUTPUT_TIME_FORMAT_TOKEN)
    print(f'{output} - {message}')

#--------------------------------------------------
# pause the current program execution
#--------------------------------------------------
def pause(seconds=constants.PAUSE_SECONDS):
    time.sleep(seconds)
