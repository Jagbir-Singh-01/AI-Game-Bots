# copy over your a1_partd.py file here
#    Main Author(s): Arad Fadaei
#    Main Reviewer(s): Arad Fadaei

from a1_partc import Queue

def get_overflow_list(grid):
    if not grid:
        return None
    
    rows = len(grid)
    cols = len(grid[0])
    of_list = []

    for r in range(rows):
        for c in range(cols):
            if (r == 0 or r == rows - 1):
                if (c == 0 or c == cols - 1):
                    nbrs = 2

                else:
                    nbrs = 3

            else:
                if (c == 0 or c == cols - 1):
                    nbrs = 3

                else:
                    nbrs = 4

            if (abs(grid[r][c]) >= nbrs):
                of_list.append((r, c))

    if of_list:
        return of_list
                
def overflow(grid, a_queue: Queue):
    def helper(_grid, q, count=0):
        is_overflowing, overflow_coords = is_overflowing_grid(_grid)
        if not is_overflowing:
            # Set the original grid to the current grid state
            for i in range(len(grid)):
                for j in range(len(grid[0])):
                    grid[i][j] = _grid[i][j]
            return count
        
        grid_copy = [row[:] for row in _grid]
        
        overflow_coords_neighbours = find_neighbours(overflow_coords, grid_copy)

        for coord in overflow_coords:
            row = coord[0]
            col = coord[1]

            sign = 1 if _grid[row][col] > 0 else -1
            grid_copy[row][col] = 0
            
        for coord in overflow_coords:
            for nr, nc in overflow_coords_neighbours[coord]:
                grid_copy[nr][nc] = (abs(grid_copy[nr][nc]) + 1) * sign

        q.enqueue(grid_copy)
        return helper(grid_copy, q, count + 1)
            
    return helper(grid, a_queue)
        

### HELPER FUNCTIONS ###
def is_overflowing_grid(grid):
    signs = set()
    overflow_coords = get_overflow_list(grid)

    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] != 0:
                signs.add(grid[r][c] > 0)

    return overflow_coords is not None and len(signs) > 1, overflow_coords


def is_within_bounds(coord, grid):
    row, col = coord
    return 0 <= row < len(grid) and 0 <= col < len(grid[0])

def get_neighbours(coord, grid):
    row, col = coord
    
    possible_neighbours = [
        (row-1, col),
        (row+1, col),
        (row, col-1),
        (row, col+1)
    ]
    
    neighbours = [i for i in possible_neighbours if is_within_bounds(i, grid)]
    return neighbours

def find_neighbours(coords, grid):
    neighbours = {}
    for coord in coords:
        neighbours[coord] = get_neighbours(coord, grid)
    return neighbours



