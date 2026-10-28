m, n = map(int, input().split())

box = []
for _ in range(m):
    box.append(input().split())

k = int(input())
directions = [input().strip().lower() for _ in range(k)]

for direction in directions:
    if direction == "right":
        # Rotate 90 degrees clockwise
        box = [list(row) for row in zip(*box[::-1])]
    else:
        # Rotate 90 degrees anticlockwise
        box = [list(row) for row in zip(*box)][::-1]

    # Apply gravity: stones fall to the bottom of each column
    rows = len(box)
    cols = len(box[0])

    for j in range(cols):
        stones = sum(1 for i in range(rows) if box[i][j] == '*')

        for i in range(rows):
            box[i][j] = '.'

        for i in range(rows - stones, rows):
            box[i][j] = '*'

for row in box:
    print(*row)
