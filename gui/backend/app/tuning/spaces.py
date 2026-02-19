from typing import Any


def suggest_param(trial, name: str, space: dict[str, Any]):
    ptype = space.get("type", "float")
    low = space.get("low", 0.0)
    high = space.get("high", 1.0)

    if ptype == "float":
        log = space.get("log", False)
        step = space.get("step")
        return trial.suggest_float(name, low, high, log=log, step=step)
    elif ptype == "int":
        return trial.suggest_int(name, int(low), int(high))
    elif ptype == "categorical":
        choices = space.get("choices", [])
        return trial.suggest_categorical(name, choices)
    else:
        return trial.suggest_float(name, low, high)
