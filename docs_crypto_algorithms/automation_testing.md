<!--
SPDX-FileContributor: SCANOSS
SPDX-License-Identifier: CC0-1.0
-->

# Testing the automation workflows

The three GitHub Actions in this repo are:

| Workflow | Trigger | Output |
| -------- | ------- | ------ |
| `keywords-changed.yml`              | `push` to `main` under `keywords/**`   | PR regenerating `dist/*.json` |
| `spdx-changed.yml`                  | daily cron + `workflow_dispatch`       | PR with submodule bump, SQL, stubs |
| `propagate-to-platform-deployment.yml` | `push` to `main` under `dist/**` or `sql/**` | PR in `scanoss/platform_deployment` |

This document covers how to exercise each one without affecting SPDX
`main` or production platform_deployment.

## One-time setup

### 1. `PLATFORM_DEPLOYMENT_TOKEN`

Create a PAT (fine-grained recommended) with:

- Repository access: `scanoss/platform_deployment`
- Permissions: `Contents: read & write`, `Pull requests: read & write`

Add it as a repo secret in this repo: **Settings → Secrets and variables →
Actions → New repository secret** named `PLATFORM_DEPLOYMENT_TOKEN`.

For early testing, point the workflow at a private sandbox copy of
platform_deployment (set `TARGET_REPO` in
`propagate-to-platform-deployment.yml` to that fork).

### 2. SPDX test fork

The fork at [`scanoss-qg/crypto-algorithms`](https://github.com/scanoss-qg/crypto-algorithms)
is used as the synthetic upstream during workflow dry-runs (do **not**
push commits to `spdx/cryptographic-algorithm-list:main` for testing).

Sync it once with upstream:

```sh
gh repo sync scanoss-qg/crypto-algorithms --source spdx/cryptographic-algorithm-list
```

## Local dry-run (no Actions involved)

Everything the workflow does can be run locally first.

### keywords change

```sh
# Pretend you've edited a keyword YAML
echo "# touch" >> keywords/aes.yaml
git restore keywords/aes.yaml  # discard once happy

python scripts/validate_consistency.py --json dist/inconsistency_report.json
python scripts/build_linked_dataset.py
git diff dist/
```

### SPDX change

```sh
# 1. Point the submodule at the fork
git -C external/spdx-crypto remote set-url origin https://github.com/scanoss-qg/crypto-algorithms.git
git -C external/spdx-crypto fetch origin

# 2. In another working copy of the fork, inject a synthetic change
#    (rename a yaml, edit a name, etc.) and push to its main.

# 3. Pull the new SHA in the submodule
git -C external/spdx-crypto checkout origin/main

# 4. Run the detector + SQL generator
python scripts/detect_spdx_changes.py --out /tmp/diff.json
python scripts/generate_sql.py --diff /tmp/diff.json --out sql --timestamp test01

# 5. Inspect generated files
ls sql/
cat sql/test01__all.sql

# 6. When done, restore submodule upstream
git -C external/spdx-crypto remote set-url origin https://github.com/spdx/cryptographic-algorithm-list.git
git submodule update --init --recursive
git checkout dist/spdx_snapshot.json
rm -rf sql/test01__*
```

## Workflow dry-run via `workflow_dispatch`

Once secrets are in place and the branch is pushed:

### Test `spdx-changed.yml` against the fork

```sh
gh workflow run spdx-changed.yml \
  -f spdx_repo_url=https://github.com/scanoss-qg/crypto-algorithms.git \
  -f spdx_ref=origin/main
```

Open the workflow run in the Actions tab and verify:

1. The "Fetch latest SPDX state" step picks up the fork.
2. The "Detect changes vs snapshot" step emits a non-empty diff (if you
   injected changes) or short-circuits cleanly (if you didn't).
3. If a diff was detected, a PR named `bot/spdx-sync` appears with all
   expected files.

### Test `keywords-changed.yml`

Push a commit to `main` that modifies a `keywords/*.yaml` file. The
workflow regenerates `dist/*.json` and opens `bot/regen-dist-keywords`.

### Test `propagate-to-platform-deployment.yml`

Merge any of the PRs above into `main`. The propagation workflow fires on
the resulting push and opens a PR in the target repo. Verify the PR body
references the source commit short SHA.

## Cleanup after testing

- Close auto-opened PRs without merging if they were synthetic.
- `git -C external/spdx-crypto remote set-url origin https://github.com/spdx/cryptographic-algorithm-list.git`
- `git submodule update --init --recursive`
- Delete any synthetic SQL files under `sql/`.
- Restore `dist/spdx_snapshot.json` from `main` if you committed a synthetic snapshot.
