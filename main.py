import heapq

GOAL_STATE = ((1, 2, 3),
              (4, 5, 6),
              (7, 8, 0))

class PuzzleNode:
    def __init__(self, state, parent=None, move=None, g=0, h=0):
        self.state = state
        self.parent = parent
        self.move = move
        self.g = g
        self.h = h
        self.f = g + h

    def __lt__(self, other):
        return self.f < other.f


def print_state(state):
    for row in state:
        print(" ".join(str(x) if x != 0 else "_" for x in row))
    print()


def find_blank(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j


def manhattan_distance(state):
    distance = 0
    for i in range(3):
        for j in range(3):
            value = state[i][j]
            if value != 0:
                goal_x = (value - 1) // 3
                goal_y = (value - 1) % 3
                distance += abs(i - goal_x) + abs(j - goal_y)
    return distance


def generate_successors(state):
    successors = []
    x, y = find_blank(state)

    moves = {
        "Up": (-1, 0),
        "Down": (1, 0),
        "Left": (0, -1),
        "Right": (0, 1)
    }

    for move_name, (dx, dy) in moves.items():
        new_x, new_y = x + dx, y + dy

        if 0 <= new_x < 3 and 0 <= new_y < 3:
            new_state = [list(row) for row in state]

            # Swap blank with target tile
            new_state[x][y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[x][y]

            successors.append((move_name, tuple(tuple(row) for row in new_state)))

    return successors


def reconstruct_path(node):
    path = []
    while node:
        path.append(node)
        node = node.parent
    return path[::-1]


def a_star(start_state):
    start_h = manhattan_distance(start_state)
    start_node = PuzzleNode(start_state, g=0, h=start_h)

    open_list = []
    heapq.heappush(open_list, start_node)

    visited = set()
    best_g = {start_state: 0}

    while open_list:
        current = heapq.heappop(open_list)

        if current.state == GOAL_STATE:
            return reconstruct_path(current)

        visited.add(current.state)

        for move, next_state in generate_successors(current.state):
            new_g = current.g + 1
            new_h = manhattan_distance(next_state)

            if next_state in visited and new_g >= best_g.get(next_state, float('inf')):
                continue

            if new_g < best_g.get(next_state, float('inf')):
                best_g[next_state] = new_g
                child = PuzzleNode(
                    state=next_state,
                    parent=current,
                    move=move,
                    g=new_g,
                    h=new_h
                )
                heapq.heappush(open_list, child)

    return None


# Example start state
start_state = ((1, 2, 3),
               (4, 0, 6),
               (7, 5, 8))

solution = a_star(start_state)

if solution:
    print("Solution Found!\n")
    for step, node in enumerate(solution):
        print(f"Step {step}")
        if node.move:
            print(f"Move: {node.move}")
        else:
            print("Move: Start")
        print(f"g(n) = {node.g}, h(n) = {node.h}, f(n) = {node.f}")
        print_state(node.state)

    print("Total moves (cost):", len(solution) - 1)
else:
    print("No solution found.")
