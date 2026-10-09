#!/usr/bin/env python3
"""CI gate for the sdd-st-dev plugin: manifests, frontmatter, links and the house conventions."""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors, checks = [], 0


def check(ok, okmsg, failmsg):
    global checks
    checks += 1
    print(("  ok   " if ok else "  FAIL ") + (okmsg if ok else failmsg))
    if not ok:
        errors.append(failmsg)


def frontmatter(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None, text
    fm, key = {}, None
    for line in m.group(1).splitlines():
        km = re.match(r"^([a-z_]+):\s*(.*)$", line)
        if km:
            key, val = km.group(1), km.group(2).strip()
            fm[key] = val
        elif key and line.startswith("  "):
            fm[key] = (fm[key] + " " + line.strip()).strip()
    return fm, text


print("== manifests ==")
plugin = json.loads((ROOT / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
market = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
entry = next((p for p in market.get("plugins", []) if p.get("name") == plugin.get("name")), None)
check(entry is not None, "marketplace lists the plugin", "marketplace.json has no entry named like plugin.json")
check(bool(re.fullmatch(r"\d+\.\d+\.\d+", plugin.get("version", ""))), "semver version", "plugin.json version is not semver")
if entry:
    for k in ("version", "description"):
        check(entry.get(k) == plugin.get(k), f"marketplace {k} matches", f"marketplace {k} differs from plugin.json")

print("== skills ==")
skills = sorted(p.parent.name for p in (ROOT / "skills").glob("*/SKILL.md"))
agents = sorted(p.stem for p in (ROOT / "agents").glob("*.md"))
for name in skills:
    p = ROOT / "skills" / name / "SKILL.md"
    fm, text = frontmatter(p)
    check(fm is not None and fm.get("name") == name, f"{name}: frontmatter name", f"{name}: frontmatter name must equal the dir name")
    check(bool(fm and fm.get("description", "").strip(" >")), f"{name}: description", f"{name}: missing description")
    used = re.findall(r"[\w-]+", (fm or {}).get("agents", ""))
    for a in used:
        check(a in agents, f"{name}: agent {a} exists", f"{name}: declares unknown agent '{a}'")
    check("house-rules.md" in text, f"{name}: links house-rules", f"{name}: must link ../_shared/house-rules.md")
    check(re.search(r"structural\s+self-check", text) is not None, f"{name}: names its structural self-check", f"{name}: must name its 'structural self-check'")
    check("git commit" not in text or "Never" in text or "never" in text, f"{name}: never commits", f"{name}: mentions git commit without forbidding it")

print("== agents ==")
for name in agents:
    fm, _ = frontmatter(ROOT / "agents" / f"{name}.md")
    check(fm is not None and fm.get("name") == name, f"{name}: frontmatter name", f"agents/{name}.md: name must equal file name")
    for k in ("description", "model"):
        check(bool(fm and fm.get(k)), f"{name}: {k}", f"agents/{name}.md: missing {k}")

print("== links ==")
docs = list((ROOT / "skills").rglob("*.md")) + list((ROOT / "agents").glob("*.md")) + [ROOT / "README.md"]
for d in docs:
    for target in re.findall(r"\]\((\.{1,2}/[^)#\s]+)", d.read_text(encoding="utf-8")):
        check((d.parent / target).resolve().exists(), f"{d.relative_to(ROOT)} → {target}",
              f"broken link in {d.relative_to(ROOT)}: {target}")

print("== invocation form & removed commands ==")
PREFIX = plugin["name"]
removed = ("specify", "clarify", "design", "sequences", "data-model", "api", "tasks", "plan-tests",
           "implement", "ship", "survey", "scaffold", "roadmap", "interview", "config", "glossary",
           "classify-size", "decide-adr", "design-system", "ux-flows", "screens")
for d in docs:
    text = d.read_text(encoding="utf-8")
    old = re.findall(r"(?<![\w/-])/sdd:[\w-]+", text)
    check(not old, f"{d.relative_to(ROOT)}: /{PREFIX}:<name> form", f"{d.relative_to(ROOT)}: old /sdd: command prefix {old}")
    stale = sorted({c for c in removed if re.search(rf"/{re.escape(PREFIX)}:{re.escape(c)}\b", text)})
    check(not stale, f"{d.relative_to(ROOT)}: no removed commands", f"{d.relative_to(ROOT)}: references removed commands {stale}")

print("== _shared no-orphan ==")
corpus = "\n".join(d.read_text(encoding="utf-8") for d in docs)
for s in sorted((ROOT / "skills/_shared").glob("*.md")):
    check(corpus.count(s.name) > 0, f"_shared/{s.name} is referenced", f"_shared/{s.name} is referenced by nothing")

print("== skill list in README ==")
readme = (ROOT / "README.md").read_text(encoding="utf-8")
for name in skills:
    check(f"/{plugin['name']}:{name}" in readme, f"README documents /{plugin['name']}:{name}", f"README never mentions /{plugin['name']}:{name}")

print()
if errors:
    print(f"FAILED: {len(errors)} error(s) out of {checks} checks")
    sys.exit(1)
print(f"PASSED: {checks} checks")
