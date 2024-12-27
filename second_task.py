# На языке Python или С++ написать минимум по 2 класса реализовывающих циклический буфер FIFO.
# Объяснить плюсы и минусы каждой реализации.
from collections import deque


class Buffer:
    """
    Класс реализующий циклический буфер FIFO. Применяется метод массива,
    в котором применяются встроенные функции pop и append.
    Удаляется первый элемент и добавляется новый в конец массива.
    Плюсы:
    - используется один указатель (линейная очередь требует двух указателей
    - простота реализации
    - возможность обработки линейных данных в исходном порядке их получения
    Минусы:
    - ограниченность буфера количеством элементов
    - сложно работы с нелинейными данными
    - сложнее отлаживать, чем другие структуры данных
    """

    def __init__(self, size):
        self.data = [None for i in range(size)]

    def append(self, value):
        self.data.pop(0)
        self.data.append(value)

    def get(self):
        return self.data


buf = Buffer(4)
for i in range(10):
    buf.append(i)
    print(buf.get())


class CircularBuffer:
    """
    Класс реализующий циклический буфер FIFO. Метод переменных,
    помимо тела массива хранится начало и конец буфера
    :param k: длина буфера
    :param head: начало буфера
    :param tail: конец буфера
    :param queue: тело буфера
    Плюсы:
    """

    def __init__(self, k):
        self.k = k
        self.queue = [None] * k
        self.head = self.tail = -1

    def add_element(self, data):
        """
        Функция добавления элемента в циклический буфер.
        Плюсы:
        - Эффективность по времени: Добавление и удаление элементов выполняются за O(1).
        - Фиксированный размер: Легче контролировать объем используемой памяти.
        - Подходит для многопоточных систем: Такой подход широко используется в системах реального времени.
        - Эффективное использование памяти: Буфер перезаписывает старые данные, избегая динамического увеличения размера.
        Минусы:
        - Сложность реализации: Требуется ручное управление указателями, что может быть сложно для новичков.
        - Трудности с отладкой: Логика циклического поведения указателей может запутывать при поиске ошибок.
        - Ограничения на размер данных: Необходима явная проверка переполнения буфера.
        :param data:
        :return:
        """

        if (self.tail + 1) % self.k == self.head:
            print("Буфер заполнен\n")

        elif self.head == -1:
            self.head = 0
            self.tail = 0
            self.queue[self.tail] = data
        else:
            self.tail = (self.tail + 1) % self.k
            self.queue[self.tail] = data

    def delete_element(self):
        """
        Функция удаления элемента из циклического буфера
        """
        if self.head == -1:
            print("Буфер пуст\n")

        elif self.head == self.tail:
            temp = self.queue[self.head]
            self.head = -1
            self.tail = -1
            return temp
        else:
            temp = self.queue[self.head]
            self.head = (self.head + 1) % self.k
            return temp

    def print_buffer(self):
        if self.head == -1:
            print("Буфер пуст\n")

        elif self.tail >= self.head:
            for i in range(self.head, self.tail + 1):
                print(self.queue[i], end=" ")
            print()
        else:
            for i in range(self.head, self.k):
                print(self.queue[i], end=" ")
            for i in range(0, self.tail + 1):
                print(self.queue[i], end=" ")
            print()


obj = CircularBuffer(5)

# adding data to the queue
for i in range(1, 6):
    obj.add_element(i)

print("Вывод буфера:")
obj.print_buffer()

print("\nУдалено значение:", obj.delete_element())
print("Удалено значение:", obj.delete_element())

print("\n2 значения удалены из буфера")
print("В новом теле буфера 3 значения:")
obj.print_buffer()


class DequeCircularBuffer:
    """
    Реализация циклического буфера FIFO с использованием collections.deque.
    Плюсы:
    - Простота и лаконичность реализации.
    - Высокая производительность: добавление и удаление элементов выполняются за O(1).
    - Автоматическое управление размером буфера через maxlen.
    Минусы:
    - Меньший контроль над внутренними процессами (делегирование функций deque).
    - Не подходит для сложной логики, требующей управления указателями.
    """
    def __init__(self, size):
        self.buffer = deque(maxlen=size)

    def append(self, value):
        """Добавляет элемент в буфер, удаляя самый старый, если буфер заполнен."""
        self.buffer.append(value)

    def get(self):
        """Возвращает текущие элементы буфера в виде списка."""
        return list(self.buffer)

buf = DequeCircularBuffer(5)
for i in range(7):
    buf.append(i)
    print(f"Буфер: {buf.get()}")