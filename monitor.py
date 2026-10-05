import psutil


def get_system_memory():
    memory = psutil.virtual_memory()

    return {
        "total": memory.total,
        "available": memory.available,
        "used": memory.used,
        "free": memory.free,
        "percent": memory.percent
    }


def get_process_memory():
    processes = []

    for process in psutil.process_iter(
        ["pid", "name", "memory_info"]
    ):
        try:
            info = process.info
            memory_info = info["memory_info"]

            processes.append({
                "pid": info["pid"],
                "name": info["name"],
                "memory": memory_info.rss
            })

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied
        ):
            continue

    return processes
