"""Heaps (binary and d-ary) and binary search trees.

Data: data/animations/trees.json. Each entry is simulated at build time and
checked against the expected answer; the build stops on any difference.
"""
from .common import _list


def heap_ops(spec):
    """Binary or d-ary heap: insert (sift up), delete the root (sift down) and bottom-up build.

    Each step records the array, the indices being compared or swapped, and a note.
    """
    d, kind = spec.get('arity', 2), spec.get('kind_of_heap', 'max')
    better = (lambda a, b: a > b) if kind == 'max' else (lambda a, b: a < b)
    word = 'larger' if kind == 'max' else 'smaller'
    a = list(spec.get('start', []))
    steps = [dict(arr=list(a), hi=[], note=(f"Start: the {kind}-heap " + str(a) + '.') if a else f"Start with an empty {kind}-heap.")]
    parent = lambda i: (i - 1) // d
    kids = lambda i: [c for c in range(d * i + 1, d * i + d + 1) if c < len(a)]

    def sift_down(i, n_note=''):
        while True:
            cs = kids(i)
            if not cs:
                steps.append(dict(arr=list(a), hi=[i], note=f"{a[i]} is now a leaf at index {i}, so it stops." if n_note else f"{a[i]} at index {i} has no children, so it stays."))
                return
            best = cs[0]
            for c in cs[1:]:
                if better(a[c], a[best]):
                    best = c
            listing = ', '.join(str(a[c]) for c in cs)
            if better(a[best], a[i]):
                steps.append(dict(arr=list(a), hi=[i, best], note=f"{a[i]} at index {i} has children {listing}; the {word} child {a[best]} beats it, so they swap."))
                a[i], a[best] = a[best], a[i]
                i, n_note = best, 'moved'
            else:
                steps.append(dict(arr=list(a), hi=[i], note=f"{a[i]} at index {i} has children {listing}; none beats it, so it stays."))
                return

    for op in spec['ops']:
        if op[0] == 'insert':
            for k in op[1]:
                a.append(k)
                i = len(a) - 1
                if i == 0:
                    steps.append(dict(arr=list(a), hi=[0], note=f"Insert {k}: it becomes the root."))
                    continue
                steps.append(dict(arr=list(a), hi=[i], note=f"Insert {k}: append it at index {i}, below {a[parent(i)]} at index {parent(i)}."))
                while i > 0 and better(a[i], a[parent(i)]):
                    q = parent(i)
                    a[i], a[q] = a[q], a[i]
                    steps.append(dict(arr=list(a), hi=[q, i], note=f"{k} beats its parent {a[i]}, so they swap; {k} moves up to index {q}."))
                    i = q
                if i > 0:
                    steps[-1]['note'] += f" {k} does not beat its parent {a[parent(i)]}, so it stops."
                else:
                    steps[-1]['note'] += f" {k} is now the root."
        elif op[0] == 'delete':
            for _ in range(op[1]):
                top, last = a[0], a.pop()
                if not a:
                    steps.append(dict(arr=[], hi=[], note=f"Remove {top}; the heap is now empty."))
                    continue
                a[0] = last
                steps.append(dict(arr=list(a), hi=[0], note=f"Remove the root {top}. Move the last element {last} to the root."))
                sift_down(0)
        elif op[0] == 'build':
            a = list(op[1])
            last_parent = parent(len(a) - 1)
            steps.append(dict(arr=list(a), hi=[], note=f"Build a {kind}-heap bottom-up: sift down each node that has children, from index {last_parent} back to 0."))
            for i in range(last_parent, -1, -1):
                sift_down(i)
        else:
            raise SystemExit('Unknown heap operation: ' + op[0])
    return steps, a


def heap_animation(qid, spec):
    steps, a = heap_ops(spec)
    want = spec['expect']
    got = a[:len(want)] if spec.get('prefix') else a
    if got != want:
        raise SystemExit(f'Animation for {qid} ends with {a}, not {want}')
    note = 'All done. Level order: ' + ', '.join(map(str, a)) + '.'
    if spec.get('prefix'):
        note += ' The first ' + str(len(want)) + ' entries: ' + ', '.join(map(str, want)) + '.'
    steps.append(dict(arr=list(a), hi=[], final=True, note=note))
    d = spec.get('arity', 2)
    title = ('Ternary ' if d == 3 else '') + ('max' if spec.get('kind_of_heap', 'max') == 'max' else 'min') + '-heap' + (f', children of i at {d}i+1 to {d}i+{d}' if d != 2 else '')
    return dict(kind='heap', arity=d, schedules=[dict(short='Heap', title=title[0].upper() + title[1:], steps=steps)], count=len(steps))


