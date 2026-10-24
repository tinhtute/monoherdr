#!/usr/bin/env bash
# Symlink config.toml into ~/.config/herdr, install the icon font, link the plugin.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
dst="$HOME/.config/herdr/config.toml"
mkdir -p "$(dirname "$dst")"
if [[ -e "$dst" && ! -L "$dst" ]]; then
  mv "$dst" "$dst.bak.$(date +%Y%m%d%H%M%S)"
fi
ln -sfn "$here/config.toml" "$dst"

if [[ "$(uname)" == Darwin ]]; then fontdir="$HOME/Library/Fonts"; else fontdir="$HOME/.local/share/fonts"; fi
mkdir -p "$fontdir"
cp "$here/fonts/HerdrAgentIconsMax-Regular.ttf" "$fontdir/"
command -v fc-cache >/dev/null && fc-cache -f "$fontdir" || true

herdr plugin link "$here/plugin" >/dev/null
herdr server reload-config >/dev/null
herdr plugin action invoke monoherdr.agent-icons.refresh >/dev/null
echo "linked $dst -> $here/config.toml"
echo "Ghostty needs: font-codepoint-map = U+E1A0-U+E1BA=Herdr Agent Icons Max"
