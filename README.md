# repo-template

Copier template plus GitHub settings sync for my repos. One template, `language`
is the question: `rust`, `python` or `none`.

## Scaffold a repo

```bash
mise run repo:new -- ../myrepo        # or: copier copy . ../myrepo
cd ../myrepo && mise run repo:sync    # GitHub settings, labels, rulesets
```

`repo_name` defaults to the target folder name.

| answer | default | drives |
|---|---|---|
| `repo_name` | folder name | release-please package name |
| `github_user` | `trash-panda-v91-beta` | CODEOWNERS |
| `language` | `rust` | `.mise.toml` tools, `hk.pkl` linters, Dockerfile |
| `container` | `false` | Dockerfile and the GHCR publish workflow |
| `release_please` | `true` | release workflow and release-please config |

## What lands in the repo

- workflows: auto-approve (label gated, cl4 also approves trashbot dependency
  PRs that are not `type/major`, never release PRs), automerge (renovate and
  release branches only), code quality checks, PR conventions, release-please,
  renovate, GHCR publish
- tooling: `.mise.toml` with check/fix/test and `repo:sync`, `hk.pkl` linters,
  actionlint, rumdl, tombi, yamlfmt, yamllint, shellcheck
- editor configs, `renovate.json`, CODEOWNERS (you plus the two bots), labeler

## repo:sync

Pushes the GitHub side state a template cannot: squash-only merge settings,
secret scanning, the standard labels, and the four rulesets (branch protection,
CI checks, PR requirements with code owner review on, tests). Run it any time to
re-converge drift.

```bash
mise run repo:sync -- owner/name      # or inside the repo: mise run repo:sync
EXTRA_CHECKS="CodeQL" mise run repo:sync -- owner/nix-repo
```

It reports the names the bots need; values stay with you.

```bash
gh secret set CL4_APP_PRIVATE_KEY -R owner/name
gh secret set TRASHBOT_APP_PRIVATE_KEY -R owner/name
CL4_APP_ID=... TRASHBOT_APP_ID=... mise run repo:sync -- owner/name
```
