### Anti VM

```py
blacklisted_hwid(hwid: str)
```

Called When Blacklisted HWID Found Detected

##### Parameters

- `hwid` ([`str`](https://docs.python.org/3/library/stdtypes.html#str)) - Blacklisted HWID
  
```py
blacklisted_pc_username(pc_username: str)
```

Called When Blacklisted PC Username Found

##### Parameters

- `pc_username` ([`str`](https://docs.python.org/3/library/stdtypes.html#str)) - Blacklisted PC Username


```py
blacklisted_pc_name(pc_name: str)
```

Called When Blacklisted PC Name Found

##### Parameters

- `pc_name` ([`str`](https://docs.python.org/3/library/stdtypes.html#str)) - Blacklisted PC Name

```py
blacklisted_ip(ip: str)
```

Called When Blacklisted IP Found

##### Parameters

- `ip` ([`str`](https://docs.python.org/3/library/stdtypes.html#str)) - Blacklisted IP

```py
blacklisted_mac_address(mac_addr: str)
```

Called When Blacklisted Mac Address Found

##### Parameters

- `mac_addr` ([`str`](https://docs.python.org/3/library/stdtypes.html#str)) - Blacklisted Mac Address

##### Parameters

```py
blacklisted_gpu(gpu: str)
```

Called When Blacklisted GPU Found

##### Parameters

- `gpu` ([`str`](https://docs.python.org/3/library/stdtypes.html#str)) - Blacklisted GPU

```py
vmware_registry(reg1: int, reg2: int)
```

Called When VMWare Registry Found

##### Parameters

- `reg1` ([`int`](https://docs.python.org/3/library/stdtypes.html#typesnumeric)) - VMWare Registry Identifier 
- `reg2` ([`int`](https://docs.python.org/3/library/stdtypes.html#typesnumeric)) - VMWare Registry Identifier

```py
vmware_mac(mac_addr: str)
```

Called When VMWare MAC Address Found

##### Parameters

- `mac_addr` ([`str`](https://docs.python.org/3/library/stdtypes.html#str)) - VMWare MAC Address


```py
screen_size(x: int, y: int)
```

Called When `x <= 200 or y <= 200` 

##### Parameters

- `x` ([`int`](https://docs.python.org/3/library/stdtypes.html#typesnumeric)) - Screen Size X
- `y` ([`int`](https://docs.python.org/3/library/stdtypes.html#typesnumeric)) - Screen Size Y

```py
vm_process_running(processes: List[str])
```

Called When VM Processes Found Running

##### Parameters

- `processes` ([List](https://docs.python.org/3/tutorial/introduction.html#lists)[[`str`](https://docs.python.org/3/library/stdtypes.html#str)]) - List Of Processes

```py
vmware_dll(dll: str)
```

Called When VMWare DLL Found

##### Parameters

- `dll` ([`str`](https://docs.python.org/3/library/stdtypes.html#str)) - VMWare DLL

```py
virtualbox_dll(dll: str)
```

Called When VirtualBox DLL Found

##### Parameters

- `dll` ([`str`](https://docs.python.org/3/library/stdtypes.html#str)) - VirtualBox DLL


