def distance(w1, w2):
    return w1.pos - w2.pos


def sign(x):
    return -1 if x < 0 else 0 if x == 0 else 1


def collide_rect(rect1, rect2) -> (bool, bool):
    return (
        (
            rect1.left < rect2.right
            and
            rect1.right > rect2.left
        ),
        (
            rect1.top < rect2.bottom
            and
            rect1.bottom > rect2.top
        )
    )

