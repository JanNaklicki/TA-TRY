#!/bin/bash

start_time=$(date +"%T")

python main.py

end_time=$(date +"%T")

echo "Server started at: $start_time"
echo "Server shutdown at: $end_time"
