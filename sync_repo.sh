#!/usr/bin/env bash
set -euo pipefail

# Helper to ask yes/no questions.
ask_yes_no() {
    local prompt="$1"
    local default="${2:-n}"
    local answer
    read -r -p "$prompt [y/N]: " answer || true
    answer="${answer:-$default}"
    case "$answer" in
        y|Y|yes|YES) return 0 ;;
        *) return 1 ;;
    esac
}

# Ensure we are inside a git repo.
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "Not inside a git repository. Abort."
    exit 1
fi

# Optionally remove global URL rewrites that force HTTPS over SSH.
if ask_yes_no "Remove global https->ssh rewrite rules if present?"; then
    git config --global --unset-all url.https://github.com/.insteadof 2>/dev/null || true
    git config --global --unset-all url.https://.insteadof 2>/dev/null || true
fi

# Handle remote URL.
remote_name="origin"
new_remote_url="${1:-}"
if [[ -n "$new_remote_url" ]]; then
    if git remote get-url "$remote_name" >/dev/null 2>&1; then
        git remote set-url "$remote_name" "$new_remote_url"
    else
        git remote add "$remote_name" "$new_remote_url"
    fi
else
    if ! git remote get-url "$remote_name" >/dev/null 2>&1; then
        read -r -p "No remote set. Enter SSH URL (e.g., git@github.com:user/repo.git): " input_url || true
        if [[ -n "$input_url" ]]; then
            git remote add "$remote_name" "$input_url"
        else
            echo "No remote provided. Abort."
            exit 1
        fi
    fi
fi

echo "Current remote ($remote_name):"
git remote get-url "$remote_name"
echo

# Show status.
git status -sb
echo

# Stage changes.
if ask_yes_no "Stage all changes (git add -A)?"; then
    git add -A
else
    echo "Skipping staging."
fi

# Commit with user-provided message.
read -r -p "Commit message (leave empty to skip commit): " commit_msg || true
if [[ -n "${commit_msg:-}" ]]; then
    git commit -m "$commit_msg"
else
    echo "Skipping commit."
fi

# Push to remote.
if ask_yes_no "Push to $remote_name now?"; then
    git push -u "$remote_name" HEAD
else
    echo "Skipping push."
fi
