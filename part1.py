from ursina import *
from multiprocessing import Array, Value
import socket

# Класс для проверки подключения
class Connection:
    @staticmethod
    def test_connection(ip, port):
        try:
            with socket.create_connection((ip, int(port)), timeout=5):
                return True
        except:
            return False

# Класс главного меню
class MainMenu(Entity):
    def __init__(self, ip_var, port_var, status_var):
        super().__init__()
        self.ip_var = ip_var
        self.port_var = port_var
        self.status_var = status_var

        # Поля ввода IP и порта
        self.ip_input = InputField(text='127.0.0.1', position=(-0.4, 0), scale=(0.5, 0.05))
        self.port_input = InputField(text='8080', position=(0.2, 0), scale=(0.5, 0.05))
        
        # Кнопка подключения
        self.connect_button = Button(text="Connect", position=(0, -0.1), scale=(0.3, 0.1), on_click=self.connect)
        
        # Текст статуса подключения
        self.connection_status = Text(text='', position=(0, -0.2), origin=(0, 0), color=color.red)

    def connect(self):
        ip = self.ip_input.text
        port = self.port_input.text

        # Проверяем подключение
        if Connection.test_connection(ip, port):
            self.connection_status.text = "Succes connect"

            # Сохраняем данные в общие переменные
            self.ip_var.value = ip.encode('utf-8')
            self.port_var.value = port.encode('utf-8')
            self.status_var.value = 1  # Устанавливаем статус успешного подключения
        else:
            self.connection_status.text = "error connect. Check ip and the port"

# Функция для запуска первой части кода
def run_part1(ip_var, port_var, status_var):
    app = Ursina()
    main_menu = MainMenu(ip_var, port_var, status_var)
    app.run()
