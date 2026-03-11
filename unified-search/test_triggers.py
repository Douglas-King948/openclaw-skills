from global_search import search

# 模拟用户触发搜索的各种说法
test_queries = [
    'Python 教程',
    'OpenClaw 项目', 
    '机器学习',
    'Wikipedia',
    '技术方案',
]

print('触发词测试：')
for q in test_queries:
    print(f'搜索: "{q}"')
    r = search(q)
    if r.get('success'):
        print(f'  -> 成功，引擎: {r.get("engine_used", "unknown")}')
        if r.get('results'):
            print(f'  -> 第一条: {r[\"results\"][0][\"title\"][:50]}')
    else:
        print(f'  -> 失败: {r.get(\"error\", \"unknown\")}')
    print()
