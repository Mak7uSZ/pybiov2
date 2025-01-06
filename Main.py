from multiprocessing import Process, Value, Array
import subprocess
import time
from part1 import run_part1
import random

def generate_port():
    """Генерация случайного порта"""
    return random.randint(1025, 65535) 

if __name__ == "__main__":
    generated_port = generate_port()
    print(f"Generated port in Main.py: {generated_port}")

    # Общие переменные
    ip_var = Array('c', 15)  # Хранение IP
    port_var = Array('c', 5)  # Хранение порта
    status_var = Value('i', 0)  # Статус подключения
    generated_port_value = Value('i', generated_port)  # Сгенерированный порт

    # Запускаем part1.py
    part1_process = Process(target=run_part1, args=(ip_var, port_var, status_var, generated_port_value))
    part1_process.start()
    part1_process.join()

    # Ожидаем успешного подключения
    while status_var.value == 0:
        time.sleep(0.5)

    # Конвертируем данные из bytes в str
    ip = ip_var.value.decode('utf-8').strip()
    port = port_var.value.decode('utf-8').strip()

    print(f"succes connection: IP={ip}, PORT={port}")

    # Завершаем part1.py
    part1_process.terminate()

    # Запускаем game.py
    subprocess.run(["python", "game.py", ip, port])