import platform
import time

import psutil

psutil.PROCFS_PATH = "/host-proc"

from app.metric import Metric


# get data and create list of Metrics
def metrics(node: int):
    # get CPU
    cpu = psutil.cpu_percent()
    # get number of cpu cores
    cores = psutil.cpu_count()
    # get number of physical cpu cores
    cores_physical = psutil.cpu_count(logical=False)
    # get memory data
    memory = psutil.virtual_memory()
    # get boot time of host system
    boot_time = psutil.boot_time()
    # get system time
    system_time = time.time()
    # get number of tcp connections
    tcp_connections = len(psutil.net_connections(kind="tcp"))
    # get disk partitions
    partitions = psutil.disk_partitions()

    # create list of Metrics
    metrics_list = [
        Metric(
            metric_name="cpu_usage",
            metric_type="gauge",
            comment="CPU Usage in Percent",
            value=cpu,
            params={"node": f"{node}"},
        ),
        Metric(
            metric_name="cpu_cores",
            metric_type="gauge",
            comment="Total CPU Cores",
            value=cores,
            params={"type": "all", "node": f"{node}"},
        ),
        Metric(
            metric_name="cpu_cores",
            metric_type="gauge",
            comment="Total CPU Cores",
            value=cores_physical,
            params={"type": "physical", "node": f"{node}"},
        ),
        Metric(
            metric_name="boot_time",
            metric_type="gauge",
            comment="Time in sec since epoch",
            value=boot_time,
            params={"node": f"{node}"},
        ),
        Metric(
            metric_name="system_time",
            metric_type="gauge",
            comment="Time in sec since epoch",
            value=system_time,
            params={"node": f"{node}"},
        ),
        Metric(
            metric_name="tcp_connections",
            metric_type="gauge",
            comment="Number of TCP connections",
            value=tcp_connections,
            params={"node": f"{node}"},
        ),
        Metric(
            metric_name="memory_usage",
            metric_type="gauge",
            comment="Memory Usage Data",
            value=memory[0],
            params={"type": "total", "node": f"{node}"},
        ),
        Metric(
            metric_name="memory_usage",
            metric_type="gauge",
            comment="Memory Usage Data",
            value=memory[1],
            params={"type": "available", "node": f"{node}"},
        ),
        Metric(
            metric_name="memory_usage",
            metric_type="gauge",
            comment="Memory Usage Data",
            value=memory[3],
            params={"type": "used", "node": f"{node}"},
        ),
        Metric(
            metric_name="memory_usage",
            metric_type="gauge",
            comment="Memory Usage Data",
            value=memory[4],
            params={"type": "free", "node": f"{node}"},
        ),
    ]

    # raspberry pi exclusive
    #if platform.system() == "Linux":
        #from vcgencmd import Vcgencmd

        # get cpu temperature
        #temp = Vcgencmd().measure_temp()
        # add to metrics list
        #metrics_list.append(
            #Metric(
                #metric_name="cpu_temperature",
                #metric_type="gauge",
                #comment="CPU Temperature",
                #value=temp,
                #params={"node": f"{node}"},
            #)
        #)
    
    
    # iterate over partitions and add important data to Metrics list
    for partition in partitions:
        disk = psutil.disk_usage(partition[1])
        metrics_list.append(
            Metric(
                metric_name="disk_usage",
                metric_type="gauge",
                comment="Disk Usage Data",
                value=disk[0],
                params={"mount": partition[1], "type": "total", "node": f"{node}"},
            )
        )
        metrics_list.append(
            Metric(
                metric_name="disk_usage",
                metric_type="gauge",
                comment="Disk Usage Data",
                value=disk[1],
                params={"mount": partition[1], "type": "used", "node": f"{node}"},
            )
        )

        metrics_list.append(
            Metric(
                metric_name="disk_usage",
                metric_type="gauge",
                comment="Disk Usage Data",
                value=disk[2],
                params={"mount": partition[1], "type": "free", "node": f"{node}"},
            )
        )

    # return list of Metrics
    return metrics_list


# generates formatted string of metrics
def generate_metrics(node: int):
    output = ""

    # get list of Metrics and concatenates them to a single string
    for metric in metrics(node):
        output += metric.to_string() + "\n" + "\n"

    return output
