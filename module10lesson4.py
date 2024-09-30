import threading
import time
from queue import Queue
from random import randint


# Класс, представляющий стол в кафе
class Table:
    def __init__(self, number):
        self.number = number  # Номер стола
        self.guest = None  # Гость, сидящий за столом (изначально нет гостя)


# Класс, представляющий гостя (наследуется от класса Thread)
class Guest(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name  # Имя гостя

    def run(self):
        # Имитируем, что гость сидит за столом случайное время от 3 до 10 секунд
        time_to_eat = randint(3, 10)
        time.sleep(time_to_eat)


# Класс Cafe, который управляет столами и очередью гостей
class Cafe:
    def __init__(self, *tables):
        self.tables = tables  # Список столов в кафе
        self.queue = Queue()  # Очередь для гостей, если нет свободных столов

    # Метод для приема гостей
    def guest_arrival(self, *guests):
        for guest in guests:
            # Ищем свободный стол
            free_table = next((table for table in self.tables if table.guest is None), None)
            if free_table:
                # Если есть свободный стол, сажаем гостя
                free_table.guest = guest
                guest.start()  # Запускаем поток гостя
                print(f"{guest.name} сел(-а) за стол номер {free_table.number}")
            else:
                # Если столов нет, ставим гостя в очередь
                self.queue.put(guest)
                print(f"{guest.name} в очереди")

    # Метод для обслуживания гостей
    def discuss_guests(self):
        while not self.queue.empty() or any(table.guest is not None for table in self.tables):
            for table in self.tables:
                if table.guest and not table.guest.is_alive():
                    # Если гость за столом закончил есть, освобождаем стол
                    print(f"{table.guest.name} покушал(-а) и ушёл(ушла)")
                    print(f"Стол номер {table.number} свободен")
                    table.guest = None

                    if not self.queue.empty():
                        # Если есть гости в очереди, пересаживаем одного из них за стол
                        next_guest = self.queue.get()
                        table.guest = next_guest
                        next_guest.start()
                        print(f"{next_guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}")

            # Делаем небольшую паузу перед следующим циклом, чтобы имитировать время обработки
            time.sleep(1)


# Пример использования
if __name__ == '__main__':
    # Создаем столы
    tables = [Table(number) for number in range(1, 6)]

    # Имена гостей
    guests_names = [
        'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
        'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
    ]

    # Создаем гостей
    guests = [Guest(name) for name in guests_names]

    # Создаем кафе и заполняем его столами
    cafe = Cafe(*tables)

    # Принимаем гостей
    cafe.guest_arrival(*guests)

    # Обслуживаем гостей
    cafe.discuss_guests()
