"""
Pick the wiki-build / memory-sync model from config/model-selection.json.

For each role, walks the ranked candidate list and picks the first model that actually
answers a 1-token probe on the provider configured in .env (OPENWIKI_PROVIDER:
"anthropic" or "gemini-enterprise"/Vertex). Prints `export` lines; with --apply it
rewrites the matching lines in .env.

Staleness: when selected_at is older than review_after_days, the ranking may no longer
reflect the best price/quality models. The script then refuses to run (exit 3) unless
--allow-stale is passed, and prints instructions to re-research the model landscape
first (web search pricing/benchmarks, update candidates + selected_at).

Usage (from the project root):
    .venv/bin/python tools/select_model.py            # show selection
    .venv/bin/python tools/select_model.py --apply    # also update .env
    .venv/bin/python tools/select_model.py --allow-stale
"""
import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "model-selection.json"
ENV_FILE = ROOT / ".env"


def read_env():
    env = {}
    for line in ENV_FILE.read_text().splitlines():
        m = re.match(r"^([A-Z_]+)=(.*)$", line.strip())
        if m:
            env[m.group(1)] = m.group(2).strip('"')
    return env


def probe_anthropic(model_id, api_key):
    import requests
    r = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={"x-api-key": api_key, "anthropic-version": "2023-06-01"},
        json={"model": model_id, "max_tokens": 1, "messages": [{"role": "user", "content": "."}]},
        timeout=30,
    )
    return r.status_code == 200, f"{r.status_code} {r.json().get('error', {}).get('type', 'ok')}"


def probe_vertex(model_id, project, location, credentials_file):
    import google.auth.transport.requests
    import google.oauth2.service_account
    import requests
    creds = google.oauth2.service_account.Credentials.from_service_account_file(
        credentials_file, scopes=["https://www.googleapis.com/auth/cloud-platform"])
    creds.refresh(google.auth.transport.requests.Request())
    host = "aiplatform.googleapis.com" if location == "global" else f"{location}-aiplatform.googleapis.com"
    url = (f"https://{host}/v1/projects/{project}/locations/{location}"
           f"/publishers/anthropic/models/{model_id}:rawPredict")
    r = requests.post(url, headers={"Authorization": f"Bearer {creds.token}"},
                      json={"anthropic_version": "vertex-2023-10-16", "max_tokens": 1,
                            "messages": [{"role": "user", "content": "."}]}, timeout=30)
    # 429 means the model exists but is briefly rate-limited; treat as available.
    return r.status_code in (200, 429), str(r.status_code)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="rewrite the model lines in .env")
    ap.add_argument("--allow-stale", action="store_true", help="proceed even if the selection is stale")
    args = ap.parse_args()

    cfg = json.loads(CONFIG.read_text())
    env = read_env()
    provider = env.get("OPENWIKI_PROVIDER", "anthropic")

    selected_at = dt.date.fromisoformat(cfg["selected_at"])
    age_days = (dt.date.today() - selected_at).days
    if age_days > cfg.get("review_after_days", 120):
        print(f"!! model-selection.json is STALE: selected_at={selected_at} ({age_days} days old, "
              f"limit {cfg.get('review_after_days', 120)}).")
        print("!! The best-priced / best-quality models have likely changed. Before building:")
        print("!!   1. Research current model pricing and quality (web search, provider docs,")
        print("!!      or the claude-api skill if running under Claude Code).")
        print("!!   2. Update the candidate ranking and selected_at in config/model-selection.json.")
        print("!!   3. Re-run this script.")
        if not args.allow_stale:
            sys.exit(3)
        print("!! --allow-stale given: continuing with the old ranking.\n")

    id_key = "gemini-enterprise" if provider == "gemini-enterprise" else "anthropic"
    exports = {}
    for role, spec in cfg["roles"].items():
        chosen = None
        for cand in spec["candidates"]:
            model_id = cand["ids"].get(id_key)
            if not model_id:
                continue
            try:
                if provider == "gemini-enterprise":
                    ok, detail = probe_vertex(model_id, env["GOOGLE_CLOUD_PROJECT"],
                                              env.get("GOOGLE_CLOUD_LOCATION", "global"),
                                              env["GOOGLE_APPLICATION_CREDENTIALS"])
                else:
                    ok, detail = probe_anthropic(model_id, env["ANTHROPIC_API_KEY"])
            except Exception as e:  # network/auth problems count as unavailable
                ok, detail = False, str(e)[:80]
            print(f"  {role}: {cand['name']} ({model_id}) -> {'OK' if ok else 'unavailable'} [{detail}]")
            if ok:
                chosen = (cand, model_id)
                break
        if not chosen:
            print(f"!! no candidate available for role {role} on provider {provider}")
            sys.exit(2)
        cand, model_id = chosen
        exports[spec["env"]] = model_id
        print(f"  -> {role}: {cand['name']}  ({spec['env']}={model_id})\n")

    for k, v in exports.items():
        print(f"export {k}={v}")

    if args.apply:
        text = ENV_FILE.read_text()
        for k, v in exports.items():
            text, n = re.subn(rf"^{k}=.*$", f"{k}={v}", text, flags=re.M)
            if n == 0:
                text += f"\n{k}={v}\n"
        ENV_FILE.write_text(text)
        print(f"applied to {ENV_FILE}")


if __name__ == "__main__":
    main()
