import pyautogui
import random
import winsound

def extreme_random_mouse_jiggle():
    for i in range(20):
        x = random.randint(-100, 100)
        y = random.randint(-100, 100)
        pyautogui.moveRel(x, y, duration=0.3)

    
def play_ringing_noise():
    frequency = random.randint(800, 20000)
    duration = random.randint(1000, 10000)
    winsound.Beep(frequency, duration)

def windows_noise():
    winsound.MessageBeep(winsound.MB_ICONHAND)

def click():
    for i in range(random.randint(1, 20)):
        pyautogui.click()

def popup_window():
    for i in range(random.randint(1, 27)):
        pyautogui.alert('Close me!')
        #play windows noise on close
        windows_noise()

def random_key_press():
    for i in range(random.randint(1, 20)):
        pyautogui.typewrite(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'))

def random_placement_random_key_press():
    for i in range(random.randint(1, 20)):
        for i in range(random.randint(1, 20)):
            pyautogui.typewrite(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'))
        for i in range(random.randint(1, 6)):
            pyautogui.press('left')

random_placement_random_key_press()

