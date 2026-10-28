def main():
    n = int(input().strip())

    horizontal = {}  # y -> list of [xmin, xmax]
    vertical = {}    # x -> list of [ymin, ymax]

    for _ in range(n):
        x1, y1, x2, y2 = map(int, input().split())

        if y1 == y2:
            left, right = sorted((x1, x2))
            horizontal.setdefault(y1, []).append((left, right))
        elif x1 == x2:
            bottom, top = sorted((y1, y2))
            vertical.setdefault(x1, []).append((bottom, top))

    def covered(segments, a, b):
        # Check whether the union of segments covers the complete interval [a, b].
        intervals = sorted(segments)
        current = a

        for left, right in intervals:
            if right < current:
                continue
            if left > current:
                return False
            current = max(current, right)
            if current >= b:
                return True

        return current >= b

    xs = sorted(vertical)
    ys = sorted(horizontal)
    rectangles = 0

    # Choose two vertical and two horizontal lines. All four sides must be
    # continuously present between the chosen corner coordinates.
    for i in range(len(xs)):
        for j in range(i + 1, len(xs)):
            left_x, right_x = xs[i], xs[j]

            common_ys = []
            for y in ys:
                if covered(horizontal[y], left_x, right_x):
                    if covered(vertical.get(left_x, []), y, y) and covered(
                        vertical.get(right_x, []), y, y
                    ):
                        common_ys.append(y)

            for a in range(len(common_ys)):
                for b in range(a + 1, len(common_ys)):
                    y_bottom, y_top = common_ys[a], common_ys[b]
                    if (covered(vertical.get(left_x, []), y_bottom, y_top)
                            and covered(vertical.get(right_x, []), y_bottom, y_top)
                            and covered(horizontal.get(y_bottom, []), left_x, right_x)
                            and covered(horizontal.get(y_top, []), left_x, right_x)):
                        rectangles += 1

    print(rectangles)


if __name__ == "__main__":
    main()
