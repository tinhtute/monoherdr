"""Publish each agent pane's logo glyph (Herdr Agent Icons Max font) as $logo."""
import json
import os
import shutil
import subprocess
import sys

# Codepoints from hhdebb/herdr-radar lib/logos.js (MIT).
LOGOS = {
    "claude": 0xE1A0, "codex": 0xE1A1, "opencode": 0xE1A2, "omp": 0xE1A3,
    "cline": 0xE1A4, "mastracode": 0xE1A5, "kimi": 0xE1A6, "kilo": 0xE1A7,
    "maki": 0xE1A8, "pi": 0xE1A9, "hermes": 0xE1AA, "cursor": 0xE1AB,
    "copilot": 0xE1AC, "deepseek": 0xE1AD, "gemini": 0xE1AE, "gpt": 0xE1AF,
    "qwen": 0xE1B0, "grok": 0xE1B1, "antigravity-cli": 0xE1B2, "agy": 0xE1B2,
    "kiro": 0xE1B3, "amp": 0xE1B4, "devin": 0xE1B5, "qodercli": 0xE1B6,
    "glm": 0xE1B7, "kimchi": 0xE1B8, "muse": 0xE1B9, "crush": 0xE1BA,
}
SOURCE = "monoherdr:icons"
# quaqua grid_role → the pane-name token it fills; config.toml colours each by role.
ROLE_TOKENS = {"cos": "name_cos", "orchestrator": "name_lead", "worker": "name_worker"}
STALE = ["role_label", "cos_bar", "lead_bar", "worker_bar", "logo_cos", "logo_lead", "logo_worker"]


def herdr():
    # HERDR_BIN_PATH can outlive the binary after a reinstall, so only trust it if it still exists.
    env = os.environ.get("HERDR_BIN_PATH")
    if env and os.access(env, os.X_OK):
        return env
    return shutil.which("herdr") or "herdr"


def main():
    clear = "--clear" in sys.argv
    out = subprocess.run([herdr(), "agent", "list"], capture_output=True, text=True, check=True).stdout
    for a in json.loads(out)["result"]["agents"]:
        # A wrapper's --display-agent (e.g. glm) wins over the detected binary.
        name = (a.get("display_agent") or a.get("agent") or "").lower()
        cp = LOGOS.get(name) or LOGOS.get(a.get("agent", ""))
        args = [herdr(), "pane", "report-metadata", a["pane_id"], "--source", SOURCE]
        tokens = a.get("tokens") or {}
        if clear or cp is None:
            args += ["--clear-token", "logo"]
        else:
            args += ["--token", "logo=" + chr(cp)]
        role = None if clear else ROLE_TOKENS.get(tokens.get("grid_role", ""))
        for tok in ROLE_TOKENS.values():
            if tok == role:
                label = a.get("name") or ("CoS" if tok == "name_cos" else tokens.get("grid_owner")) or a["pane_id"]
                args += ["--token", f"{tok}={label}"]
            else:
                args += ["--clear-token", tok]
        for tok in STALE:
            args += ["--clear-token", tok]
        subprocess.run(args, capture_output=True)


if __name__ == "__main__":
    main()
