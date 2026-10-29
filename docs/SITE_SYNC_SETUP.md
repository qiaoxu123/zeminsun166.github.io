# Academic homepage: checked cross-repository synchronization

## Repositories and public URL

- **Editable source:** `qiaoxu123/zeminsun166.github.io`, branch `site-source`.
- **Live GitHub Pages repository:** `zeminsun166/zeminsun166.github.io`, branch `main`.
- **Public website stays:** https://zeminsun166.github.io/

Do not transfer or rename the live repository.

## One-time credential setup (required)

1. Sign in to GitHub as **zeminsun166** (the owner of the live website).
2. Open **Settings > Developer settings > Personal access tokens > Fine-grained tokens**, and generate a token whose **Resource owner** is `zeminsun166`.
3. Limit the token to **only** repository `zeminsun166.github.io`, and grant **Contents: Read and write** (Metadata: Read is automatic). A token expiration date is recommended. The target repo's workflows are deliberately excluded from synchronization, so the token does not need Actions or Workflows write access.
4. As **qiaoxu123**, go to https://github.com/qiaoxu123/zeminsun166.github.io/settings/secrets/actions and create repository secret **SITE_SYNC_TOKEN** with that token value. Never put the token in a commit, PR, or chat.
5. Ensure Actions is enabled for the source fork. Check https://github.com/qiaoxu123/zeminsun166.github.io/actions . If GitHub displays "Enable workflows", enable them.
6. Confirm the **original** repository's **Settings > Pages > Build and deployment** still uses its existing publishing source (normally branch `main` and root `/`). No changes to the live Pages settings are required.

## Daily workflow

1. Create a work branch from `site-source` in the qiaoxu123 repository.
2. Open a pull request **into `site-source`**. The **Validate and sync academic homepage** workflow checks bilingual content and builds Jekyll without using any token.
3. Review the changes and merge the PR into `site-source` only after validation passes.
4. A push to `site-source` runs the same checks again; only successful checks allow synchronization to the original repo's `main`.
5. The source workflow keeps target-specific `.github` files (including the Google Scholar crawler) and omits source-only validation/setup files. Target updates are **normal, non-force pushes**.
6. GitHub Pages publishes from the original repository without changing the URL.

**Strongly recommended:** protect the `site-source` branch with a GitHub ruleset requiring PR review and a passing `Check bilingual content and build Jekyll` status check. Without the ruleset, contributors with direct push rights could publish after automatic validation without human review.

## Safeguards and failure handling

- A missing/expired `SITE_SYNC_TOKEN` stops the sync job; the live website remains untouched.
- The first sync permits target `main` only at baseline `f56d991bbe466130bfecc060ace8a053cbb9c33d`. Later syncs require that the previous live commit was created by this sync process and its source commit is an ancestor of the new source head. Independent edits to target `main` cause the job to **stop** instead of overwriting changes.
- The target GitHub Pages repository's `.github` folder is preserved, and no `git push --force` is used.
- The workflow uses a scoped PAT rather than `GITHUB_TOKEN` to allow the live repo's branch-based GitHub Pages build to trigger.
- If a check fails, inspect the Actions job logs and fix the source branch. **Do not force-push** the live site.
- To stop future deployments immediately, disable the **Validate and sync academic homepage** workflow in the source fork or delete/rotate the `SITE_SYNC_TOKEN` secret.

## Initial update in this repository

The `site-source` branch includes the reviewed bilingual homepage changes from commit `7c0312afc2fbe7be4cc218cb7366412d61dbb3c8`, with the Chinese webpage title unchanged as `孙泽敏`. Configure the secret and run the next validated push to `site-source` to publish those changes.
