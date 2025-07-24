from queue import Queue

pool = Queue()

def warm_pool(size=3):
    for _ in range(size):
        pool.put(docker.from_env().containers.run(...))

def execute_from_pool(code: str):
    container = pool.get()
    # Copy code into container & exec
    pool.put(container)
