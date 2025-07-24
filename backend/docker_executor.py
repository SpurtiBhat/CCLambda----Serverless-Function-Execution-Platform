import docker
import uuid

client = docker.from_env()

def execute_docker(code: str):
    file_name = f"temp_{uuid.uuid4().hex[:6]}.py"
    with open(file_name, "w") as f:
        f.write(code)
    
    container = client.containers.run(
        image="python:3.9",
        command=f"python /app/{file_name}",
        volumes={os.getcwd(): {"bind": "/app", "mode": "rw"}},
        remove=True
    )
    return container.decode()
