from . import (
    Text,
    Fps,
    Redirect,
    Input
)

elements = {
    "p": {
        "class": Text.Text,
        "focusable": False
    },
    "h1": {
        "class": Text.Text,
        "focusable": False
    },
    "h2": {
        "class": Text.Text,
        "focusable": False
    },
    "h3": {
        "class": Text.Text,
        "focusable": False
    },
    "h4": {
        "class": Text.Text,
        "focusable": False
    },
    "h5": {
        "class": Text.Text,
        "focusable": False
    },
    "h6": {
        "class": Text.Text,
        "focusable": False
    },
    "fps": {
        "class": Fps.Fps,
        "focusable": True,
    },
    "a": {
        "class": Redirect.Redirect,
        "focusable": True
    },
    "input": {
        "class": Input.Input,
        "focusable": True
    }
}