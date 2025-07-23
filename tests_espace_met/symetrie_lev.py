# Implémentation simple de la distance de Levenshtein (edit distance)
def levenshtein_distance(a, b):
    n, m = len(a), len(b)
    if n > m:
        a, b = b, a
        n, m = m, n

    current = list(range(n + 1))
    for i in range(1, m + 1):
        previous, current = current, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous[j] + 1, current[j - 1] + 1, previous[j - 1]
            if a[j - 1] != b[i - 1]:
                change += 1
            current[j] = min(add, delete, change)
    return current[n]

# Recalcul avec la vraie distance de Levenshtein
reliable_matches_lev, D_lev = match_with_metric_filtering(P, T, levenshtein_distance)
reliable_matches_lev, D_lev.round(1)
