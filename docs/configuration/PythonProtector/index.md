# Python Protector

```py
class PythonProtector:
    def __init__(
        self,
        debug: Optional[bool],
        modules: Set[str],
        logs_path: Optional[Union[Path, str]],
        webhook_url: Optional[str],
        on_detect: Optional[Set[str]],
    ) -> None:
```

## Arguments

- `debug` (`bool`) - Whether Or Not PythonProtector Should Log Actions.
- `modules` (`Set[str]`) - List Of Modules You Would Like To Enable.
- `logs_path` (`Union[Path, str]`) - Path For PythonProtector Logs.
- `webhook_url` (`str`) - Webhook URL For Reporting Remotely.
- `on_detect` (`Set[str], optional`) - List of Things PyProtector Does When Detections Are Caused

## Raises
- `ModulesNotValid` - Raises If Modules Are Not Valid
- `DetectionsNotValid` -  Raises If on_detect parameters are invalid
- `LogsPathEmpty` - Raises If Debug Is Enabled But No Logs Path Are Provided

## Methods

#### `start`

Main Function Of PythonProtector, Initializes Everything.

##### Raises
 - `DeprecationWarning` - If Python Version < 3.11


## Properties

#### `version`

Returns The Current PythonProtector Version

##### Type

[`str`](https://docs.python.org/3/library/stdtypes.html#str)

#### `user`

Returns a Tuple of User Information

##### Type

[`tuple`](https://docs.python.org/3/library/functions.html#func-tuple)

#### `ip`

Returns The Current Users IP

##### Type

[`str`](https://docs.python.org/3/library/stdtypes.html#str)

#### `computer`

Returns The Current Users WMI Computer Object

##### Type

[`typing.Any`](https://docs.python.org/3/library/typing.html#the-any-type)

## Extra Notes

#### List of Valid Modules:

```py
Modules: Final[Set[str]] = {
    "Miscellaneous",
    "AntiProcess",
    "AntiDLL",
    "AntiVM",
    "AntiAnalysis",
    }
```

#### List of Valid Detections:

```py
Detections: Final[Set[str]] = {"Screenshot", "Exit", "Report"}
```