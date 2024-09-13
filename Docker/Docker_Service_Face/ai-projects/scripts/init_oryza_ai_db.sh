#!/bin/bash

# Prompt for environment selection
echo "Select environment:"
echo "1. Production"
echo "2. Development"
read -p "Enter choice [1 or 2]: " env_choice

# Determine the docker-compose file based on user choice
case "$env_choice" in
    1)
        compose_file="docker-compose.oryza-ai.prod.yml"
        ;;
    2)
        compose_file="docker-compose.oryza-ai.dev.yml"
        ;;
    *)
        echo "Invalid choice. Please select 1 for Production or 2 for Development."
        exit 1
        ;;
esac

# Prompt for username
read -p "Enter username (default: admin): " username

# Use default value if empty
username=${username:-admin}

# Prompt for password securely
read -sp "Enter password (default: 1): " password
echo

# Use default value if empty
password=${password:-1}

# Check if the username and password are not empty
if [ -z "$username" ] || [ -z "$password" ]; then
    echo "Error: Username and password cannot be empty."
    exit 1
fi

# Execute the docker compose command with the selected compose file and provided credentials
docker compose -f "$compose_file" exec oryza_ai python -m app.db.init_db --email admin@oryza.vn --username "$username" --password "$password"
