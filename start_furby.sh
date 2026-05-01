#!/bin/bash

# Give the system 30 seconds to fully initialize Wi-Fi and hardware
sleep 30

# Create a new detached tmux session named 'furby'
tmux new-session -d -s furby

# Navigate to the project directory
tmux send-keys -t furby "cd /home/furby/furpberry" C-m

# Activate the virtual environment (change 'venv' to 'env' if your Makefile used that)
tmux send-keys -t furby "source venv/bin/activate" C-m

# Run the Furby code
tmux send-keys -t furby "furbalicious" C-m