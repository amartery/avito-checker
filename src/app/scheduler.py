from time import time
from threading import Thread, Event, Lock
from queue import PriorityQueue, Empty
import itertools


class Task(object):
    def __init__(self, delay, function, args=(), kwargs={}):
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.delay = delay

    def complete_task(self):
        return self.function(*self.args, **self.kwargs)

    def time_to_execute(self):
        return time() + self.delay


class Scheduler(Thread):

    def default_fun(*args, **kwargs):
        pass

    default_task = Task(0, default_fun)

    def __init__(self):
        Thread.__init__(self)
        self.entry_finder = {}
        self.tasks = PriorityQueue()  # PriorityQueue() потокобезопасный класс

        self.new_task = Event()

        self.create_lock = Lock()
        self.id_generator = itertools.count()

    def add_task(self, task):
        timestamp = task.time_to_execute()
        if timestamp:
            with self.create_lock:
                id_task = next(self.id_generator)
                entry = [timestamp, id_task, task]
                self.entry_finder[task] = entry
                self.tasks.put(entry)
            self.new_task.set()

    def schedule_task(self, *args, **kwargs):
        task = Task(*args, **kwargs)
        self.add_task(task)
        return task

    def run(self):
        self.new_task.clear()
        while True:
            try:
                # timeout создает блокировку на 1 секунду
                timestamp, id_task, task = self.tasks.get(timeout=1)
                # если время выполнения задачи еще не наступило, возвращаем задачу назад в очередь
                if self.new_task.wait(timestamp - time()):
                    self.tasks.put([timestamp, id_task, task])
                    self.new_task.clear()
                else:
                    # ессли время наступило и необходмо исполнить задачу
                    if task is not self.default_task:
                        del self.entry_finder[task]
                        task.complete_task()
            # очередь пуста, ждем задачи
            except Empty:
                self.new_task.wait(10)
