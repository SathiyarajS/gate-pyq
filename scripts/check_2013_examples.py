#!/usr/bin/env python3
"""Reproduce selected checks for GATE 2013 CS booklet A.

Printed CS48 / normalized Q58: finite spill-witness simulation.
Printed CS50–51 / normalized Q60–61: exhaustive replacement-map testing.
Printed CS54 / normalized Q64: exhaustive candidate-key enumeration.

These checks complement the independent derivations and source/key review.
They do not prove all solutions, register lower bounds, or universal correctness
of the spill witness. No question records or repository files are modified.
Run with Python 3; no third-party dependencies are needed.
"""
from itertools import combinations, product


def check_replacement_maps():
    """Enumerate all 5^5 inputs separately for each of the four printed maps."""
    cases = [
        ('abc', 'dab', 'dabde', 'dabde', 0),
        ('cde', 'bcd', 'abbcd', 'abbcd', 0),
        ('bca', 'cda', 'acdde', 'addde', 2101),
        ('abc', 'bac', 'bacde', 'aacde', 2101),
    ]
    failures = []
    for case, (old, new, expected_sample, actual_sample, expected_count) in enumerate(cases, 1):
        mapping = dict(zip(old, new))

        def correct_replacement(s):
            # Each result depends only on its original character.
            return ''.join(mapping.get(c, c) for c in s)

        def printed_procedure(s):
            out = []
            for c in s:
                for oldc, newc in zip(old, new):
                    if c == oldc:
                        c = newc
                out.append(c)
            return ''.join(out)

        assert correct_replacement('abcde') == expected_sample
        assert printed_procedure('abcde') == actual_sample
        count = sum(
            correct_replacement(s) != printed_procedure(s)
            for s in map(''.join, product('abcde', repeat=5))
        )
        assert count == expected_count, (case, count)
        failures.append(count)
        print(f'Replacement case {case}: {count}/3125 inputs expose the flaw; '
              f'abcde should become {expected_sample}, actually becomes {actual_sample}.')
    assert [i + 1 for i, count in enumerate(failures) if count] == [3, 4]
    return len(cases) * 5**5


def check_candidate_keys():
    """Compute closure for all 2^8 subsets and test minimal superkeys."""
    attributes = frozenset('ABCDEFGH')
    dependencies = [
        (frozenset(left), frozenset(right))
        for left, right in [('CH', 'G'), ('A', 'BC'), ('B', 'CFH'),
                            ('E', 'A'), ('F', 'EG')]
    ]

    def closure(seed):
        result = set(seed)
        while True:
            before = result.copy()
            for left, right in dependencies:
                if left <= result:
                    result.update(right)
            if result == before:
                return frozenset(result)

    all_subsets = [
        frozenset(subset)
        for size in range(9)
        for subset in combinations(sorted(attributes), size)
    ]
    closures = {subset: closure(subset) for subset in all_subsets}
    superkeys = [subset for subset in all_subsets if closures[subset] == attributes]
    candidate_keys = {
        ''.join(sorted(key))
        for key in superkeys
        if not any(other < key for other in superkeys)
    }
    assert candidate_keys == {'AD', 'BD', 'DE', 'DF'}, candidate_keys
    assert all('D' in key for key in superkeys)
    for attribute in 'ABEF':
        assert closure(attribute) == attributes - {'D'}
    prime = set(''.join(candidate_keys))
    assert prime == set('ABDEF')
    assert 'C' not in prime and 'C' in closure('A')
    print('Candidate keys from all 256 attribute subsets: '
          + ', '.join(sorted(candidate_keys)) + '.')
    return len(all_subsets)


def check_spill_witness():
    """Compare branch-relevant results on all integer pairs in [-12, 12]^2.

    Arithmetic uses Python integers, corresponding to the unbounded-arithmetic
    model. The tested magnitudes also fit a conventional signed 32-bit model.
    Input register loading is not a spill. S is the sole spill slot. Results on
    the unchosen branch, and all values after the segment, are dead as specified.
    """
    branches = set()
    checked = 0
    for a in range(-12, 13):
        for b in range(-12, 13):
            # Printed order, retaining the relevant results for comparison.
            c = a + b
            d = c * a
            e = c + a
            x = c * c
            if x > a:
                expected = ('true', a * a)
            else:
                expected = ('false', d * d, e * e)

            # Two-register code after permitted code motion.
            r1, r2 = a, b
            stores = reloads = 0
            r2 = r1 + r2               # c
            spill_slot = r2            # store c once
            stores += 1
            r2 = r2 * r2               # x overwrites c
            if r2 > r1:
                r1 = r1 * r1           # y
                actual = ('true', r1)
            else:
                r2 = spill_slot        # reload c
                reloads += 1
                r2 = r2 * r1           # d
                r2 = r2 * r2           # d squared, then dead
                observed_d_squared = r2
                # observed_d_squared is test instrumentation, not a machine register.
                r2 = spill_slot        # reload c
                reloads += 1
                r2 = r2 + r1           # e
                r2 = r2 * r2           # e squared, then dead
                actual = ('false', observed_d_squared, r2)
            assert actual == expected, (a, b, expected, actual)
            assert stores == 1
            assert reloads == (0 if actual[0] == 'true' else 2)
            branches.add(actual[0])
            checked += 1
    assert branches == {'true', 'false'}, branches
    print(f'Spill witness: {checked} input pairs match; both branches exercised; '
          'one spill store, zero or two reloads.')
    return checked


def main():
    replacement_count = check_replacement_maps()
    subset_count = check_candidate_keys()
    spill_count = check_spill_witness()
    print(f'PASS: {replacement_count} replacement-map cases, {subset_count} FD subsets, '
          f'{spill_count} spill-witness input pairs.')
    print('Scope: selected exhaustive/finite examples only, not proof of every solution '
          'or of the register lower bounds.')


if __name__ == '__main__':
    main()
