# Intro To Events

`Events` is a system implemented to notify when a specific function has raised a detection.

Example Event:

```py
@security.event.obs.on("process_running") 
def on_process_running(text: str, module: str, process: psutil.Process):
    print(f"{module} - {text}\nProcess Name: {process.name()}")
    # Free To Do Whatever You Want Here...
```

Events Will Always Return `text` and `module`, any other kwargs are event specific.

You Can Find All Events In Each Modules Respective `Event Reference`.


