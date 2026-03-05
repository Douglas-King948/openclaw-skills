from global_search import search

test_queries = [
    'Python tutorial',
    'OpenClaw',
    'machine learning',
]

for q in test_queries:
    print(f'Search: {q}')
    r = search(q)
    if r.get('success'):
        print(f'  OK - Engine: {r.get(\"engine_used\", \"unknown\")}')
    else:
        print(f'  FAIL')
