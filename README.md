# screen-reader-emulator

A browser extension to operate screen readers with your mouse instead of hotkeys

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

- Might need more explicit calling out if pre-commit hooks/CI for black/flake8 aren't setup yet

  - Same might go for Prettier/ESLint

- Also had to make a similar increase as [here](https://github.com/Microsoft/vscode-python/issues/4842#issuecomment-478759707) after also installing flake8 and having it run-on-save

- flake8 and black have slightly different default line lengths, so I increased vs code's limits per [this](https://github.com/psf/black/blob/ac10ca8e60594a6bdf57ff3b078eccb3192d7878/README.md#user-content-line-length)
