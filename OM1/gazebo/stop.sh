#!/usr/bin/env bash
# ------------------------------------------------------------------
# Script: stop_gz_processes.sh
#
# Description:
#   This script terminates every process that has "gz" or "gazebo" 
#   in its command line. It uses pkill with the -f flag to search the
#   full command line and sends SIGKILL (-9) to force termination.
#
# Usage:
#   Make sure the script is executable:
#       chmod +x stop_gz_processes.sh
#   Then run it:
#       ./stop_gz_processes.sh
#
# ------------------------------------------------------------------

echo "Stopping every process with 'gz' or 'gazebo' in its command line..."

# Use pkill with a regex pattern to match both 'gz' and 'gazebo'
# The -f flag tells pkill to match against the full command line.
# The -9 flag sends SIGKILL to force termination.
pkill -9 -f "gz|gazebo"

# Check the exit status of pkill
if [ $? -eq 0 ]; then
    echo "Processes terminated (if any were running)."
else
    echo "No matching processes found or an error occurred."
fi


# Stop existing containers if any
safe_docker_stop_and_remove() {
  local container_name=$1

  # Check if the container exists and is running, then stop it
  if docker ps -q -f name="$container_name" &>/dev/null; then
    echo "Stopping container: $container_name"
    docker stop "$container_name" &>/dev/null
  fi

  # Check if the container exists (stopped or running), then remove it
  if docker container ls -a -q -f name="$container_name" &>/dev/null; then
    echo "Removing container: $container_name"
    docker container rm "$container_name" &>/dev/null
  fi
}

# Stop and remove specific containers
safe_docker_stop_and_remove ros1_gazebo_container
safe_docker_stop_and_remove ros1_ros2_bridge