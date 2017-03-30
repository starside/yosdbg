import time
from multiprocessing import Process,  Queue, Manager

def initGui(q, que, td, events, outqueue):
    while True:
        print que.get()
        q.put("Go")
        time.sleep(1)

class DCont():
    def __init__(self, *args):
        assert (len(args) == 6)
        # read in comm channels
        self.async = args[5]  # synch or async mode
        self.que = args[2]
        self.events = args[4]
        self.timeDir = args[3]
        self.parent_conn = args[1]
        self.child_conn = args[0]

    @staticmethod
    def runMain(func):
        # create bidirectional comm channels
        manager = Manager()
        async = manager.dict()  # synch or async mode
        que = Queue()
        events = Queue()
        timeDir = None
        out_conn = Queue()
        in_conn = Queue()
        # run the simulation code in child process
        p = Process(target=func, args=(in_conn, out_conn, que, timeDir, events, async))
        # p.daemon = True
        p.start()
        # run gui in parent process
        initGui(in_conn, que, timeDir, events, async)

    # Low Level method to communicate with gui thread
    def say(self, obj):
        self.que.put(obj)
        return self.child_conn.get()

def main(*args):
    # init GUI
    pc = DCont(*args)  # Create GUI
    while True:
        print pc.say("o7")

DCont.runMain(main)