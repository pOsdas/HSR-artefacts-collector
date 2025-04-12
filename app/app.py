import flet as ft
import pyautogui
import threading
import time
import os
import json
import sys


def resource_path(relative_path) -> str | bytes:
    """ 
    Получить абсолютный путь к ресурсам, работает с dev и PyInstaller 
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


config_file = 'config.json'


def load_config() -> dict:
    """
    Получить время ожидания
    """
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            return json.load(f)
    else:
        return {'wait_time': 80}


def save_config(configs):
    """
    Сохранить время ожидания
    """
    with open(config_file, 'w') as f:
        json.dump(configs, f)
        
        
stop_program = False
config = load_config()
wait_time = config['wait_time']


def main(page: ft.Page):
    """
    EI Дизайн
    """
    page.title = "Honkai Artefacts collect"
    page.window_always_on_top = True
    page.window_width = 300
    page.window_height = 550
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
        """
        Сохранение данных в json
        """
        config['wait_time'] = int(wait_time_field.value)
        save_config(config)
        page.snack_bar = ft.SnackBar(ft.Text("Настройки сохранены"), open=True)
        page.update()
        print("config has been updated")

    def countdown(start_seconds, callback):
        """ 
        Время на то, чтобы открыть игру 
        """
        for i in range(start_seconds, 0, -1):
            timer_label.value = f"Таймер: {i} секунд"
            page.update()
            time.sleep(1)
        timer_label.value = "Начинаем автоматизацию"
        page.update()
        callback()

    def click_center():
        """
        Клик в центр экрана
        """
        screenWidth, screenHeight = pyautogui.size()
        center_x = screenWidth // 2
        center_y = screenHeight // 2
        pyautogui.click(center_x, center_y)

    def perform_actions_short():
        """
        Действия на 300 смолы
        """
        click_center()

        x_coordinate, y_coordinate = 1183, 952  # approximate coordinates of the button
        interval = load_config()

        global stop_program
        while not stop_program:
            pyautogui.click(x_coordinate, y_coordinate)
            print(f"Клик выполнен в координатах ({x_coordinate}, {y_coordinate})")
            time.sleep(interval['wait_time'])

    def perform_actions_long():
        """
        Действия на больше смолы
        """

        click_center()
        interval = load_config()

        while True:
            for i in range(7):
                click_center()
                pyautogui.click(1183, 952)
                time.sleep(interval['wait_time'])

            # После семи итераций выполняем пополнение смолы:
            pyautogui.click(1760, 66)
            time.sleep(0.5)
            pyautogui.click(1099, 735)
            time.sleep(0.5)
            pyautogui.click(1017, 615)
            time.sleep(0.5)
            pyautogui.write("280", interval=0.1)  # взять 280 смолы
            pyautogui.click(1109, 786)
            time.sleep(0.5)
            click_center()

    def start_button_short_handler(e):
        """
        Логика кнопки 'старт короткий'
        """
        global stop_program
        stop_program = False
        threading.Thread(
            target=countdown, args=(10, lambda: threading.Thread(target=perform_actions_short).start())
        ).start()
        print("start button short")

    def start_button_long_handler(e):
        """
        Логика кнопки 'старт длинный'
        """
        global stop_program
        stop_program = False
        threading.Thread(
            target=countdown, args=(10, lambda: threading.Thread(target=perform_actions_long).start())
        ).start()
        print("start button long")

    def stop_button_handler(e):
        """
        Логика кнопки 'стоп'
        """
        global stop_program
        stop_program = True
        print("stop button")

    def on_close(e):
        print("Приложение закрыто")
        page.window_close()

    # Кнопка старт 'короткая'
    start_button_short = ft.ElevatedButton(
        text="Старт 'короткий'",
        on_click=start_button_short_handler,
        style=ft.ButtonStyle(bgcolor=ft.colors.INDIGO_500, color=ft.colors.WHITE),
        tooltip=description,
    )

    # Кнопка старт 'длинная'
    start_button_long = ft.ElevatedButton(
        text="Старт 'длинный'",
        on_click=start_button_long_handler,
        style=ft.ButtonStyle(bgcolor=ft.colors.INDIGO_500, color=ft.colors.WHITE),
        tooltip=description,
    )

    # Кнопка стоп
    stop_button = ft.ElevatedButton(
        text="Стоп",
        on_click=stop_button_handler,
        style=ft.ButtonStyle(bgcolor=ft.colors.RED_400, color=ft.colors.WHITE),
        tooltip="Останавливает бесконечный сбор артефактов.",
    )

    # Кнопка сохранения
    save_button = ft.ElevatedButton(text="Сохранить настройки", on_click=on_save, width=220, style=ft.ButtonStyle(
        bgcolor=ft.colors.GREEN_600, color=ft.colors.WHITE))

    # Поле времени
    wait_time_field = ft.TextField(label="Время ожидания (в секундах)", value=str(wait_time), width=200)

    page.on_close = on_close

    controls = ft.Column(
        controls=[
            label,
            start_button_short,
            start_button_long,
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
