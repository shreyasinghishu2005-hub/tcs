n = int(input().strip())

rectangles = []
for _ in range(n):
    x1, y1, x2, y2 = map(int, input().split())
    rectangles.append((x1, y1, x2, y2))

paper_x1, paper_y1, paper_x2, paper_y2 = map(int, input().split())

# A vertical fold is allowed only at an integer x-coordinate that is
# not strictly inside the horizontal span of any colored rectangle.
valid_x = [
    x for x in range(paper_x1, paper_x2 + 1)
    if all(not (x1 < x < x2) for x1, y1, x2, y2 in rectangles)
]

# A horizontal fold is allowed only at an integer y-coordinate that is
# not strictly inside the vertical span of any colored rectangle.
valid_y = [
    y for y in range(paper_y1, paper_y2 + 1)
    if all(not (y1 < y < y2) for x1, y1, x2, y2 in rectangles)
]

min_width = min(valid_x[i + 1] - valid_x[i] for i in range(len(valid_x) - 1))
min_height = min(valid_y[i + 1] - valid_y[i] for i in range(len(valid_y) - 1))

print(min_width * min_height)
