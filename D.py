def on_segment(x, y, slide):
    x1, y1, x2, y2 = slide
    return (
        min(x1, x2) <= x <= max(x1, x2)
        and min(y1, y2) <= y <= max(y1, y2)
        and abs(x - x1) == abs(y - y1)
    )


def main():
    n = int(input().strip())
    slides = [tuple(map(int, input().split())) for _ in range(n)]
    x, y, energy = map(int, input().split())

    # Avoid repeatedly paying the unlock cost at the same touching point.
    unlocked_points = set()
    seen_states = set()

    while y > 0:
        state = (x, y, energy)
        if state in seen_states:
            break
        seen_states.add(state)

        # Gravity: fall vertically to the highest slide directly below.
        landing_y = 0
        for slide in slides:
            x1, y1, x2, y2 = slide
            if min(x1, x2) <= x <= max(x1, x2):
                sy = y1 + (x - x1) * (y2 - y1) // (x2 - x1) if x2 != x1 else None
                if sy is not None and sy < y and sy > landing_y:
                    landing_y = sy

        y = landing_y
        if y == 0:
            break

        while True:
            # Find slides containing the current position.
            touching = [i for i, s in enumerate(slides) if on_segment(x, y, s)]
            if not touching:
                break

            # At a shared point the ball is stuck between slides and must unlock.
            if len(touching) >= 2 and (x, y) not in unlocked_points:
                cost = x * y
                if energy < cost:
                    print(x, y)
                    return
                energy -= cost
                unlocked_points.add((x, y))

            # Select the unique downhill slide direction available at this point.
            options = []
            for idx in touching:
                x1, y1, x2, y2 = slides[idx]
                if y1 < y2:
                    low_x, low_y = x1, y1
                elif y2 < y1:
                    low_x, low_y = x2, y2
                else:
                    continue

                dx = 0 if low_x == x else (1 if low_x > x else -1)
                dy = -1
                # Only move downhill along this slide if the current point is
                # on the path to its lower endpoint.
                if (low_x - x) * dx >= 0:
                    options.append((idx, dx, dy, low_x, low_y))

            if not options:
                break

            # Inputs guarantee a unique possible direction; use the first valid one.
            _, dx, dy, low_x, low_y = options[0]

            moved = False
            while (x, y) != (low_x, low_y):
                if energy <= 0:
                    print(x, y)
                    return

                nx, ny = x + dx, y - 1

                # Stop at an intersection/touching point with another slide.
                if any(on_segment(nx, ny, s) for j, s in enumerate(slides)
                       if not (j == options[0][0] and (nx, ny) != (low_x, low_y))):
                    # Continue onto a slide only if this is the endpoint or
                    # an intersection; the next outer iteration handles it.
                    x, y = nx, ny
                    energy -= 1
                    moved = True
                    break

                x, y = nx, ny
                energy -= 1
                moved = True

            if energy < 0:
                energy = 0

            if y == 0:
                print(x, y)
                return

            # If energy ran out mid-slide, the ball stops at its current point.
            if energy == 0 and (x, y) != (low_x, low_y):
                print(x, y)
                return

            if not moved or (x, y) == (low_x, low_y):
                break

        # If no slide movement was possible, gravity resumes from here.
        if y == 0:
            break

    print(x, y)


if __name__ == "__main__":
    main()
