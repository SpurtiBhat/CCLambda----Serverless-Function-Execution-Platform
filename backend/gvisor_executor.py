def execute_gvisor(code: str):
    container = client.containers.run(
        image="python:3.9",
        command="python /app/temp.py",
        volumes={os.getcwd(): {"bind": "/app", "mode": "rw"}},
        runtime="runsc",  # Only on Linux
        remove=True
    )
    return container.logs().decode()
