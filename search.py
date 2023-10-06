from collections import deque
import time
import resource

class Search:

    def __init__(self):
        self.directions = {'U': -4, 'D': 4, 'L': -1, 'R': 1}
        self.move_names = {'U': 'Up', 'D': 'Down', 'L': 'Left', 'R': 'Right'}

    def goal_test(self, cur_tiles):
        return cur_tiles == ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '0']

    def get_neighbors(self, state):
        # Generate neighboring states based on valid moves
        neighbors = []
        empty_index = state.index('0')
        for direction, offset in self.directions.items():
            # Check if the move is valid within the puzzle grid
            if (
                0 <= empty_index + offset < 16
                and (empty_index % 4 != 3 or direction != 'R')
                and (empty_index % 4 != 0 or direction != 'L')
            ):
                neighbor = state[:]
                # Swap the empty tile with the neighboring tile
                neighbor[empty_index], neighbor[empty_index + offset] = neighbor[empty_index + offset], neighbor[empty_index]
                neighbors.append((neighbor, direction))
        return neighbors

    def bfs(self, initial_state):
        # Initialize BFS search
        start_time = time.time()
        queue = deque([(initial_state, [])])  # Initialize the queue with the initial state and an empty path
        explored = set()  # Keep track of explored states to avoid revisiting
        max_memory = 0

        while queue:
            cur_state, path = queue.popleft()  # Dequeue the state from the front of the queue
            if self.goal_test(cur_state):
                # If the goal state is reached, calculate and return results
                end_time = time.time()
                memory_used = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0
                max_memory = max(max_memory, memory_used)
                return ''.join(path), len(explored), round(end_time - start_time, 3), round(max_memory, 3)

            if tuple(cur_state) not in explored:
                # If the state hasn't been explored, mark it as explored
                explored.add(tuple(cur_state))
                neighbors = self.get_neighbors(cur_state)
                for neighbor_state, move in neighbors:
                    # Add neighboring states to the queue with an updated path
                    queue.append((neighbor_state, path + [move]))

        return None, 0, 0.0, 0.0

    def solve(self, input):
        initial_list = input.split(" ")  # Parse the input string into a list
        solution_moves, num_expanded, time_taken, memory_used = self.bfs(initial_list)
        if solution_moves is not None:
            # Print results if a solution is found
            print("Moves: ", solution_moves)
            print("Number of Nodes expanded:", num_expanded)
            print("Time Taken:", time_taken)
            print("Memory Used:", memory_used, "kb")
        return solution_moves

if __name__ == '__main__':
    initial_board = "1 0 2 4 5 7 3 8 9 6 11 12 13 10 14 15"
    agent = Search()
    agent.solve(initial_board)
