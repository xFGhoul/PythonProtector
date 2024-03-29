### Miscellaneous

```py
is_debugger_present()
```

Called When IsDebuggerPresent Returns True

```py
check_remote_debugger_present()
```

Called When CheckRemoteDebuggerPresent Returns True

```py
output_debug_string()
```

Called When `OutputDebugString` != 0

```py
ram_check(ram: int)
```

Called When RAM Check Failed

```py
cpu_count()
```

Called When CPU Core Count Is Less Than OR Equal To `1`

##### Parameters

- `memory` ([`int`](https://docs.python.org/3/library/stdtypes.html#typesnumeric)) - Current RAM 
  
```py
disk_size_check(disk_size: int)
```

Called When Disk Size Check Failed

##### Parameters

- `disk_size` ([`int`](https://docs.python.org/3/library/stdtypes.html#typesnumeric)) - Current Disk Size


```py
blacklisted_path(path: str)
```

Called When Blacklisted Path Found

- `path` ([`str`](https://docs.python.org/3/library/stdtypes.html#str)) - Blacklisted Path

```py
blacklisted_import(package: str, dist: Distribution)
```

Called When Blacklisted Import Found

##### Parameters

- `package` ([`str`](https://docs.python.org/3/library/stdtypes.html#str)) - Name Of Package
- `dist` ([`Distribution`](https://setuptools.pypa.io/en/latest/pkg_resources.html#distribution-objects)) - Distribution Object

```py
ip_check(ip: str)
```

Called When Blacklisted IP Found

##### Parameters

- `ip` ([`str`](https://docs.python.org/3/library/stdtypes.html#str)) - Blacklisted IP

```py
proxy_headers(header: str)
```

Called When Proxy Headers Found

##### Parameters

- `header` ([`str`](https://docs.python.org/3/library/stdtypes.html#str)) - Proxy Header

```py
proxy_ip(ip: str)
```

Called When Proxy IP Found

##### Parameters

- `ip` ([`str`](https://docs.python.org/3/library/stdtypes.html#str)) - Proxy IP

```py
tor_network()
```

Called When A Tor Network Is Found In Use

```py
transparent_proxies()
```

Called When Transparent Proxies Detected
