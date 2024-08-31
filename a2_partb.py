# Main Author: Jagbir Singh
# Main Reviewer: Arad Fadaei

from a1_partd import overflow
from a1_partc import Queue

# This function duplicates and returns the board. You may find this useful
def copy_board(board):
        current_board = []
        height = len(board)
        for i in range(height):
            current_board.append(board[i].copy())
        return current_board


# this function is your evaluation function for the board
# returns higher score if player is winning
def evaluate_board (board, player):
    overflow_board = [ # Corners are eliminated from overflow table
                      [2,2,2,2,2,2],
                      [2,3,3,3,3,2],
                      [2,3,3,3,3,2],
                      [2,3,3,3,3,2],
                      [2,2,2,2,3,2]]
    score = 0
    if all(cell >= 0 for row in board for cell in row):
        return player*float('inf') #returns +infinity if player wins 
    elif all(cell <= 0 for row in board for cell in row):
        return -player*float('inf') #returns -infinity if player losses
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col]*player < 0: # plenty if opponent have gems
                score -= 10
            elif board[row][col]*player != 0 and board[row][col]*player <= overflow_board[row][col]: # points for having gems
                score += 10
                if board[row][col]*player == overflow_board[row][col]: # algo should avoid going close to overflow if possible
                    score -= 3
    return score

class GameTree:
    class Node:
        def __init__(self, board, depth, player, tree_height = 4):
            self.board = board
            self.depth = depth
            self.player = player
            self.children = []
            self.cord = []
            self.score = 0
        

    def __init__(self, board, player, tree_height = 4):
        self.player = player
        self.board = copy_board(board)
        self.root = self._build_tree(self.board, player, 0, tree_height)
        # you will need to implement the creation of the game tree here.  After this function completes,
        # a full game tree will be created.
        # hint: as with many tree structures, you will need to define a self.root that points to the root
        # of the game tree.  To create the tree itself, a recursive function will likely be the easiest as you will
        # need to apply the minimax algorithm to its creation.

    def _build_tree(self, board, player, depth, max_depth):
        node = self.Node(board, depth, player)
        if depth == max_depth or self._is_terminal(board):
            node.score = evaluate_board(board, player)
            return node
            
        q = Queue()
        for row in range(len(board)):
            for col in range(len(board[0])):
                if board[row][col] == 0 or board[row][col]/abs(board[row][col]) == player:
                    new_board = copy_board(board)
                    new_board[row][col] += player
                    overflow(new_board, q)
                    child_node = self._build_tree(new_board, -player, depth + 1, max_depth)
                    child_node.cord = [row, col]
                    node.children.append(child_node)

        # Minimax scoring
        node.score = -min(child.score for child in node.children)

        return node
    
    def _is_terminal(self, board):
        # Check if the game has ended (all gems same color)
        return all(cell >= 0 for row in board for cell in row) or all(cell <= 0 for row in board for cell in row)

    # this function is a pure stub.  It is here to ensure the game runs.  Once you complete
    # the GameTree, you will use it to determine what to return.
    def get_move(self):
        best_move_node = min(self.root.children, key=lambda child: child.score)
        cord = best_move_node.cord
        self.clear_tree()
        return cord

    def clear_tree(self):
        if self.root:  # Check if tree exists
            self.clear_node(self.root)
            self.root = None

    def clear_node(self, node):
        for child in node.children:
            self.clear_node(child)  # Recursive call to clear children
        del node  # Delete the node after children are cleared

    
