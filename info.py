import platform
import socket
import cpuinfo
import psutil
import datetime
import re
import uuid

# Function to format bytes to a proper format
def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

# Function to format and retrieve system information
def system_information(spaces=12):
    content = "```"
    content += "\nSystem Information:\n\n"
    uname = platform.uname()
    content += "{0:<{spaces}} {1:>20}\n".format("System:", uname.system, spaces=spaces)
    content += "{0:<{spaces}} {1:>20}\n".format("Node Name:", uname.node, spaces=spaces)
    content += "{0:<{spaces}} {1:>20}\n".format("Release:", uname.release, spaces=spaces)
    content += "{0:<{spaces}} {1:>20}\n".format("Version:", uname.version, spaces=spaces)
    content += "{0:<{spaces}} {1:>20}\n".format("Machine:", uname.machine, spaces=spaces)
    content += "{0:<{spaces}} {1:>20}\n".format("Processor:", uname.processor, spaces=spaces)
    content += "{0:<{spaces}} {1:>20}\n".format("Processor:", cpuinfo.get_cpu_info()['brand_raw'], spaces=spaces)
    content += "{0:<{spaces}} {1:>20}\n".format("IP Address:", socket.gethostbyname(socket.gethostname()), spaces=spaces)
    content += "{0:<{spaces}} {1:>20}\n".format("Mac Address:", ':'.join(re.findall('..', '%012x' % uuid.getnode())), spaces=spaces)

    # Boot Time
    content += "\nBoot Time:\n"
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.datetime.fromtimestamp(boot_time_timestamp)
    content += "{0:<{spaces}} {1:>20}\n".format("Boot Time:", f"{bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}", spaces=spaces)

    # CPU information
    content += "\nCPU Info:\n"
    content += "{0:<{spaces}} {1:>20}\n".format("Physical cores:", psutil.cpu_count(logical=False), spaces=spaces)
    content += "{0:<{spaces}} {1:>20}\n".format("Total cores:", psutil.cpu_count(logical=True), spaces=spaces)
    cpufreq = psutil.cpu_freq()
    content += "{0:<{spaces}} {1:>20.2f}Mhz\n".format("Max Frequency:", cpufreq.max, spaces=spaces)
    content += "{0:<{spaces}} {1:>20.2f}Mhz\n".format("Min Frequency:", cpufreq.min, spaces=spaces)
    content += "{0:<{spaces}} {1:>20.2f}Mhz\n".format("Current Frequency:", cpufreq.current, spaces=spaces)
    content += "\nCPU Usage Per Core:\n"
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        content += "{0:<{spaces}} {1:>20}\n".format(f"Core {i+1}:", f"{percentage}%", spaces=spaces)

    # Memory Information
    content += "\nMemory Usage:\n"
    svmem = psutil.virtual_memory()
    content += "{0:<{spaces}} {1:>20}\n".format("Total:", get_size(svmem.total), spaces=spaces)
    content += "{0:<{spaces}} {1:>20}\n".format("Available:", get_size(svmem.available), spaces=spaces)
    content += "{0:<{spaces}} {1:>20}\n".format("Used:", get_size(svmem.used), spaces=spaces)
    content += "{0:<{spaces}} {1:>20}\n".format("Percentage:", f"{svmem.percent}%", spaces=spaces)

    # Disk Information
    content += "\nDisk Usage:\n"
    partitions = psutil.disk_partitions()
    for partition in partitions:
        content += "{0:<{spaces}} {1:>20}\n".format("Device:", partition.device, spaces=spaces)
        content += "{0:<{spaces}} {1:>20}\n".format("Mountpoint:", partition.mountpoint, spaces=spaces)
        content += "{0:<{spaces}} {1:>20}\n".format("File system type:", partition.fstype, spaces=spaces)
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            continue
        content += "{0:<{spaces}} {1:>20}\n".format("Total:", get_size(partition_usage.total), spaces=spaces)
        content += "{0:<{spaces}} {1:>20}\n".format("Used:", get_size(partition_usage.used), spaces=spaces)
        content += "{0:<{spaces}} {1:>20}\n".format("Free:", get_size(partition_usage.free), spaces=spaces)
        content += "{0:<{spaces}} {1:>20}\n".format("Percentage:", f"{partition_usage.percent}%", spaces=spaces)
        content += "\n"

    content += "```"
    return content

if __name__ == "__main__":
    print(system_information(12))
