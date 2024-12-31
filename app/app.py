import flet as ft
import pyautogui
import threading
import time
import os
import json
import sys


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


config_file = 'config.json'


def load_config():
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return json.load(f)
    else:
        return {'wait_time': 80}


def save_config(configs):
    with open(config_file, 'w') as f:
        json.dump(configs, f)


stop_program = False
config = load_config()
wait_time = config['wait_time']


def main(page: ft.Page):
    page.title = "Honkai Artefacts collect"
    page.window_always_on_top = True
    page.window_width = 300
    page.window_height = 500
    page.window_resizable = False
    page.window.maximizable = False
    page.window_icon = "assets/favicon.ico"

    label = ft.Text("Авто сбор артефактов!", size=20, weight="bold", color="blue")

    description = "Кнопка 'Старт' выполняет следующее:\n" \
                  "1. Ждет пока вы откроете игру 10 секунд.\n" \
                  "2. Собирает артефакты и запускает бой заново.\n"

    timer_label = ft.Text("", size=16, color="blue")

    empty_label = ft.Text("")

    def on_save(e):
        config['wait_time'] = int(wait_time_field.value)
        save_config(config)
        page.snack_bar = ft.SnackBar(ft.Text("Настройки сохранены"), open=True)
        page.update()
        print("config has been updated")

    def countdown(start_seconds, callback):
        for i in range(start_seconds, 0, -1):
            timer_label.value = f"Таймер: {i} секунд"
            page.update()
            time.sleep(1)
        timer_label.value = "Начинаем автоматизацию"
        page.update()
        callback()

    def perform_actions():
        screen_width, screen_height = pyautogui.size()
        pyautogui.click(x=screen_width // 2, y=screen_height // 2)

        x_coordinate, y_coordinate = 1183, 952  # approximate coordinates of the button
        interval = load_config()

        global stop_program
        while not stop_program:
            pyautogui.click(x_coordinate, y_coordinate)
            print(f"Клик выполнен в координатах ({x_coordinate}, {y_coordinate})")
            time.sleep(interval['wait_time'])

    def start_button_handler(e):
        global stop_program
        stop_program = False
        threading.Thread(
            target=countdown, args=(10, lambda: threading.Thread(target=perform_actions).start())
        ).start()
        print("start button")

    def stop_button_handler(e):
        global stop_program
        stop_program = True
        print("stop button")

    def on_close(e):
        print("Приложение закрыто")
        page.window_close()

    start_button = ft.ElevatedButton(
        text="Старт",
        on_click=start_button_handler,
        style=ft.ButtonStyle(bgcolor=ft.colors.INDIGO_500, color=ft.colors.WHITE),
        tooltip=description,
    )

    stop_button = ft.ElevatedButton(
        text="Стоп",
        on_click=stop_button_handler,
        style=ft.ButtonStyle(bgcolor=ft.colors.RED_400, color=ft.colors.WHITE),
        tooltip="Останавливает бесконечный сбор артефактов.",
    )

    save_button = ft.ElevatedButton(text="Сохранить настройки", on_click=on_save, width=220, style=ft.ButtonStyle(
        bgcolor=ft.colors.GREEN_600, color=ft.colors.WHITE))

    wait_time_field = ft.TextField(label="Время ожидания (в секундах)", value=str(wait_time), width=200)

    page.on_close = on_close

    controls = ft.Column(
        controls=[
            label,
            start_button,
            timer_label,
            empty_label,
            wait_time_field,
            save_button,
            stop_button,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=30,
    )

    page.add(ft.Stack([controls]))


""" find cursor """
# x, y = pyautogui.position()
#
# print(f"Координаты курсора: x={x}, y={y}")
