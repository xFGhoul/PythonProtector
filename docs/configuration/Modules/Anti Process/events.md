### Anti Process

```py
process_running(process: psutil.Process)
```

Called When Blacklisted Process Found Running

##### Parameters

- `process` ([`psutil.Process`](https://psutil.readthedocs.io/en/latest/#psutil.Process)) - Process Found Running

```py
window_name_detected(window_name: str)
```

Called When Blacklisted Window Name Found

##### Parameters

- `window_name` ([`str`](https://docs.python.org/3/library/stdtypes.html#str)) - Window Name