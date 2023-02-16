from threading import Thread
from queue import Queue

class TranscriptionQueue(Queue):
    SENTINEL = object()

    def close(self):
        self.put(self.SENTINEL)

    def __iter__(self):
        while True:
            item = self.get()
            try:
                if item is self.SENTINEL:
                    return # スレッドを終了させる
                yield item
            finally:
                self.task_done()

class ChangeWorker(Thread):
    def __init__(self, func, in_queue, out_queue):
        super().__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue

    def run(self):
        for item in self.in_queue:
            results = self.func(item)
            self.out_queue.put(results)
    