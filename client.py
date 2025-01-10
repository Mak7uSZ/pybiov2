from ursina import *
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

# Класс игры
class Game(Entity):
    def __init__(self):
        super().__init__()
        self.enabled = True
        self.player = Entity(model='cube', color=color.red, position=(0, 0, 0))
        self.camera.position = (0, 5, -10)
        self.camera.look_at(self.player)

    def update(self):
        self.player.rotation_y += 1  # Поворот игрока для примера

# Класс главного меню
class MainMenu(Entity):
    def __init__(self):
        super().__init__()
        self.enabled = True
        self.ip_input = InputField(text='127.0.0.1', position=(-0.4, 0), scale=(0.5, 0.05))
        self.port_input = InputField(text='8080', position=(0.2, 0), scale=(0.5, 0.05))
        self.connect_button = Button(text="Подключиться", position=(0, -0.1), scale=(0.3, 0.1), on_click=self.connect)
        self.connection_status = Text(text='', position=(0, -0.2), origin=(0, 0), color=color.red)
    
    def connect(self):
        ip = self.ip_input.text
        port = self.port_input.text

        if Connection.test_connection(ip, port):
            self.connection_status.text = "Подключение успешно!"
            self.enabled = False  # Скрыть главное меню
            self.start_game()  # Запуск игры после успешного подключения
        else:
            self.connection_status.text = "Ошибка подключения. Проверьте IP и порт."
    
    def start_game(self):
        # Переключаемся на игровую сцену
        game_scene = Game()  # Создаем экземпляр игры
        self.enabled = False  # Скрываем главное меню
        game_scene.enabled = True  # Показываем сцену игры

app = Ursina()

# Создание главного меню
main_menu = MainMenu()

app.run()
 