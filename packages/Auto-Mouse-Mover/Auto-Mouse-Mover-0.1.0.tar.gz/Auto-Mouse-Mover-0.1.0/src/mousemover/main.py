import pyautogui
from . import constants
from . import routines

#--------------------------------------------------
# Main logic
#--------------------------------------------------
def run():
    pyautogui.FAILSAFE = False

    # print program data
    routines.print_program_data(constants.MAX_CYCLES)

    print(f'\n\nBe sure to place hover your mouse over Teams calendar!!\n\n')

    # make program sleep for specified sleep cycle
    for _ in range(constants.MAX_CYCLES):
        routines.move_mouse()
        routines.change_volume()
        routines.report_movement()