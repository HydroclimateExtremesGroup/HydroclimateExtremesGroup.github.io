# Git Quick Reference Guide

## Standard Workflow for Pushing Changes

### Step 1: Check What Changed
```bash
git status
```
Shows which files have been modified, added, or deleted.

### Step 2: Stage Your Changes
```bash
# Stage all changes
git add .

# OR stage specific files
git add path/to/file.html
git add file1.html file2.html
```

### Step 3: Commit Your Changes
```bash
git commit -m "Description of your changes"
```
**Good commit message examples:**
- `git commit -m "Update team page with new member information"`
- `git commit -m "Fix styling on projects page"`
- `git commit -m "Add new publication to publications list"`
- `git commit -m "Update Wisconsin Rainfall Project page links"`

### Step 4: Push to GitHub
```bash
git push origin main
```
(Use `master` if your default branch is `master`)

## Quick One-Liner (All-in-One)
```bash
git add . && git commit -m "Your change description" && git push origin main
```

## Navigation
First, navigate to your project directory:
```bash
cd "/Users/daniel/Library/Mobile Documents/com~apple~CloudDocs/UW Documents/WebsiteStuff/GithubSite/her.github.io"
```

## Useful Commands

### View Changes
```bash
# See what files changed
git status

# See detailed line-by-line changes
git diff

# See changes for a specific file
git diff path/to/file.html
```

### Undo Changes (Before Committing)
```bash
# Unstage a file (keep changes, but don't commit)
git reset HEAD path/to/file.html

# Discard changes to a file (WARNING: This deletes your changes!)
git checkout -- path/to/file.html

# Discard all uncommitted changes (WARNING: This deletes all your changes!)
git reset --hard HEAD
```

### View History
```bash
# See commit history
git log

# See commit history (one line per commit)
git log --oneline
```

## Best Practices

1. **Commit Often**: Make small, focused commits rather than large ones
2. **Write Clear Messages**: Describe what you changed and why
3. **Check Before Committing**: Use `git status` and `git diff` to review changes
4. **Test Locally**: Verify your changes work before pushing

## GitHub Pages Deployment

- After pushing, GitHub Pages automatically deploys your site
- Usually takes 1-2 minutes for changes to appear live
- Your site URL: `https://hydroclimateextremesgroup.github.io/`

## Common Workflows

### Workflow 1: Single File Update
```bash
git add publications.html
git commit -m "Add new publication"
git push origin main
```

### Workflow 2: Multiple Related Changes
```bash
git add team/pi.html team/wentao_zhan.html
git commit -m "Update team member information"
git push origin main
```

### Workflow 3: All Changes
```bash
git add .
git commit -m "Update website content"
git push origin main
```

## Troubleshooting

### If you get "fatal: not a git repository"
Make sure you're in the correct directory:
```bash
cd "/Users/daniel/Library/Mobile Documents/com~apple~CloudDocs/UW Documents/WebsiteStuff/GithubSite/her.github.io"
```

### If you get "nothing to commit, working tree clean"
All your changes are already committed. No action needed.

### If you get authentication errors
You may need to set up GitHub authentication (SSH keys or personal access token).

---

**Quick Reference Card:**

```bash
cd "/path/to/project"
git status              # Check changes
git add .              # Stage all
git commit -m "..."    # Commit
git push origin main   # Push to GitHub
```

