from collections import deque
from multiprocessing.managers import SharedMemoryManager
from multiprocessing import Process, Pipe
from bin.engine import taskqueue
from bin.game import tasks
import functools
import pickle
import time

from threading import Thread


MAX_THREAD_COUNT = 2
MEMORY_HEAP_SIZE = 4096

GLOBAL_MEMORY_UNIT = "boolsonly"
CONNECTED_SMM_NAME = None
MAIN_THREAD_GAME_RUNNING = 0
TASK_QUEUE_THREAD_RUNNING = 1

PROCESS_SHARED_ARRAY_SPACE = 4


class TempVar:
    def __init__(self):
        pass


class MultiProcessMemoryHandler:
    def __init__(self, unit=None):
        """Initialize MultiProcessMemoryHandler object"""
        self.smm = SharedMemoryManager(address=unit)
        if not unit:
            global CONNECTED_SMM_NAME
            CONNECTED_SMM_NAME = self.smm.address
        self.smm.start()
        self.process = {}
        # shared memory units
        self.smu = {}
        # shareable arrays
        self.sa = {}
        # pipes
        self.pipes = {}
        # TODO - IMPLEMENT POOLS
        # when looking for tasks, just loop through the available processes
        # if there is an inactive process, activate and use to run task
        # if no available processes, store tasks in a queue
        # task queue :D

    def begin_processes(self):
        """Starts all processes"""
        for p in self.process.values():
            p.start()

    def add_process(self, target, args, shared_mem_unit=None, name=None, daemon=False):
        """Add a new process"""
        arguments = [_ for _ in args]
        if shared_mem_unit:
            [arguments.append(self.get_shared_memory_unit(s)) for s in shared_mem_unit]
        process = Process(name=str(name), target=target, args=tuple(arguments), daemon=daemon)
        self.process[name] = process
        return process

    def make_shared_memory_unit(self, name, size):
        """Make a new shared memory unit"""
        self.smu[name] = self.smm.SharedMemory(size=size)

    def get_shared_memory_unit(self, name):
        """Get a shared memory unit"""
        return self.smu.get(name)

    def make_shareable_array(self, name, size):
        """Creates and caches shareable array"""
        self.sa[name] = self.smm.ShareableList([None for i in range(size)])

    def get_shareable_array(self, name):
        """Returns shareable array"""
        return self.sa.get(name)

    def create_pipe(self, name, duplex=False):
        """Create a pipe object"""
        client, host = Pipe(duplex)
        self.pipes[name] = (host, client)
        return host, client

    def get_pipe(self, name):
        """Returns pipe host and client"""
        return self.pipes.get(name)

    def close(self):
        """Join and close all processes and shared memory units"""
        # join processes
        for p in self.process.values():
            try:
                p.join()
                p.close()
            finally:
                continue

        # clear pipes
        for h, c in self.pipes.values():
            try:
                h.close()
                c.close()
            finally:
                continue

        # shutdown the shared memory
        self.smm.shutdown()

        # clear all caches
        self.process.clear()
        self.smu.clear()
        self.pipes.clear()


class MultiThreadedTaskHandler:
    def __init__(self, max_threads=1):
        """Create a MultiThreadedTaskHandler"""
        # task queue - stores taskqueue.Task objects
        self.task_queue = deque()
        # memory manager
        self.Manager = MultiProcessMemoryHandler()
        # create initial memory queue to keep count of each active process
        self.Manager.make_shared_memory_unit("local", size=max_threads*2 + 1)
        self.shared_memory = self.Manager.get_shared_memory_unit("local")
        # set all to false
        self.max_threads = max_threads
        for i in range(1, max_threads*2+1):
            self.shared_memory.buf[i] = False
        # print([type(x) for x in self.shared_memory.buf])
        # results - its gonan only store pickled strings cuz they are byte form and cool
        # print([type(e) for e in self.results])
        # print([type(e) for e in self.results])
        self.threads = {}
        self.active = TempVar()
        self.active.active = True

    def start(self, world):
        """Start the shared memory unit and set the first pointer to True"""
        self.shared_memory.buf[0] = True
        # create processes
        for i in range(1, self.max_threads+1):
            self.shared_memory.buf[i] = True
            # to send data to process
            tsend, trec = self.Manager.create_pipe(f"{i}to")
            # to send from process to thread
            fsend, frec = self.Manager.create_pipe(f"{i}from")
            # make
            data = TempVar()
            data.send = fsend; data.rec = trec; data.thread_count = self.max_threads
            self.Manager.add_process(target=taskqueue.handle_tasks,
                                     args=(self.shared_memory, data, i,),
                                     name=i).start()

        # create threads that recieve each of the chagnes
        for i in range(1, self.max_threads+1):
            fsend, frec = self.Manager.get_pipe(f"{i}from")
            self.make_thread(name=i, task=taskqueue.test, args=(self.active, world, frec),
                             tname=f"Thread Process {i}")
            self.get_thread(i).start()

        # create task uplaod thread
        self.make_thread(name="taskhandler", task=self.update_tasks, args=(),
                         tname="Task Handler Thread")
        self.get_thread("taskhandler").start()

    def end(self):
        """Sets all running variables to false to close all running processes"""
        self.shared_memory.buf[0] = False
        # send an abort message
        for i in range(1, self.max_threads+1):
            self.shared_memory.buf[i+self.max_threads] = False
            send, rec = self.Manager.get_pipe(f"{i}to")
            send.send((tasks.EndProcess, ()))
            # print([int(x) for x in self.shared_memory.buf])
        # close threads
        self.active.active = False
        self.Manager.close()
        print("closed")
        self.task_queue.clear()

    def close(self):
        """Close the Manager and threads"""
        self.get_thread("taskhandler").join()
        for thread in self.threads.values():
            thread.join()

    def find_available_process(self):
        for i in range(1, self.max_threads+1):
            # check if that process isnt working
            if self.shared_memory.buf[i] and self.shared_memory.buf[i+self.max_threads]:
                # if thread is alive and paused, we can send
                # send the task to that thread
                return i
        return None

    def get_thread(self, name):
        return self.threads.get(name)

    def make_thread(self, name, task, args, tname=None):
        self.threads[name] = Thread(target=task, args=args, name=tname)

    def add_task(self, task, args):
        """Create and run tasks"""
        # add task to task queue
        # print(task, args)
        self.task_queue.append((task, args))

    def update_tasks(self):
        # recieve changes
        # TODO - RECIEVE CHANGES
        # add tasks
        while self.active.active:
            if self.task_queue:
                i = self.find_available_process()
                if not i:
                    time.sleep(0.1)
                    continue
                self.shared_memory.buf[i+self.max_threads] = False
                tsend, trec = self.Manager.get_pipe(f"{i}to")
                if tsend:
                    task = self.task_queue.popleft()
                    # print(task)
                    tsend.send(task)
            else:
                time.sleep(0.1)


