#!/usr/bin/env bash
# Symlink config.toml into ~/.config/herdr, backing up any existing file.
set -euo pipefail
src="$(cd "$(dirname "$0")" && pwd)/config.toml"
dst="$HOME/.config/herdr/config.toml"
mkdir -p "$(dirname "$dst")"
if [[ -e "$dst" && ! -L "$dst" ]]; then
  mv "$dst" "$dst.bak.$(date +%Y%m%d%H%M%S)"
fi
ln -sfn "$src" "$dst"
herdr config check 2>/dev/null || true
herdr server reload-config
echo "linked $dst -> $src"
