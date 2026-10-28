def polygon_area(points):
    area2 = 0
    n = len(points)
    for i in range(n):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % n]
        area2 += x1 * y2 - x2 * y1
    return abs(area2) / 2.0


n = int(input().strip())
points = [tuple(map(int, input().split())) for _ in range(n)]

# Determine polygon orientation: positive signed area means counter-clockwise.
signed_area2 = 0
for i in range(n):
    x1, y1 = points[i]
    x2, y2 = points[(i + 1) % n]
    signed_area2 += x1 * y2 - x2 * y1
counter_clockwise = signed_area2 > 0

# Each edge is shifted inward by H. For a horizontal edge, store its
# shifted y-coordinate direction; for a vertical edge, store its x direction.
edges = []
max_tenths = 10**9

for i in range(n):
    x1, y1 = points[i]
    x2, y2 = points[(i + 1) % n]

    length = abs(x2 - x1) + abs(y2 - y1)
    max_tenths = min(max_tenths, int((length - 0.1 + 1e-9) * 5))

    if y1 == y2:  # Horizontal edge
        inward_sign = (1 if counter_clockwise else -1)
        if x2 < x1:
            inward_sign *= -1
        edges.append(('H', y1, inward_sign))
    else:  # Vertical edge
        inward_sign = (-1 if counter_clockwise else 1)
        if y2 < y1:
            inward_sign *= -1
        edges.append(('V', x1, inward_sign))

best_volume = 0.0

# H must be a multiple of 0.1. Check every valid height.
for tenths in range(1, max_tenths + 1):
    h = tenths / 10.0
    inset_points = []

    for i in range(n):
        previous_edge = edges[(i - 1) % n]
        current_edge = edges[i]

        if previous_edge[0] == 'H' and current_edge[0] == 'V':
            x = current_edge[1] + current_edge[2] * h
            y = previous_edge[1] + previous_edge[2] * h
        elif previous_edge[0] == 'V' and current_edge[0] == 'H':
            x = previous_edge[1] + previous_edge[2] * h
            y = current_edge[1] + current_edge[2] * h
        else:
            # A rectilinear polygon alternates horizontal and vertical edges.
            continue

        inset_points.append((x, y))

    if len(inset_points) != n:
        continue

    area = polygon_area(inset_points)
    volume = area * h
    if volume > best_volume:
        best_volume = volume

print(f"{best_volume:.2f}")
