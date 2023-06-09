# Human-Readable Lightweight OpenAPI client Generator

## Introduction

The goal of this repository is to create an API client (SDK) from an OpenAPI json file.

The created client will be very lightweight with only aiohttp as external dependency. It will also
be human-readable so that the generated client can easily be modified and read by developers.

## The generated client

The generated client will be very simple, for example in Python:

- **ApiName.py** This file will contain a class that allow interactions with the API.
                 Users are able to interact with the API by creating an instance of this
                 class and calling the methods.
- **models/\*** This folder will contain all models for the API. They are usually the return
                types of the methods of ApiName.py
- **exceptions/\*** This folder will contain all of the exceptions that the SDK can throw.

It will use Async features and be documented using sphinx for Python. This way a Documentation
can easily be generated from the SDK created.

## TODO

- [x] Make the destination an already ready module
- [x] Change `TooManyRequestException` to `TooManyRequestsException` (add an `s`)
- [x] Change tests so that they import from the module
- [x] Change the main files so that they import the models and exceptions correctly
- [ ] Change files so that a newline is not added on top of them
- [ ] Remove asdict import in tests when it is not needed (for example the decimals call)
- [ ] Add example for method calls
