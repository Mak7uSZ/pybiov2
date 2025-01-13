import subprocess
import socket
import time
from ursina import *
import threading
from pathlib import Path
import requests
import sys
import os

class MainMenu(Entity):
    def __init__(self, generated_port_value, ip_var=None, port_var=None, status_var=None):
        super().__init__()
        self.enabled = True
        
        # Инициализация переменных
        self.ip_var = ip_var
        self.port_var = port_var
        self.status_var = status_var
        self.generated_port_value = generated_port_value
        print(f"Received generated port in part1.py: {self.generated_port_value.value}")
        
        welcome_text = Text("PyGame Biologie V2.0", scale=3)
        welcome_text.world_position = (-6.6, 6)

        # Кнопка для создания сервера   
        self.create_server_button = Button(text="create server", position=(0, 0.1), scale=(0.3, 0.1), on_click=self.create_server)
        
        # Кнопка для подключения
        self.connect_button = Button(text="connect to server", position=(0, -0.1), scale=(0.3, 0.1), on_click=self.connect_to_server)
        
        # Поля ввода IP и порта (только для подключения)
        ip_text = Text("IP", scale=1)
        ip_text.world_position = (-8, -4.5)
        self.ip_input = InputField(text='127.0.0.1', position=(-0.4, -0.3), scale=(0.5, 0.05))
        port_text = Text("PORT", scale=1)
        port_text.world_position = (3, -4.5)
        self.port_input = InputField(text='8080', position=(0.2, -0.3), scale=(0.5, 0.05))
        
        # Отключаем поля ввода IP и порта до того, как выберется опция подключения
        self.ip_input.enabled = True
        self.port_input.enabled = True
        
    def create_server(self):
        """Создание локального сервера и подключение к нему"""
        def server_thread():
            """Функция, которая будет запускать сервер в отдельном потоке"""
            print("creating server...")
            generated_port = int(self.generated_port_value.value)
            print(f"Using generated port in server_thread: {generated_port}")
            # Запускаем сервер в фоновом процессе
            process = subprocess.Popen(["python", "server.py", str(generated_port)])  # Используем Popen, чтобы процесс продолжался в фоновом режиме

            # Ожидаем некоторое время, чтобы сервер успел запуститься (например, 1 секунда)
            time.sleep(5)  # Можно регулировать время в зависимости от того, сколько времени требуется серверу для старта

            if process.poll() is None:
                print("server works!")
            else:
                print("server didnt start!")

            # Get the public IP address by querying an external service
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname) 
            ip = local_ip

# Get the public IP address
            print(f"server started on {ip}:{generated_port}")

            # Запускаем game.py с IP и случайным портом
            self.run_game(ip, generated_port)
            time.sleep(5)

        # Создаем и запускаем отдельный поток для сервера
        server_thread_instance = threading.Thread(target=server_thread)
        server_thread_instance.start()
        
    def connect_to_server(self):
        ip = self.ip_input.text
        port = self.port_input.text

        print(f"COnnecting to server {ip}:{port}")
            
            # Проверяем, доступен ли сервер
        try:
            if self.test_connection(ip, port):
                print("Successful connection!")
                self.run_game(ip, port)
            else:
                print("Error: Connection failed!")
        except Exception as e:
            print(f"Error connection: {e}")
            # Clear the input fields or display an error message
            self.ip_input.text = ''
            self.port_input.text = ''

            

    def run_game(self, ip, port):
        """Запуск игры"""
        # Получаем путь к текущей директории проекта
        project_dir = Path(__file__).parent

        # Путь к файлу game.py в корне проекта
        file_path = project_dir / 'game.py'

        # Проверяем, существует ли файл
        if not file_path.exists():
            print(f"Ошибка: Файл {file_path} не найден.")
            return

        # Выводим путь к файлу
        print(f"Путь к файлу: {file_path}")

        # Запускаем скрипт с переданными параметрами
        print(f"Запуск сервера с параметрами: {ip}:{port}")
        subprocess.Popen(["python", str(file_path), ip, str(port)])
        time.sleep(5)

    @staticmethod
    def test_connection(ip, port):        
            try:
                with socket.create_connection((ip, int(port)), timeout=5):
                    return True
            except:
                    return False

def run_part1(ip_var, port_var, status_var, generated_port_value):
    app = Ursina()
    main_menu = MainMenu(ip_var=ip_var, port_var=port_var, status_var=status_var, generated_port_value=generated_port_value)
    app.run()