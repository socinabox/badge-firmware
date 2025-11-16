# badge-firmware

Firmware for the badge project.

## Repository Information

- **Repository URL (SSH):** `git@github.com:socinabox/badge-firmware.git`

- **Repository URL (HTTPS):** `https://github.com/socinabox/badge-firmware.git`

- **Branch:** `main`

## Git Workflow

### Initial Setup

This repository is already initialized and connected to GitHub. The remote is configured to use SSH authentication.

### Pushing Changes

To push changes to GitHub:

```bash
# Stage your changes
git add .

# Commit your changes
git commit -m "Description of changes"

# Push to GitHub
git push origin main
```

### Authentication

This repository uses **SSH authentication**. The SSH key is located at `~/.ssh/id_rsa.pub` and has been added to the GitHub account.

If you encounter authentication issues:

1. Verify SSH key is added to GitHub: https://github.com/settings/keys

2. Test SSH connection:
   ```bash
   ssh -T git@github.com
   ```

3. If needed, check remote URL:
   ```bash
   git remote -v
   ```

### Common Commands

```bash
# Check status
git status

# View changes
git diff

# Pull latest changes
git pull origin main

# Create a new branch
git checkout -b feature-name

# Switch branches
git checkout main
```

## Author

David Broggy
