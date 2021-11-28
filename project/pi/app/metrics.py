import platform
import time

import psutil

from app.metric import Metric


def metrics(node: int):
    cpu = psutil.cpu_percent()
    cores = psutil.cpu_count()
    cores_physical = psutil.cpu_count(logical=False)
    memory = psutil.virtual_memory()
    boot_time = psutil.boot_time()
    system_time = time.time()
    tcp_connections = len(psutil.net_connections(kind='tcp'))
    partitions = psutil.disk_partitions()

    metrics_list = [Metric(
        metric_name="cpu_usage",
        metric_type="gauge",
        comment="CPU Usage in Percent",
        value=cpu,
        params={
            "node": f"{node}"
        }
    ), Metric(
        metric_name="cpu_cores",
        metric_type="gauge",
        comment="Total CPU Cores",
        value=cores,
        params={
            "type": "all",
            "node": f"{node}"
        }
    ), Metric(
        metric_name="cpu_cores",
        metric_type="gauge",
        comment="Total CPU Cores",
        value=cores_physical,
        params={
            "type": "physical",
            "node": f"{node}"
        }
    ), Metric(
        metric_name="boot_time",
        metric_type="gauge",
        comment="Time in sec since epoch",
        value=boot_time,
        params={
            "node": f"{node}"
        }
    ), Metric(
        metric_name="system_time",
        metric_type="gauge",
        comment="Time in sec since epoch",
        value=system_time,
        params={
            "node": f"{node}"
        }
    ), Metric(
        metric_name="tcp_connections",
        metric_type="gauge",
        comment="Number of TCP connections",
        value=tcp_connections,
        params={
            "node": f"{node}"
        }
    ), Metric(
        metric_name="memory_usage",
        metric_type="gauge",
        comment="Memory Usage Data",
        value=memory[0],
        params={
            "type": "total",
            "node": f"{node}"
        }
    ), Metric(
        metric_name="memory_usage",
        metric_type="gauge",
        comment="Memory Usage Data",
        value=memory[1],
        params={
            "type": "available",
            "node": f"{node}"
        }
    ), Metric(
        metric_name="memory_usage",
        metric_type="gauge",
        comment="Memory Usage Data",
        value=memory[3],
        params={
            "type": "used",
            "node": f"{node}"
        }
    ), Metric(
        metric_name="memory_usage",
        metric_type="gauge",
        comment="Memory Usage Data",
        value=memory[4],
        params={
            "type": "free",
            "node": f"{node}"
        }
    )]

    # raspberry pi exclusive
    if platform.system() == "Linux":
        from vcgencmd import Vcgencmd
        temp = Vcgencmd().measure_temp()
        metrics_list.append(
            Metric(
                metric_name="cpu_temperature",
                metric_type="gauge",
                comment="CPU Temperature",
                value=temp,
                params={
                    "node": f"{node}"
                }
            ))

    for partition in partitions:
        disk = psutil.disk_usage(partition[1])
        metrics_list.append(
            Metric(
                metric_name="disk_usage",
                metric_type="gauge",
                comment="Disk Usage Data",
                value=disk[0],
                params={
                    "mount": partition[1],
                    "type": "total",
                    "node": f"{node}"
                }
            ))
        metrics_list.append(
            Metric(
                metric_name="disk_usage",
                metric_type="gauge",
                comment="Disk Usage Data",
                value=disk[1],
                params={
                    "mount": partition[1],
                    "type": "used",
                    "node": f"{node}"
                }
            ))

        metrics_list.append(
            Metric(
                metric_name="disk_usage",
                metric_type="gauge",
                comment="Disk Usage Data",
                value=disk[2],
                params={
                    "mount": partition[1],
                    "type": "free",
                    "node": f"{node}"
                }
            ))

    return metrics_list


def generate_metrics(node: int):
    output = ""

    for metric in metrics(node):
        output += metric.to_string() + "\n" + "\n"

    return output
