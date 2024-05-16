import random
from typing import List, Dict, Optional
from box import Box

def get_line_boxes(matrix: List[List[Box]], line: List[tuple[int, int]]) -> List[Box]:
    p1, p2 = line
    boxes = []
    if p1[0] == p2[0]:  # horizontal line
        y_min = min(p1[1], p2[1])
        if p1[0] > 0:
            boxes.append(matrix[p1[0] - 1][y_min])
        if p1[0] < len(matrix) - 1:
            boxes.append(matrix[p1[0]][y_min])
    else:  # vertical line
        x_min = min(p1[0], p2[0])
        if p1[1] > 0:
            boxes.append(matrix[x_min][p1[1] - 1])
        if p1[1] < len(matrix[0]) - 1:
            boxes.append(matrix[x_min][p1[1]])
    return boxes

def get_adjacent_boxes(matrix: List[List[Box]], box: Box) -> Dict[str, Optional[Box]]:
    adjacent = {'top': None, 'bottom': None, 'left': None, 'right': None}
    x, y = box.idx
    if x > 0:
        adjacent['top'] = matrix[x - 1][y]
    if x < len(matrix) - 1:
        adjacent['bottom'] = matrix[x + 1][y]
    if y > 0:
        adjacent['left'] = matrix[x][y - 1]
    if y < len(matrix[0]) - 1:
        adjacent['right'] = matrix[x][y + 1]
    return adjacent

def count_adjacent_boxes(matrix: List[List[Box]], box: Box) -> int:
    count = 0
    x, y = box.idx
    if x > 0:
        count += 1
    if x < len(matrix) - 1:
        count += 1
    if y > 0:
        count += 1
    if y < len(matrix[0]) - 1:
        count += 1
    return count

def get_random_empty_side(box: Box, exclude: Optional[tuple[int, int]] = None) -> Optional[tuple[int, int]]:
    choices = []
    if box.top is None and (exclude is None or box.top_idx() != exclude):
        choices.append(box.top_idx())
    if box.bottom is None and (exclude is None or box.bottom_idx() != exclude):
        choices.append(box.bottom_idx())
    if box.left is None and (exclude is None or box.left_idx() != exclude):
        choices.append(box.left_idx())
    if box.right is None and (exclude is None or box.right_idx() != exclude):
        choices.append(box.right_idx())
    return random.choice(choices) if choices else None

def get_side_counts(matrix: List[List[Box]], box: Box) -> Dict[str, Optional[int]]:
    sides = {'top': None, 'bottom': None, 'left': None, 'right': None}
    x, y = box.idx
    if x > 0:
        sides['top'] = matrix[x - 1][y].sides
    if x < len(matrix) - 1:
        sides['bottom'] = matrix[x + 1][y].sides
    if y > 0:
        sides['left'] = matrix[x][y - 1].sides
    if y < len(matrix[0]) - 1:
        sides['right'] = matrix[x][y + 1].sides
    return sides

def is_side_less_than(matrix: List[List[Box]], box: Box, side: str, num: int) -> bool:
    sides = get_side_counts(matrix, box)[side]
    return sides is None or sides < num

def is_facing_outside(matrix: List[List[Box]], box: Box) -> bool:
    x, y = box.idx
    return (
        (x == 0 and box.top is None) or
        (x == len(matrix) - 1 and box.bottom is None) or
        (y == 0 and box.left is None) or
        (y == len(matrix[0]) - 1 and box.right is None)
    )

def easy_strategy(matrix: List[List[Box]], prev_line: Optional[List[tuple[int, int]]]) -> Optional[tuple[int, int]]:
    if prev_line:
        for prev_box in get_line_boxes(matrix, prev_line):
            if prev_box.sides == 3:
                return get_random_empty_side(prev_box)

    boxes = Box.ALL_BOXES
    box3 = [box for box in boxes if box.sides == 3]
    if box3:
        return get_random_empty_side(random.choice(box3))

    box0 = [box for box in boxes if box.sides == 0]
    box1 = [box for box in boxes if box.sides == 1]
    box2 = [box for box in boxes if box.sides == 2]

    for box_list in [box0, box1, box2]:
        if box_list:
            return get_random_empty_side(random.choice(box_list))
    return None

def medium_strategy(matrix: List[List[Box]], prev_line: Optional[List[tuple[int, int]]]) -> Optional[tuple[int, int]]:
    if prev_line:
        for prev_box in get_line_boxes(matrix, prev_line):
            if prev_box.sides == 3:
                return get_random_empty_side(prev_box)

    boxes = Box.ALL_BOXES
    box0 = [box for box in boxes if box.sides == 0]
    box1 = [box for box in boxes if box.sides == 1]
    box2 = [box for box in boxes if box.sides == 2]
    box3 = [box for box in boxes if box.sides == 3]

    box_less2 = box0 + box1

    if box3:
        return get_random_empty_side(random.choice(box3))

    sides_to_check = ['top', 'bottom', 'left', 'right']
    choices = []
    for side in sides_to_check:
        choices.extend([
            getattr(box, f"{side}_idx")()
            for box in box_less2 if is_side_less_than(matrix, box, side, 2)
        ])
    
    if choices:
        return random.choice(choices)

    for box_list in [box0, box1, box2]:
        if box_list:
            return get_random_empty_side(random.choice(box_list))
    return None

def hard_strategy(matrix: List[List[Box]], prev_line: Optional[List[tuple[int, int]]]) -> Optional[tuple[int, int]]:
    if prev_line:
        for prev_box in get_line_boxes(matrix, prev_line):
            if prev_box.sides == 3:
                return get_random_empty_side(prev_box)

    boxes = Box.ALL_BOXES
    box0 = [box for box in boxes if box.sides == 0]
    box1 = [box for box in boxes if box.sides == 1]
    box3 = [box for box in boxes if box.sides == 3]

    if box3:
        return get_random_empty_side(random.choice(box3))

    box_less2 = box0 + box1
    sides_to_check = ['top', 'bottom', 'left', 'right']
    choices = []
    for side in sides_to_check:
        choices.extend([
            getattr(box, f"{side}_idx")()
            for box in box_less2 if is_side_less_than(matrix, box, side, 2)
        ])

    if choices:
        return random.choice(choices)

    chains, crosses, checked, options = [], [], [], boxes.copy()
    while len(checked) < len(boxes):
        current = [options.pop(0)]
        if current[0].color or current[0].sides < 2:
            crosses.append(current[0])
            checked.append(current[0])
            continue

        chain = []
        while current:
            for box in current:
                checked.append(box)
                chain.append(box)
                around = get_adjacent_boxes(matrix, box)
                for direction in ['top', 'bottom', 'left', 'right']:
                    if getattr(box, direction) is None and around[direction]:
                        adj_box = around[direction]
                        if adj_box not in chain and adj_box not in current:
                            if adj_box.sides >= 2:
                                current.append(adj_box)
            current = [b for b in current if b not in chain]
        chains.append(chain)

    if chains:
        sorted_chains = sorted(chains, key=len)
        if sorted_chains:
            return get_random_empty_side(random.choice(sorted_chains[0]))

    return get_random_empty_side(random.choice(crosses))

def extreme_strategy(matrix: List[List[Box]], prev_line: Optional[List[tuple[int, int]]]) -> Optional[tuple[int, int]]:
    boxes = Box.ALL_BOXES
    box0 = [box for box in boxes if box.sides == 0]
    box1 = [box for box in boxes if box.sides == 1]
    box3 = [box for box in boxes if box.sides == 3]
    box_less2 = box0 + box1

    sides_to_check = ['
