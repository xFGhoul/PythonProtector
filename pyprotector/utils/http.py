import httpx

def get_ip_address() -> str:
    data = httpx.get("https://ipinfo.io/json").json()
    ip = data.get('ip')
    return ip

def hasInternet() -> bool:
    if httpx.get("https://google.com"):
        return True
    else:
        return False
        