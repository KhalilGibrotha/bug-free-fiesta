#!/usr/bin/env python3
"""
Test script to verify macros file exclusion logic
"""

def test_exclusion(file):
    """Test if a file should be excluded from document processing"""
    if (file == 'macros.j2' or 
        file.endswith('macros.j2') or 
        'macros' in file.lower() or
        file.startswith('_')):
        return True  # Should be excluded
    return False  # Should be processed

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
