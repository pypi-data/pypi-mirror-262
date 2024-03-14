# Transutil

Transutil is a versatile utility tool designed to enhance productivity and streamline workflow processes. With a focus on simplicity, security, and efficiency, Transutil offers a range of features to support various tasks and projects.

## Features

- **Chiper**: A built-in encryption tool providing a secure alternative to JWT for protecting sensitive data.
- **Syncbit**: Lightweight and dependency-free, Syncbit offers seamless data synchronization, serving as a substitute for pydantic.

### HTTP Client

Transutil provides a reliable HTTP client module as an alternative to Python's requests library. With Transutil's HTTP client, you can easily make HTTP requests and handle responses efficiently.

### Validators

Transutil includes a comprehensive validators module for data validation. Whether you need to validate user input, API responses, or any other data, Transutil's validators offer a robust solution for ensuring data integrity.

### Dispatcher

Efficiently handle real-time signals and events with Transutil's dispatcher module. With support for event-driven architecture, the dispatcher allows you to manage and respond to signals effectively.

### Mailer

Simplify email communication with Transutil's mailer module. Whether you need to send notifications, alerts, or other types of messages, Transutil's mailer provides a reliable solution for sending emails.

### Module Loader

Streamline module loading and management with Transutil's module loader. Dynamically load modules, handle dependencies, and simplify your application's architecture with ease.

### Crypter

Secure your data with Transutil's crypter module. With support for encryption algorithms, the crypter module allows you to encrypt and decrypt sensitive information securely.


## Installation

You can install Transutil via pip:

```bash
pip install transutil
```

## EXAMPLES

```python
from transutil import syncbit

class UserAuthRegisterSchema(syncbit.Schema):

    name: str = syncbit.fields.String(strict = True)
    email: str = syncbit.fields.String(strict = True)
    mobile: int = syncbit.fields.Integer(strict = True)
    password: str = syncbit.fields.String(strict = True)

    def __str__(self) -> str:
        return self.name
    
    def __repr__(self) -> str:
        return "UserAuthRegisterSchema %s" % (self.name)
    
class UserAuthLoginSchema(syncbit.Schema):

    email: str = syncbit.fields.String(strict = True)
    password: str = syncbit.fields.String(strict = True)

    def __str__(self) -> str:
        return self.email
    
    def __repr__(self) -> str:
        return "UserAuthLoginSchema %s" % (self.email)

```
