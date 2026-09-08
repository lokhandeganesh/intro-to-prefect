import resource


def format_memory(bytes_value):
    """Converts bytes into a human-readable string (KB, MB, GB)."""
    # Handles negative consumption if memory drops during execution
    abs_value = abs(bytes_value)

    if abs_value >= 1024**3:
        value = bytes_value / (1024**3)
        unit = "GB"
    elif abs_value >= 1024**2:
        value = bytes_value / (1024**2)
        unit = "MB"
    elif abs_value >= 1024:
        value = bytes_value / 1024
        unit = "KB"
    else:
        value = bytes_value
        unit = "B"

    return f"{value:.2f} {unit}"


def get_system_peak_memory():
    # resource.getrusage returns maxrss in KILOBYTES on Linux systems
    max_rss_kb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    max_rss_bytes = max_rss_kb * 1024

    # Reusing your format_memory logic
    return format_memory(max_rss_bytes), max_rss_bytes

def log_final_peak(flow, flow_run, state):
    """Prefect hook that runs automatically the moment the flow finishes."""
    max_rss_kb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    peak_str = format_memory(max_rss_kb * 1024)

    print(f"True MAXIMUM PROCESS PEAK:- {peak_str}")
