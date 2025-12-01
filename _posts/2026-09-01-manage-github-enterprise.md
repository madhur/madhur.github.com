---
layout: blog-post
title: "Manage both github and github enterprise"
excerpt: "Manage both github and github enterprise"
disqus_id: /2026/09/01/manage-github-enterprise/
tags:
    - Github
---

> **Disclaimer**: This blog article has been generated with the assistance of AI. While the content is AI-generated, the software itself and the ideas behind it are the result of real development work and genuine user needs.

# Managing Multiple GitHub SSH Configurations for Personal and Enterprise Accounts

When working with both personal GitHub repositories and enterprise GitHub accounts, you'll often need different SSH keys and configurations. This guide walks through setting up SSH configurations to seamlessly work with multiple GitHub environments and automating repository cloning.

## The Challenge

Many developers face this scenario:
- Personal projects on regular GitHub.com using one SSH key
- Work projects on an enterprise GitHub organization requiring a different SSH key
- Need to clone repositories from both environments without manually switching configurations

## Solution: SSH Config with Host Aliases

The elegant solution is to use SSH host aliases in your `~/.ssh/config` file. This allows you to use different SSH keys and configurations for different "hosts" that actually point to the same GitHub servers.

### Step 1: Generate Separate SSH Keys

First, create separate SSH key pairs for each environment:

```bash
# Generate key for personal GitHub
ssh-keygen -t ed25519 -C "your-personal@email.com" -f ~/.ssh/id_ed25519_personal

# Generate key for enterprise GitHub
ssh-keygen -t ed25519 -C "your-work@company.com" -f ~/.ssh/id_ed25519_enterprise
```

### Step 2: Add Keys to SSH Agent

```bash
# Add both keys to your SSH agent
ssh-add ~/.ssh/id_ed25519_personal
ssh-add ~/.ssh/id_ed25519_enterprise
```

### Step 3: Configure SSH Config File

Create or edit `~/.ssh/config`:

```ssh-config
# Personal GitHub account
Host github.com
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_personal
    IdentitiesOnly yes

# Enterprise GitHub account
Host github-enterprise
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_enterprise
    IdentitiesOnly yes
```

### Step 4: Add Public Keys to GitHub

- Add `~/.ssh/id_ed25519_personal.pub` to your personal GitHub account
- Add `~/.ssh/id_ed25519_enterprise.pub` to your enterprise GitHub account

### Step 5: Test Your Configuration

```bash
# Test personal GitHub connection
ssh -T git@github.com

# Test enterprise GitHub connection  
ssh -T git@github-enterprise
```

Both should return successful authentication messages.

## Using the Configuration

With this setup, you can clone repositories using different SSH hosts:

```bash
# Clone personal repository (standard way)
git clone git@github.com:username/personal-repo.git

# Clone enterprise repository (using alias)
git clone git@github-enterprise:enterprise-org/work-repo.git
```

## Automating Repository Cloning

When building automation scripts (like cloning all starred repositories), you'll need to handle the SSH host transformation. Here's how:

### The Problem

GitHub's API always returns SSH URLs in the standard format:
```
git@github.com:enterprise-org/repository.git
```

But you need to transform these to use your custom SSH host:
```
git@github-enterprise:enterprise-org/repository.git
```

### The Solution

Here's a bash script snippet that handles this transformation:

```bash
#!/bin/bash

# SSH Configuration for Organizations
declare -A SSH_HOST_MAP=(
    ["enterprise-org"]="github-enterprise"
    ["another-org"]="github-another"
)

# Function to transform SSH URL based on organization
transform_ssh_url() {
    local ssh_url=$1
    
    # Extract organization from SSH URL
    if [[ $ssh_url =~ git@github\.com:([^/]+)/.* ]]; then
        local org_name="${BASH_REMATCH[1]}"
        
        # Check if we have a custom SSH host for this organization
        if [[ -n "${SSH_HOST_MAP[$org_name]}" ]]; then
            local custom_host="${SSH_HOST_MAP[$org_name]}"
            ssh_url=$(echo "$ssh_url" | sed "s|git@github\.com:|git@${custom_host}:|")
        fi
    fi
    
    echo "$ssh_url"
}

# Example usage
original_url="git@github.com:enterprise-org/some-repo.git"
transformed_url=$(transform_ssh_url "$original_url")
echo "Original: $original_url"
echo "Transformed: $transformed_url"
```

## Complete Automation Script

Here's a complete script that fetches all your starred repositories and clones them using the appropriate SSH configuration:

```bash
#!/bin/bash

# Configuration
GITHUB_TOKEN="your_personal_access_token"
USERNAME="your_username"
CLONE_DIR="./starred_repos"

# SSH host mapping for organizations
declare -A SSH_HOST_MAP=(
    ["enterprise-org"]="github-enterprise"
)

transform_ssh_url() {
    local ssh_url=$1
    if [[ $ssh_url =~ git@github\.com:([^/]+)/.* ]]; then
        local org_name="${BASH_REMATCH[1]}"
        if [[ -n "${SSH_HOST_MAP[$org_name]}" ]]; then
            local custom_host="${SSH_HOST_MAP[$org_name]}"
            ssh_url=$(echo "$ssh_url" | sed "s|git@github\.com:|git@${custom_host}:|")
        fi
    fi
    echo "$ssh_url"
}

# Fetch starred repositories
get_starred_repos() {
    local page=1
    while true; do
        response=$(curl -s -H "Authorization: token ${GITHUB_TOKEN}" \
            "https://api.github.com/users/${USERNAME}/starred?page=${page}&per_page=100")
        
        repos=$(echo "$response" | jq -r '.[].ssh_url' | grep -v '^null$')
        [[ -z "$repos" ]] && break
        
        echo "$repos"
        ((page++))
    done
}

# Clone repositories with SSH host transformation
mkdir -p "$CLONE_DIR"
get_starred_repos | while read -r ssh_url; do
    [[ -z "$ssh_url" ]] && continue
    
    transformed_url=$(transform_ssh_url "$ssh_url")
    repo_name=$(basename "$transformed_url" .git)
    
    if [[ -d "$CLONE_DIR/$repo_name" ]]; then
        echo "Skipping $repo_name (already exists)"
        continue
    fi
    
    echo "Cloning $repo_name..."
    if git clone "$transformed_url" "$CLONE_DIR/$repo_name"; then
        echo "✓ Successfully cloned $repo_name"
    else
        echo "✗ Failed to clone $repo_name"
    fi
done
```

## Conclusion

Using SSH host aliases provides a clean, maintainable way to work with multiple GitHub environments. Combined with automation scripts that handle URL transformation, you can seamlessly clone and manage repositories across personal and enterprise accounts without manual configuration changes.

This approach scales well as you add more organizations or GitHub instances, and the configuration remains clear and easy to understand for other team members who might need to work with your scripts.

---

*Have questions about SSH configuration or GitHub automation? Feel free to reach out in the comments below.*