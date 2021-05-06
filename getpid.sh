#!/bin/bash

ps -aux | grep "python3 ./Controller.py" | grep -v "grep"