def bst_build(keys):
    """Insert keys in order into an unbalanced BST. Returns parent links, depths and steps."""
    root, left, right, depth, parent = None, {}, {}, {}, {}
    steps = [dict(shown=[], path=[], note='Start with an empty tree. Smaller keys go left, larger keys go right.')]
    for k in keys:
        if k in depth:
            raise SystemExit(f'Duplicate BST key {k}')
        if root is None:
            root, depth[k] = k, 0
            steps.append(dict(shown=list(depth), path=[k], key=k, note=f"Insert {k}: the tree is empty, so {k} is the root."))
            continue
        node, path, moves = root, [], []
        while True:
            path.append(node)
            side = left if k < node else right
            moves.append(f"{k} {'<' if k < node else '>'} {node}, go {'left' if k < node else 'right'}")
            if node in side:
                node = side[node]
            else:
                side[node] = k
                parent[k], depth[k] = node, depth[node] + 1
                break
        steps.append(dict(shown=list(depth), path=path + [k], key=k, note=f"Insert {k}: " + '; '.join(moves) + f". It becomes the {'left' if k < node else 'right'} child of {node}."))
    return dict(root=root, left=left, right=right, depth=depth, parent=parent), steps


def bst_animation(qid, spec):
    keys = spec['keys']
    tree, steps = bst_build(keys)
    if spec.get('from_preorder'):
        steps[0]['note'] = 'Inserting the keys in preorder rebuilds the same tree: each key arrives after its ancestors. ' + steps[0]['note']
    left, right, depth = tree['left'], tree['right'], tree['depth']
    order = []

    def walk(n, kind):
        if n is None:
            return
        if kind == 'preorder':
            order.append(n)
        walk(left.get(n), kind)
        if kind == 'inorder':
            order.append(n)
        walk(right.get(n), kind)
        if kind == 'postorder':
            order.append(n)

    q, want = spec['query'], spec['expect']
    note = 'All done.'
    traversal = None
    if q in ('inorder', 'preorder', 'postorder'):
        walk(tree['root'], q)
        got = order
        traversal = order
        # Show the traversal one node at a time.
        rule = {'inorder': 'left subtree, node, right subtree', 'preorder': 'node, left subtree, right subtree', 'postorder': 'left subtree, right subtree, node'}[q]
        steps.append(dict(shown=list(depth), path=[], out=[], note=f"Now the {q} traversal: {rule}."))
        for i, n in enumerate(order):
            steps.append(dict(shown=list(depth), path=[n], out=order[:i + 1], note=f"Visit {n} (position {i + 1})."))
        note += f" {q.capitalize()}: " + ', '.join(map(str, order)) + '.'
        if spec.get('position_of') is not None:
            got = order.index(spec['position_of']) + 1
            note += f" {spec['position_of']} is at position {got}."
    elif q == 'height':
        got = max(depth.values())
        deepest = [k for k in keys if depth[k] == got]
        note += f" The deepest node{'s are' if len(deepest) > 1 else ' is'} {_list([str(x) for x in deepest])}, {got} edges below the root, so the height is {got}."
    elif q == 'deepest':
        h = max(depth.values())
        got = [k for k in keys if depth[k] == h]
        note += f" The deepest level is {h} edges below the root: {_list([str(x) for x in got])}."
    elif q == 'depth':
        got = depth[spec['node']]
        path, n = [spec['node']], spec['node']
        while n in tree['parent']:
            n = tree['parent'][n]
            path.append(n)
        note += f" The path from {spec['node']} to the root is {' → '.join(map(str, path))}: {got} edges."
    elif q == 'subtrees':
        r = tree['root']

        def size(n):
            return 0 if n is None else 1 + size(left.get(n)) + size(right.get(n))
        got = [size(left.get(r)), size(right.get(r))]
        note += f" The root {r} has {got[0]} nodes in its left subtree and {got[1]} in its right."
    else:
        raise SystemExit(f'Unknown BST query for {qid}: {q}')
    if got != want:
        raise SystemExit(f'Animation for {qid} gives {got}, not {want}')
    steps.append(dict(shown=list(depth), path=[], out=traversal, final=True, note=note))
    rank = {k: i for i, k in enumerate(sorted(keys))}
    nodes = [[k, rank[k], depth[k], tree['parent'].get(k)] for k in keys]
    return dict(kind='bst', nodes=nodes, schedules=[dict(short='BST', title='Binary search tree' + (', built from its preorder' if spec.get('from_preorder') else ''), steps=steps)], count=len(steps))



# Animation kinds this family provides, and the player file that draws them.
KINDS = {'heap': heap_animation, 'bst': bst_animation}
PLAYER = 'trees'
