import threading

# class server_worker() that will start off an active and a passive socket/threads at the server worker node

class server_worker(threading.Thread):
    def __init__(self, port, queue, function):
        threading.Thread.__init__(self)
        self.queue = queue
        self.port = port
        self.function = function


    def run(self):
            # depending on the output you put something on the queeu or you don't
            self.function()