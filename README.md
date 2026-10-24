# monoherdr

Tui's custom [Herdr](https://herdr.dev) config.

- `config.toml`: symlinked to `~/.config/herdr/config.toml`
- `plugin/`: the `monoherdr.agent-icons` plugin, which publishes each agent's logo as the `$logo` sidebar token
- `fonts/`: the `Herdr Agent Icons Max` font, taken from [hhdebb/herdr-radar](https://github.com/hhdebb/herdr-radar) (MIT, see `fonts/`)
- `./install.sh`: back up and symlink the config, install the font, link the plugin, reload

Ghostty needs this line so the glyphs render:

```
font-codepoint-map = U+E1A0-U+E1BA=Herdr Agent Icons Max
```

Refresh the icons by hand: `herdr plugin action invoke monoherdr.agent-icons.refresh`
