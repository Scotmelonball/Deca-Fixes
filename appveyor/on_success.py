import sys
import os
import subprocess
import datetime
import json

if len(sys.argv) < 4:
    print('WARNING: NEED AT LEAST THREE PARAMETERS: <STATUS> <CHANGELOG> <WEBHOOK_URL>.')
    sys.exit(1)

status = sys.argv[1]
changelog_fn = sys.argv[2]
webhook_url = sys.argv[3]

print('Running Script...')
print(f'Status: {status}')
print(f'Changelog File: {changelog_fn}')
print(f'Webhook URL: {webhook_url}')

APPVEYOR_REPO_COMMIT = os.environ.get("APPVEYOR_REPO_COMMIT", None)
APPVEYOR_BUILD_VERSION = os.environ.get("APPVEYOR_BUILD_VERSION", None)
APPVEYOR_BUILD_NUMBER = os.environ.get("APPVEYOR_BUILD_NUMBER", None)
APPVEYOR_REPO_NAME = os.environ.get("APPVEYOR_REPO_NAME", None)
APPVEYOR_REPO_BRANCH = os.environ.get("APPVEYOR_REPO_BRANCH", None)
APPVEYOR_JOB_ID = os.environ.get("APPVEYOR_JOB_ID", None)

# Print environment variables
print(f'APPVEYOR_REPO_COMMIT: {APPVEYOR_REPO_COMMIT}')
print(f'APPVEYOR_BUILD_VERSION: {APPVEYOR_BUILD_VERSION}')
print(f'APPVEYOR_BUILD_NUMBER: {APPVEYOR_BUILD_NUMBER}')
print(f'APPVEYOR_REPO_NAME: {APPVEYOR_REPO_NAME}')
print(f'APPVEYOR_REPO_BRANCH: {APPVEYOR_REPO_BRANCH}')
print(f'APPVEYOR_JOB_ID: {APPVEYOR_JOB_ID}')

# Fallback to git for commit hash if not found in environment
if not APPVEYOR_REPO_COMMIT:
    result = subprocess.run(['git', 'log', '-1', '--pretty=%H'], stdout=subprocess.PIPE)
    APPVEYOR_REPO_COMMIT = result.stdout.decode('utf-8').strip()
    print(f'Fallback Commit Hash (git): {APPVEYOR_REPO_COMMIT}')

# Extract commit metadata
result = subprocess.run(['git', 'log', '-1', APPVEYOR_REPO_COMMIT, '--pretty=%s'], stdout=subprocess.PIPE)
COMMIT_SUBJECT = result.stdout.decode('utf-8').strip()
print(f'Commit Subject: {COMMIT_SUBJECT}')

result = subprocess.run(['git', 'log', '-1', APPVEYOR_REPO_COMMIT, '--pretty=%aN'], stdout=subprocess.PIPE)
AUTHOR_NAME = result.stdout.decode('utf-8').strip()
print(f'Author Name: {AUTHOR_NAME}')

# Read the changelog file
try:
    with open(changelog_fn, 'r') as f:
        changelog = f.read().strip()
        print('Changelog:')
        print(changelog)
except FileNotFoundError:
    print(f'WARNING: Changelog file not found: {changelog_fn}')
    changelog = ""

# Simulate webhook data
WEBHOOK_DATA = {
    "status": status,
    "commit": {
        "subject": COMMIT_SUBJECT,
        "author": AUTHOR_NAME,
    },
    "changelog": changelog,
}

print('---- WEBHOOK_DATA ----')
print(json.dumps(WEBHOOK_DATA, indent=2))
print('---- END ----')

# Final status message
print('SUCCESS')
