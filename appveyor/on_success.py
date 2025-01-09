import sys
import os

if len(sys.argv) < 2:
    print('WARNING: NEED AT LEAST TWO PARAMETERS: <STATUS> <CHANGELOG>.')
    sys.exit(1)

status = sys.argv[1]
changelog_fn = sys.argv[2]

print('Running Script...')
print(f'Status: {status}')
print(f'Changelog File: {changelog_fn}')

# You can add additional processing here if needed.
print('SUCCESS')
