# Multi-Agents Smart OA System

This repository now contains a structured Flask application skeleton that matches the desired layout:

```
APP/
├── app.py
├── config.py
├── instance/
│   └── config.py
├── DataPanel/
│   ├── DataPanel.py
│   ├── __init__.py
│   ├── models/
│   ├── routes/
│   ├── static/
│   └── templates/
└── ChatPage/
    ├── ChatPage.py
    ├── __init__.py
    ├── models/
    ├── routes/
    ├── static/
    ├── templates/
    ├── UserController/
    │   ├── UserController.py
    │   ├── __init__.py
    │   ├── models/
    │   ├── routes/
    │   ├── static/
    │   └── templates/
    └── ConversationController/
        ├── ConversationController.py
        ├── __init__.py
        ├── models/
        ├── routes/
        ├── static/
        └── templates/
```

Each package exposes a Flask blueprint and registers routes through dedicated modules. Placeholder templates are provided so the application can run immediately while you continue development.
