import psutil


def check_system_memory(threshold=85):
    """
    Warn when overall system memory usage reaches
    the configured percentage.
    """
    memory = psutil.virtual_memory()

    return {
        "alert": memory.percent >= threshold,
        "memory_percent": memory.percent,
        "threshold": threshold,
        "message": (
            f"System memory usage is {memory.percent:.1f}%."
            if memory.percent >= threshold
            else "System memory usage is within the configured limit."
        ),
    }


def check_process_memory(pid, limit_mb=500):
    """
    Check whether a process exceeds a configured RSS limit.
    This function does not terminate or modify the process.
    """
    try:
        process = psutil.Process(pid)
        memory_mb = process.memory_info().rss / (1024 ** 2)

        return {
            "pid": pid,
            "process": process.name(),
            "memory_mb": round(memory_mb, 2),
            "alert": memory_mb >= limit_mb,
            "threshold_mb": limit_mb,
            "message": (
                f"PID {pid} exceeds the {limit_mb} MB memory limit."
                if memory_mb >= limit_mb
                else f"PID {pid} is within the configured memory limit."
            ),
        }

    except (psutil.NoSuchProcess, psutil.AccessDenied) as exc:
        return {
            "pid": pid,
            "alert": False,
            "message": f"Cannot inspect PID {pid}: {exc}",
        }


def get_prevention_recommendations(system_alert, process_alert):
    """
    Provide recommendations without taking automatic action.
    """
    recommendations = []

    if system_alert:
        recommendations.append(
            "System memory is high. Inspect running applications "
            "and close unnecessary applications safely."
        )

    if process_alert:
        recommendations.append(
            "Inspect the process for sustained memory growth. "
            "Save your work before restarting any application."
        )

    if not recommendations:
        recommendations.append(
            "No memory threshold alerts. Continue monitoring "
            "for sustained memory growth."
        )

    return recommendations
