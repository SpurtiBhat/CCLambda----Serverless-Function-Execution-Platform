import docker
from queue import Queue

client = docker.from_env()

# Pool of running container IDs
container_pool = Queue()

def create_container_pool(pool_size=2):
    for _ in range(pool_size):
        container = client.containers.run(
            "python:3.9-slim",
            command="tail -f /dev/null",
            detach=True,
            tty=True,
            remove=False,
            name=f"pool-{_}"
        )
        container_pool.put(container.id)
        print(f"Started container {container.id}")

def execute_in_pooled_container(code: str, timeout: float = 3.0):
    container_id = container_pool.get()
    container = client.containers.get(container_id)

    with open("temp.py", "w") as f:
        f.write(code)

    result = container.exec_run(f"python temp.py", demux=True)
    container_pool.put(container_id)  # Recycle

    stdout, stderr = result.output
    return (stdout or b'').decode() + (stderr or b'').decode()

# Call this on app start
create_container_pool()
