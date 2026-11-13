#!/bin/zsh
# Copy the Apify token first (Console > Settings > API & Integrations > copy), then run this.
t=$(pbpaste | tr -d '[:space:]')
[[ $t == apify_api_* ]] || { echo "Clipboard is not an Apify token (should start apify_api_)"; exit 1; }
security add-generic-password -U -a "$USER" -s apify-token -w "$t" && echo "Saved to Keychain: apify-token"
cd ~/Developer/linkedin-autopilot && python3 scripts/apify_posts.py search >/dev/null && echo "Test OK"
