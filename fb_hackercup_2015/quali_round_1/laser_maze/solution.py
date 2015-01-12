import heapq

filename = 'in'

START = 'S'
GOAL = 'G'
WALL = '#'

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

T_UP = '^'
T_DOWN = 'v'
T_LEFT = '<'
T_RIGHT = '>'

def replace_char(original, index, new_char):
    return original[:index] + new_char + original[index+1:]

class Step(object):
    def __init__(self, maze, step_number):
        self.maze = maze
        self.step_number = step_number

        x = maze.position[0]
        y = maze.position[1]
        goal_x = maze.goal[0]
        goal_y = maze.goal[1] 
        v_distance = goal_x - x
        h_distance = goal_y - y
        self.distance_to_goal = v_distance^2 + h_distance^2

    def __lt__(self, other):
        if self.distance_to_goal == other.distance_to_goal:
            return self.step_number < other.step_number
        else:
            return self.distance_to_goal < other.step_number

    def __repr__(self):
        return "Step: %s\n%s" % (self.step_number, self.maze)


class SetOfMazes(object):
    def __init__(self):
        self.steps = set()

    def add(self, maze):
        encoded = repr(maze)
        self.steps.add(encoded)

    def __contains__(self, maze):
        encoded = repr(maze)
        # print(len(self.steps))
        return encoded in self.steps


class Maze(object):

    def __init__(self, maze, m, n, copy_from=None):
        # copies the maze representation
        self.maze = list(maze)
        self.n = n
        self.m = m

        if copy_from is None:
            self.start = self.find(START)
            self.goal = self.find(GOAL)

            self.turrets = []
            for i, line in enumerate(self.maze):
                for j, block in enumerate(line):
                    if block == T_UP or block == T_DOWN or block == T_LEFT or block == T_RIGHT:
                        self.turrets.append((i, j))

        else:
            self.start = copy_from.start
            self.goal = copy_from.goal
            self.turrets = copy_from.turrets

        self.position = self.start

    def __repr__(self):
        txt = ''
        for i, line in enumerate(self.maze):
            for j, block in enumerate(line):
                if (i, j) == self.position:
                    txt += 'x'
                else:    
                    txt += block
            txt += '\n'
        return txt

    def find(self, block_type):
        for i, line in enumerate(self.maze):
            for j, block in enumerate(line):
                if block == block_type:
                    return (i, j)
        return None

    def is_free_block(self, block):
        x = block[0]
        y = block[1]

        return (self.maze[x][y] != WALL 
                and self.maze[x][y] != T_UP
                and self.maze[x][y] != T_DOWN
                and self.maze[x][y] != T_LEFT
                and self.maze[x][y] != T_RIGHT)

    def reached_goal(self):
        x = self.position[0]
        y = self.position[1]
        return self.maze[x][y] == GOAL

    def is_laser_free(self, block):
        # if next step in block will be laser free
        x = block[0]
        y = block[1]
        for t_x, t_y in self.turrets:
            turret = self.maze[t_x][t_y]
            if turret == T_UP and x == t_x and y > t_y:
                return False
            if turret == T_DOWN and x == t_x and y < t_y:
                return False
            if turret == T_LEFT and x < t_x and y == t_y:
                return False    
            if turret == T_RIGHT and x > t_x and y == t_y:
                return False 
        return True

    def _can_walk(self, direction):
        x = self.position[0]
        y = self.position[1]
            
        if direction == UP:
            return x > 0 and self.is_free_block((x-1,y)) and self.is_laser_free((x-1, y))
        if direction == DOWN:
            return x < self.m - 1 and self.is_free_block((x+1, y)) and self.is_laser_free((x+1, y))
        if direction == LEFT:
            return y > 0 and self.is_free_block((x, y-1)) and self.is_laser_free((x, y-1))
        if direction == RIGHT:
            return y < self.n - 1 and self.is_free_block((x, y+1)) and self.is_laser_free((x, y+1))

    def _update_turrets(self):
        for turret in self.turrets:
            i = turret[0]
            j = turret[1]
            block = self.maze[i][j]
            if block == T_UP:
                self.maze[i] = replace_char(self.maze[i], j, T_RIGHT)
            if block == T_RIGHT:
                self.maze[i] = replace_char(self.maze[i], j, T_DOWN)
            if block == T_DOWN:
                self.maze[i] = replace_char(self.maze[i], j, T_LEFT)
            if block == T_LEFT:
                self.maze[i] = replace_char(self.maze[i], j, T_UP)

    def walk(self, direction):
        # returns a new maze with new position and new laser turrets
        new_maze = None
        if self._can_walk(direction):
            new_maze = Maze(self.maze, self.m, self.n, copy_from=self)
            x = self.position[0]
            y = self.position[1]
            if direction == UP:
                new_maze.position = (x-1, y)
            if direction == DOWN:
                new_maze.position = (x+1, y)
            if direction == LEFT:
                new_maze.position = (x, y-1)
            if direction == RIGHT:
                new_maze.position = (x, y+1)

            # update turrets
            new_maze._update_turrets()

        return new_maze


def find_goal(maze):

    steps_heap = [Step(maze, step_number=0)]
    directions = [UP, DOWN, LEFT, RIGHT]

    visited_steps = SetOfMazes()

    while steps_heap:
        current_step = heapq.heappop(steps_heap)
        # print(steps_heap)
        # print(current_step)
        # input()

        visited_steps.add(current_step.maze)

        if current_step.maze.reached_goal():
            return current_step.step_number

        for direction in directions:
            new_maze = current_step.maze.walk(direction)
            if new_maze:
                if new_maze in visited_steps:
                    pass
                    # print("Been there, done that.")
                else:
                    step = Step(new_maze, current_step.step_number + 1)
                    heapq.heappush(steps_heap, step)

    return None
        
def solve():
    with open(filename) as input_file:
        t = int(input_file.readline().strip())
        for i in range(1, t + 1):

            maze = []
            m, n = tuple(map(int, input_file.readline().strip().split()))

            for _ in range(m):
                line = input_file.readline().strip()
                maze.append(line)

            maze = Maze(maze, m, n)

            answer = find_goal(maze)
            print("Case #%s: %s" % (i, answer if answer else 'impossible'))
            # input()

solve()