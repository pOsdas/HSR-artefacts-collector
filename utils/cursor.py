import time
import pyautogui


def find_cursor():
    """
    Найти координаты курсора
    """
    time.sleep(5)
    x, y = pyautogui.position()

    print(f"Координаты курсора: x={x}, y={y}")