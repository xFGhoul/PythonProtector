# Intro To Events

`Events` is a system implemented to notify when a specific function has raised a detection.

There are two events that are called when the application detects suspicious activity, `pyprotector_detect` and the function's specific event found in the event reference.

Example `pyprotector_detect` Event:

```py
@security.event.obs.on("pyprotector_detect")
def on_pyprotector_detect(text: str, module: str, **kwargs):
    print(f"{module} - {text}\nKwargs: {kwargs}")
```

Example Function Specific Event:

```py
@security.event.obs.on("process_running") 
def on_process_running(text: str, module: str, process: psutil.Process):
    print(f"{module} - {text}\nProcess Name: {process.name()}")
    # Free To Do Whatever You Want Here...
```

Events Will Always Return `text` and `module`, any other kwargs are event specific.

You Can Find All Events In Each Modules Respective `Event Reference`.


