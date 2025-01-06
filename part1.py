import subprocess
import socket
import time
from ursina import *
import threading
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
        
        # Кнопка для создания сервера   
        self.create_server_button = Button(text="create server", position=(0, 0.1), scale=(0.3, 0.1), on_click=self.create_server)
        
        # Кнопка для подключения
        self.connect_button = Button(text="connect to server", position=(0, -0.1), scale=(0.3, 0.1), on_click=self.connect_to_server)
        
        # Поля ввода IP и порта (только для подключения)
        self.ip_input = InputField(text='127.0.0.1', position=(-0.4, -0.3), scale=(0.5, 0.05))
        self.port_input = InputField(text='8080', position=(0.2, -0.3), scale=(0.5, 0.05))
        
        # Отключаем поля ввода IP и порта до того, как выберется опция подключения
        self.ip_input.enabled = True
        self.port_input.enabled = True
        
    def create_server(self):
        """Создание локального сервера и подключение к нему"""
        def server_thread():
            """Функция, которая будет запускать сервер в отдельном потоке"""
            print("Создаем сервер...")
            generated_port = int(self.generated_port_value.value)
            print(f"Using generated port in server_thread: {generated_port}")
            # Запускаем сервер в фоновом процессе
            process = subprocess.Popen(["python", "server.py", str(generated_port)])  # Используем Popen, чтобы процесс продолжался в фоновом режиме

            # Ожидаем некоторое время, чтобы сервер успел запуститься (например, 1 секунда)
            time.sleep(1)  # Можно регулировать время в зависимости от того, сколько времени требуется серверу для старта

            if process.poll() is None:
                print("Сервер работает!")
            else:
                print("Сервер не запустился!")
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            ip = local_ip

# Get the public IP address
            print(f"Сервер запущен на {ip}:{generated_port}")

            # Запускаем game.py с IP и случайным портом
            self.run_game(ip, generated_port)

        # Создаем и запускаем отдельный поток для сервера
        server_thread_instance = threading.Thread(target=server_thread)
        server_thread_instance.start()
        
    def connect_to_server(self):
        """Подключение к существующему серверу"""
        ip = self.ip_input.text
        port = self.port_input.text

        print(f"Подключаемся к серверу {ip}:{port}")
        
        # Проверяем, доступен ли сервер
        if self.test_connection(ip, port):
            print("Подключение успешно!")
            self.run_game(ip, port)
        else:
            print("Ошибка подключения!")
            # Можно очистить поля ввода или отобразить сообщение о неудаче
            self.ip_input.text = ''
            self.port_input.text = ''
        
    def run_game(self, ip, port):
        """Запуск игры"""
        # Вы можете запускать свою игру, передавая параметры
        print(f"Запускаем игру с сервером {ip}:{port}")
        subprocess.Popen(["python", "game.py", ip, str(port)])
        self.close_menu()  # Закрываем главное меню после запуска игры
    
    def close_menu(self):
        """Закрытие главного меню"""
        self.enabled = False  # Отключаем главное меню
    
    @staticmethod
    def test_connection(ip, port):
        """Проверка доступности сервера по IP и порту"""
        try:
            with socket.create_connection((ip, int(port)), timeout=5):
                return True
        except:
            return False

def run_part1(ip_var, port_var, status_var, generated_port_value):
    app = Ursina()
    main_menu = MainMenu(ip_var=ip_var, port_var=port_var, status_var=status_var, generated_port_value=generated_port_value)
    app.run()