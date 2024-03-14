import socket
import os
import psutil

import requests

def get_groundlight_service_info() -> dict:
    """Gathers info about connectivity to groundlight.  This includes:
    - Endpoint being used  (from env var GROUNDLIGHT_ENDPOINT)
    - is an API Token configured?  (from env var GROUNDLIGHT_API_TOKEN)
    - Is the endpoint's URL reachable.
    """
    #TODO: We should re-think this; it's okay as a demo, but not actually very good.
    # Instead, we should try to connect with the SDK.  If that works, we just display
    # the endpoint & username from the SDK.
    # If that doesn't work, then we start displaying other things, like the endpoint
    # and some network diagnostics.  Figure out the endpoint host (get this from the SDK)
    # do DNS on it.  Try a simple TCP connection to the port number and report what happens.
    out = {}

    # Get the endpoint being used
    endpoint = os.getenv("GROUNDLIGHT_ENDPOINT", "api.groundlight.ai")
    out["Groundlight Endpoint"] = endpoint

    # Is an API Token configured?
    api_token = os.getenv("GROUNDLIGHT_API_TOKEN")
    out["API Token Configured"] = "Yes" if api_token else "No"

    # Stupid check of if we can reach the endpoint.
    try:
        response = requests.get(f"https://{endpoint}/v1/ping")
        response.raise_for_status()
        out["Endpoint Reachable"] = "Yes"
    except Exception as e:
        out["Endpoint Reachable"] = "No"
        out["Endpoint Reachable Error"] = str(e)

    return out


def get_system_info() -> dict:
    """Returns a dictionary containing system information"""
    out = {}

    # Get local IP address
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    out["Local IP Address"] = local_ip
    out["Hostname / Container ID"] = hostname
    
    # Get uptime
    try:
        with open("/proc/uptime", "r") as f:
            uptime_seconds = float(f.readline().split()[0])
            days, remainder = divmod(uptime_seconds, 86400)
            hours, remainder = divmod(remainder, 3600)
            minutes, seconds = divmod(remainder, 60)
            uptime = f"{int(days)}d {int(hours)}h {int(minutes)}m {int(seconds)}s"
    except Exception as e:
        uptime = "Unavailable"
    out["Uptime"] = uptime
    
    # Get load average
    try:
        load1, load5, load15 = os.getloadavg()
        out["CPU Load Average (1 min)"] = f"{load1:.3f}"
        out["CPU Load Average (5 min)"] = f"{load5:.3f}"
        out["CPU Load Average (15 min)"] = f"{load15:.3f}"
    except Exception as e:
        out["CPU Load Average"] = "Unavailable"

    out["CPU Cores"] = os.cpu_count()
    try:
        out["Total RAM"] = f"{psutil.virtual_memory().total / 1024 / 1024:.0f} MB"
    except Exception as e:
        out["Total RAM"] = "Unavailable"
    
    try:
        out["Free Disk Space"] = f"{psutil.disk_usage('/').free / 1024 / 1024 :.0f} MB"
    except Exception as e:
        out["Free Disk Space"] = "Unavailable"

    # CPU architecture
    out["CPU Architecture"] = os.uname().machine

    return out


def get_all_diagnostics() -> dict:
    """Returns a dictionary containing all diagnostics"""
    out = {}

    # merge all the diagnostics
    out.update(get_groundlight_service_info())
    out.update(get_system_info())
    return out

