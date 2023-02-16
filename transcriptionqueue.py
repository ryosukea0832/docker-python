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
    

##########################################################
#move_to_wav_queue = TranscriptionQueue()
#cut_wav_queue = TranscriptionQueue()
#cut_wavs_str_queue = TranscriptionQueue()
#done_queue = TranscriptionQueue()
#threads = [
#    ChangeWorker(move_to_wav, move_to_wav_queue, cut_wav_queue),
#    ChangeWorker(cut_wav, cut_wav_queue, cut_wavs_str_queue),
#    ChangeWorker(cut_wavs_str, cut_wavs_str_queue, done_queue),
#]

# すべての入力作業が投入されたら、第一段階の入力キューを閉じて停止信号を送る
#for thread in threads:
#    thread.setDaemon(True)
#    thread.start()
#for _ in range(1000):
#    move_to_wav_queue.put(object())
#move_to_wav_queue.close()

# 各段階を結合してたキューをジョインして作業終了を待つ

#move_to_wav_queue.join()
#cut_wav_queue.close()
#cut_wav_queue.join()
#cut_wavs_str_queue.close()
#cut_wavs_str_queue.join()
#print(done_queue.qsize(), 'items finished')