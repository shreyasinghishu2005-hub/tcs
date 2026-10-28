import sys
import math


EPS = 1e-8


def cross(ax, ay, bx, by):
    return ax * by - ay * bx


def segment_intersection(a, b, c, d):
    """Return intersection point of two non-parallel segments, if it lies on both."""
    ax, ay = a
    bx, by = b
    cx, cy = c
    dx, dy = d

    rx, ry = bx - ax, by - ay
    sx, sy = dx - cx, dy - cy
    den = cross(rx, ry, sx, sy)

    if abs(den) < EPS:
        # Parallel/collinear overlaps are not expected in the input.
        return None

    qpx, qpy = cx - ax, cy - ay
    t = cross(qpx, qpy, sx, sy) / den
    u = cross(qpx, qpy, rx, ry) / den

    if -EPS <= t <= 1 + EPS and -EPS <= u <= 1 + EPS:
        x = ax + t * rx
        y = ay + t * ry
        return (round(x + 0.0, 2), round(y + 0.0, 2))
    return None


def point_key(p):
    return (round(p[0], 2), round(p[1], 2))


def distance(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def polygon_area(poly):
    area2 = 0.0
    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % len(poly)]
        area2 += x1 * y2 - x2 * y1
    return abs(area2) / 2.0


def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return

    n = int(data[0])
    sticks = []
    pos = 1
    for _ in range(n):
        x1, y1, x2, y2 = map(float, data[pos:pos + 4])
        pos += 4
        sticks.append(((x1, y1), (x2, y2)))

    # Collect all endpoints and intersections on each stick.
    points_on_stick = [[point_key(a), point_key(b)] for a, b in sticks]
    for i in range(n):
        for j in range(i + 1, n):
            p = segment_intersection(sticks[i][0], sticks[i][1],
                                     sticks[j][0], sticks[j][1])
            if p is not None:
                points_on_stick[i].append(p)
                points_on_stick[j].append(p)

    # Split every stick at all intersection points and build a graph.
    graph = {}
    edge_lengths = {}
    total_length = 0.0

    for i, (a, b) in enumerate(sticks):
        total_length += distance(a, b)
        ax, ay = a
        bx, by = b
        dx, dy = bx - ax, by - ay
        denom = dx * dx + dy * dy

        unique_points = list(set(points_on_stick[i]))
        unique_points.sort(
            key=lambda p: ((p[0] - ax) * dx + (p[1] - ay) * dy) / denom
            if denom > EPS else 0
        )

        for p in unique_points:
            graph.setdefault(p, [])

        for p, q in zip(unique_points, unique_points[1:]):
            if p == q:
                continue
            length = distance(p, q)
            # Store each geometric edge once.
            e = tuple(sorted((p, q)))
            if e not in edge_lengths:
                edge_lengths[e] = length
                graph[p].append(q)
                graph[q].append(p)

    # Find a simple cycle. The problem guarantees at most one closed figure.
    cycle = None
    visited_edges = set()

    def dfs(start, current, parent, path, path_set):
        nonlocal cycle
        if cycle is not None:
            return

        for nxt in graph.get(current, []):
            edge = tuple(sorted((current, nxt)))
            if nxt == parent:
                continue
            if nxt == start and len(path) >= 3:
                cycle = path[:]
                return
            if nxt in path_set:
                continue
            dfs(start, nxt, current, path + [nxt], path_set | {nxt})
            if cycle is not None:
                return

    for vertex in graph:
        dfs(vertex, vertex, None, [vertex], {vertex})
        if cycle is not None:
            break

    if cycle is None:
        print("Abandoned")
        return

    # Compute the chosen closed figure's perimeter from its consecutive edges.
    perimeter = 0.0
    for i in range(len(cycle)):
        p = cycle[i]
        q = cycle[(i + 1) % len(cycle)]
        perimeter += edge_lengths.get(tuple(sorted((p, q))), distance(p, q))

    player_area = polygon_area(cycle)
    remaining_length = max(0.0, total_length - perimeter)
    computer_area = (remaining_length / 4.0) ** 2

    if player_area + 1e-7 >= computer_area:
        print("Kalyan")
    else:
        print("Computer")


if __name__ == "__main__":
    main()
