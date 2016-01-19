#!/bin/bash
flake8 cron_descriptor tests examples --max-line-length=120 --builtins=_
