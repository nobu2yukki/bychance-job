#!/bin/bash

# Exit on error
set -e

echo "Setting up rich terminal environment..."

# Install required packages
apt-get update
apt-get install -y zsh curl git wget

# Install Oh My Zsh
if [ ! -d "$HOME/.oh-my-zsh" ]; then
    echo "Installing Oh My Zsh..."
    sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
fi

# Install Starship prompt
if ! command -v starship &> /dev/null; then
    echo "Installing Starship..."
    curl -sS https://starship.rs/install.sh | sh -s -- -y
fi

# Configure Zsh
if [ -f "$HOME/.zshrc" ]; then
    # Add Starship initialization
    if ! grep -q "starship init zsh" "$HOME/.zshrc"; then
        echo 'eval "$(starship init zsh)"' >> "$HOME/.zshrc"
    fi
    
    # Set a nice theme for Oh My Zsh
    sed -i 's/ZSH_THEME="robbyrussell"/ZSH_THEME="agnoster"/' "$HOME/.zshrc"
fi

# Set Zsh as default shell
chsh -s $(which zsh)

echo "Rich terminal environment setup complete!"