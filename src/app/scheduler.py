from time import time
from threading import Thread, Event, Lock
from queue import PriorityQueue, Empty
import itertools


class Task(object):
    """A class used to represent some task"""
    def __init__(self, delay, function, args=(), kwargs={}):
        self.delay = delay
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def complete_task(self):
        """call the function with args, kwargs"""
        return self.function(*self.args, **self.kwargs)

    def time_to_execute(self):
        """calculating time for task execution"""
        return time() + self.delay


class Scheduler(Thread):
    """A this class is used to execute a Task after a certain time (delay)"""

    def _default_fun(*args, **kwargs):
        pass

    _default_task = Task(0, _default_fun)

    def __init__(self):
        Thread.__init__(self)
        self.id_generator = itertools.count()  # id generator

        self.entry_finder = {}  # dict stores metadata for task
        self.tasks = PriorityQueue()  # PriorityQueue() threadsafety class

        self.new_task = Event()  # flag for threads
        self.create_lock = Lock()  # lock for threads

    def _add_task(self, task: Task):
        timestamp = task.time_to_execute()  # calculating time for task execution
        if timestamp:
            with self.create_lock:
                id_task = next(self.id_generator)
                entry = [timestamp, id_task, task]
                self.entry_finder[task] = entry
                self.tasks.put(entry)
            self.new_task.set()  # raising the flag

    def schedule_task(self, *args, **kwargs) -> Task:
        """It takes many parameters (delay, function, (function_args,...))
        this method adds the task to the execution loop
        Parameters
        ----------
        delay - time after which it will be executed function
        function - function to perform
        (function_args,...) - function`s arguments
        Returns
        -------
        Task
            some created task
        """
        task = Task(*args, **kwargs)
        self._add_task(task)
        return task

    def run(self):
        self.new_task.clear()  # lowering the flag
        while True:  # the execution loop
            try:
                # timeout creates a lock for 1 second
                timestamp, id_task, task = self.tasks.get(timeout=1)
                # if the task has not been completed yet, return the task back to the queue
                if self.new_task.wait(timestamp - time()):
                    self.tasks.put([timestamp, id_task, task])
                    self.new_task.clear()
                else:
                    # if the time has come and you need to complete the task
                    if task is not self._default_task:
                        del self.entry_finder[task]
                        task.complete_task()
            # the queue is empty, waiting for a task
            except Empty:
                self.new_task.wait(10)
