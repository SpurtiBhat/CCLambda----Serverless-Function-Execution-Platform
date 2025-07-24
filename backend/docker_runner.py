import subprocess

def get_docker_command(image_name, timeout, mount_dir=None, use_gvisor=False):
    cmd = [
        "docker", "run", "--rm",
        "--network", "none",
        "--memory", "256m",
        "--cpus", "0.5",
        "--pids-limit", "64",
    ]

    if use_gvisor:
        cmd += ["--runtime=runsc"]  # Enable gVisor runtime

    if mount_dir:
        cmd += ["-v", f"{mount_dir}:/app"]

    cmd += [image_name]

    return cmd

def run_function_docker(image_name, timeout=10, mount_dir=None, use_gvisor=False):
    cmd = get_docker_command(image_name, timeout, mount_dir, use_gvisor)
    
    try:
        result = subprocess.run(
            cmd, capture_output=True, timeout=timeout, text=True
        )
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {"error": "Function timed out"}
