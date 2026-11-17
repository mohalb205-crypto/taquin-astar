import random

GOAL = (1, 2, 3, 8, 0, 4, 7, 6, 5)
GOAL_POS = {v: divmod(i, 3) for i, v in enumerate(GOAL)}


def inversions(state):
    tiles = [t for t in state if t != 0]
    return sum(1 for i in range(len(tiles))
               for j in range(i + 1, len(tiles)) if tiles[i] > tiles[j])


def is_solvable(state):
    return inversions(state) % 2 == inversions(GOAL) % 2


def h(state):
    total = 0
    for i, v in enumerate(state):
        if v != 0:
            r, c = divmod(i, 3)
            gr, gc = GOAL_POS[v]
            total += abs(r - gr) + abs(c - gc)
    return total



def neighbors(state):
    b = state.index(0)
    r, c = divmod(b, 3)
    result = []
    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            n = nr * 3 + nc
            lst = list(state)
            lst[b], lst[n] = lst[n], lst[b]
            result.append(tuple(lst))
    return result

def astar(start):
    g_cost = {start: 0}
    parent = {start: None}
    OPEN = {start: h(start)}
    CLOSED = {}
    log = []

    while OPEN:
        fmin = min(OPEN.values())
        N = [n for n, f in OPEN.items() if f == fmin]

        if GOAL in N:
            log.append((GOAL, g_cost[GOAL], 0, g_cost[GOAL]))
            path, s = [], GOAL
            while s is not None:
                path.append(s)
                s = parent[s]
            return path[::-1], log

        nj = random.choice(N)
        del OPEN[nj]
        CLOSED[nj] = fmin
        g = g_cost[nj]
        log.append((nj, g, fmin - g, fmin))

        for nij in neighbors(nj):
            ng = g + 1
            f_new = ng + h(nij)

            if nij in CLOSED:
                if f_new < CLOSED[nij]:
                    del CLOSED[nij]
                    OPEN[nij] = f_new
                    g_cost[nij] = ng
                    parent[nij] = nj
            elif nij not in OPEN:
                OPEN[nij] = f_new
                g_cost[nij] = ng
                parent[nij] = nj
            elif f_new < OPEN[nij]:
                OPEN[nij] = f_new
                g_cost[nij] = ng
                parent[nij] = nj
    return None, log