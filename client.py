from ursina import *

# Функция для обработки нажатия кнопки
def connect():
    ip = ip_input.text
    port = port_input.text
    if ip and port.isdigit():
        print(f"[INFO] Попытка подключения к {ip}:{port}")
    else:
        print("[ERROR] Введите корректные IP-адрес и порт.")

# Функция для проверки наведения мыши
def update():
    if connect_button.hovered:
        print("[DEBUG] Мышь наведена на кнопку.")  # Сообщение при наведении мыши на кнопку

# Создаем приложение
app = Ursina()

# Включаем курсор
mouse.visible = True

# Камера в 2D
camera.orthographic = True
camera.fov = 10

# Фон
background = Entity(parent=camera.ui, model='quad', texture='white_cube', scale=(1.5, 1), color=color.dark_gray)

# Заголовок
title = Text("Главное меню", parent=camera.ui, y=0.4, origin=(0, 0), scale=2, color=color.white)

# Поле ввода для IP-адреса
ip_input = InputField(parent=camera.ui, y=0.2, placeholder='Введите IP-адрес', scale=(0.5, 0.1))

# Поле ввода для порта
port_input = InputField(parent=camera.ui, y=0, placeholder='Введите порт', scale=(0.5, 0.1))

# Кнопка подключения
connect_button = Button(parent=camera.ui, scale=(0.3, 0.1), color=color.azure, text="Подключиться", y=-0.2)
connect_button.on_click = connect  # Привязываем функцию к кнопке

# Запуск приложения
app.run()
