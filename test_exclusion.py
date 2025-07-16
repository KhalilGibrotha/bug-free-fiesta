import sys
import os
from entrypoint import should_be_excluded as test_exclusion

#!/usr/bin/env python3
"""
Test script to verify macros file exclusion logic
"""

# Add the confluence-publisher action directory to the Python path
# to allow importing the exclusion logic directly.
# This assumes a standard project layout where the test script
# is run from the repository root.

# The following lines are removed as they are no longer needed.
# The test script now imports the exclusion logic directly from the
# confluence-publisher action's entrypoint script.
# This avoids duplicating the logic and ensures that the test
# is always running against the current implementation.

action_path = os.path.join(os.path.dirname(__file__), '.github/actions/confluence-publisher')
if os.path.isdir(action_path):
    sys.path.insert(0, action_path)
else:
    # Fallback for different execution environments
    # This path might need adjustment based on the actual project structure
    # and where the test is executed from.
    action_path = '.github/actions/confluence-publisher'
    if os.path.isdir(action_path):
        sys.path.insert(0, action_path)

try:
    # Import the actual exclusion function from the entrypoint script
except (ImportError, ModuleNotFoundError) as e:
    print(f"Error: Could not import 'should_be_excluded' from entrypoint.py.", file=sys.stderr)
    print(f"Please ensure '.github/actions/confluence-publisher/entrypoint.py' exists and is in the Python path.", file=sys.stderr)
    print(f"Attempted to add '{os.path.abspath(action_path)}' to sys.path.", file=sys.stderr)
    print(f"Original error: {e}", file=sys.stderr)
    # Define a dummy function to allow the script to exit gracefully
    def test_exclusion(file):
        """Dummy function to prevent script crash when import fails."""
        print("Import failed, returning False.", file=sys.stderr)
        return False


test_files = [
    'macros.j2',
    'docs_macros.j2', 
    'helper_macros.j2',
    '_includes.j2',
    'regular_doc.j2',
    'BRANCH_NAMING_GUIDE.j2',
    'aap_operations_manual.j2'
]

print('Testing exclusion logic:')
print('========================')
for file in test_files:
    excluded = test_exclusion(file)
    status = 'EXCLUDED' if excluded else 'PROCESSED'
    print(f'  {file:<25} -> {status}')

print('\nSummary:')
excluded_count = sum(1 for f in test_files if test_exclusion(f))
processed_count = len(test_files) - excluded_count
print(f'  Files excluded: {excluded_count}')
print(f'  Files processed: {processed_count}')
