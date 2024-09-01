## Assignment Objectives

In this assignment we will:

* Implement a hash table
* Create a game tree to implement game playing bots
* Extend the features of the game using data structures you learned

NOTE: **as this assignment is about implementing data structures, you are not allowed to make use of any Python libraries or use built-in python data structures and functions unless specified.  If you are not sure, please ask.  Any use a built-in libraries or functions without approval will result in having to redo the assignment with a grade penalty of -50%**

## Part A - Hash Tables 


In this part of the assignment you will implement a class called HashTable which implements a hash table.  

When doing this portion of the assignment you can use:

* python list for the main table (but NOT the chains if you are doing chaining)
* python hash() function - don't write your own
* Your linked list from part A (if you wish to create a chaining hash table)

You may use either chaining or linear probing as your collision resolution method.  The exact method and details of implementation (such as using tombstones or not if you choose linear probing) is up to you.


### Member functions


---

```python
	def __init__(self, capacity=32):
```
The initializer for the table defaults the initial table capacity to 32.  It creates a list with capacity elements all initialized to None.

---


```python
	def insert(self, key, value):
```
This function adds a new key-value pair into the table. If a record with matching key already exists in the table, the function does not add the new key-value pair and returns False. Otherwise, function adds the new key-value pair into the table and returns True.  When an insertion causes the HashTable's load factor to exceed 0.7, the list used to store the table must be resized.  Resizing must still allow every existing record to be found.



---

```python
	def modify(self, key, value):
```
This function modifies an existing key-value pair into the table. If no record with matching key exists in the table, the function does nothing and returns False. Otherwise, function changes the existing value into the one passed into the function and returns True

---

```python
	def remove(self, key):
```

This function removes the key-value pair with the matching key.  If no record with matching key exists in the table, the function does nothing and returns False.  Otherwise, record with matching key is removed and returns True

---

```python
	def search(self, key):
```

This function returns the value of the record with the matching key.  If no reocrd with matching key exists in the table, function returns None

---

```python
	def capacity(self):
```
This function returns the number of spots in the table.  This consists of spots available in the table.  

---

```python
	def __len__(self):
```

This function returns the number of Records stored in the table.

---


## Part B - A Game tree based bot  


In this part of the assignment you will implement a bot that will play a simple board game by performing look-ahead's using a game treee.

For this part of the assignment you will need to do the following:

* Write an Evaluation Function.
* Create a Game tree

### The rules of the game.

This game is a 2D board game.  Initially player 1 has a gem in the top left corner and player 2 has a gem in the bottom right corner. Players take turns adding one gem per turn to the board.  A gem can be added to any empty square or any square where the player has at least one gem.  If the number of gems in a square reaches the number of neighbours for the cell, the gems overflow into its neighbours, increasing the number of gems and changing the colour of gems to that player's colour (follows the rules of the overflow() function from assignment 1.)

The game ends if every single gem on the board is the same colour.  The player represented by that colour is the winner of the game.

Your repo includes an implementation of the game.  You will need to run this locally as codespaces won't properly support pygames.

To run the game use the command:

```
python game.py
```

Note that the current AI player is just a stub.  It doesn't even check if the move it is making is valid.  The first player always places a piece into top left corner.  The second player always puts a piece in the bottom right corner.  It is up to you to implement an actual AI bot for the game.

If the AI player makes an invalid move, the game will end and the other player will automatically win the game. 



### Write an Evaluation Function

```python
def evaluate_board(board, player)
```

* **board** - The board is a 2D grid with numbers.
	- 0 indicates that the cell is empty
	- the absolute value of a non-zero number indicates the number pieces in the corresponding cell
	- the sign indicates which player's pieces are in the cell.  Positive numbers are player 1.  Negative numbers are player 2
* **player** - This number is either +1 or -1.  A +1 means we are evaluating the board for player 1.  A -1 indicates the function is evaluating the board for player 2.

Given a board and the player you are evaluating the board for, this function returns a score for the board.  Ensure that the score for a winning board is higher than any estimate for a non-winning board.  Also ensure that a score for a losing board is lower than any non-losing board.  Non-winning is just any board that isn't in a winning state for the player.  It does not mean the player has lost.. just hasn't won.  Similarly a non-losing board is just a board in a state where player hasn't lost.  The exact algorithm for this is entirely up to you as long as it follows the rule for scoring non-winning/non-losing boards.

### Implement a Game Tree

A game tree is a data structure that allows you to search through a series of possible next moves players can make in a game.  This data structure allows you to consider not only what you can do but what your opponent can do based on what you did, then you can choose what to do based on what your opponent did and so on...


For games with a small number of possible states, it is possible to generate all possible moves to a terminal state.  That is a state where the game has ended because someone has won or a the game has reached some sort of tied state where no one else can make any more moves.

For example, this is possible in a game like tic-tac-toe as there are less than 9! = 362880 nodes in a game tree starting from an empty board.  Thus tic-tac toe is considered to be solved.. the computer can always play to a tie game if the opponent makes no mistakes

For games that have more possible states, where it is not possible to generate all moves to a terminal state, game trees are typically created to a certain height.  The boards at the leafs are evaluated using an evaluation function that tries to estimate a score for a given board.  A minimax function is then applied to the tree in order to find the best move


### Game Tree

#### Nodes

A game tree node has a set of pointers its children node. represents what moves it can make. This Node class must be internal to your GameTree Class

```python
__init__(board,depth, player, tree_height = 4)
```
When a node is instantiated, it is passed 
* a 2D array representing the board for the node, 
* the depth of this node
* the height of the game tree
* the player (1 or -1) the tree is being created for.  
This function initializes the node.


***

#### GameTree Class

```python
__init__(board, player, tree_height = 4)
```

This function initializes the GameTree Object.  It is passed:

* board - the 2D array representing the board of the game in its current state
* tree_height - the maximum height of the tree to be generated
* player - the player the tree is being created for


The init function will build the game tree to a height of tree_height

In the construction of the game tree, you will create children for each node representing the placement of a piece.  Depending on the level of the node, the player placing the piece will be different.  The root represents the board in the current state, all nodes at level 1 (root's children) represent the placement of the player's piece to the original board. After placing the piece and performing the overflow routine as needed, you will get a new board for each placed piece.  that new board form the boards for the nodes of level 1.  After the player makes a move, the opponent makes a move. Thus, each node in level 2 is formed by the opponent placing a piece onto the board in its parent node.  At level 3, we go back to the player's move and so on.

##### Scoring each node

Your tree will have leaf's due to various conditions:
	a) the board for the node is in a terminal state (someone has won)
	b) the node has reached its maximum depth (tree_height-1).  

For any leaf node, the board is evaluated using the evaluation function.

For any inner node, the minimax algorithm determines the score for the node.

minimax is based on the following:

* You want the best possible board for yourself
* Your opponent wants the worst for you

Thus, if you are making a move, you want the best possible move you can make.  However, if your opponent is making a choice on what move to make, they will want the worst possible move for you.

To score an inner node, choose the best or worst score in the children nodes depending on who is making the move. A node at an even level is scored as the max of the children's scores while the node at an odd level is scored as the min of the children's scores.

Since you need to score nodes based result's of children, it is necessary to score the nodes in a depth first manner (ie you can't find the score of a node unless you know the scores of all the children)

You can either create the entire tree, then perform a depth first traversal to score each node, or you can score the nodes as you create the tree.  The choice is yours

***

```python
def get_move(self)
```
This function gets (row,col) which is the position of the choice from the tree.

***

```python
def clear_tree(self)
```
This function destroys the game tree by unlinking all nodes in order to allow the garbage collector to work on clearing the memory.




#### Ways to make your bots better

NOTE.  Your grade is not based on how good your bots perform!!  Even if they are terrible at the game you can still get top marks.  They simply need to implement a game tree and evaluation function to spec.  See rubric on grading.

- a good evaluation that scores boards accurately is useful
- a fast evaluation function is useful (you can create taller trees if your function is faster)
- with game trees, the key to making better game trees is actually to have taller game trees.  A taller game tree is better than a good evaluation function.  One way to create taller trees is to prune.  If you are interested in this, check out the idea of alpha-beta prunning

## Part C: Game Improvements 

This part of the assignment is open ended.  There are different features that you can add to make this game better.  Exactly what you implement is up to you!  The only rule is the basic game must remain the same.  Note, the feature added needs to be coding based.. so changing out the artwork for something that looks better is not considered a valid extra feature.  Here are some suggestions to get you started.. but you are free to use your imagination to add more.

* Create an "undo" last move button for any human players (AI bots shouldn't be allowed to undo) as long as they haven't lost.  This undo reverts the game to a state before that human player's last move.
* Add Animations... the gems currently just "appear" when they overflow.. you can animate the movement
* Add UI elements to increase/decrease the smartness of the bots (the taller the game tree the smarter the bot)


**This is only a very very limited set of ideas.  You are free to be creative and add others**

If you need a Stack, Dequeue, Queue, HashTable, LinkedList to implement your idea, you must make use of the data structure you wrote earlier in the class.  If you need other data structures, you can use the built in python ones for this part of the assignment.

This part of the assignment has no testers as we don't know what you will implement.  Thus, aside from pushing an updated version of game.py to the repo, you will need to also provide the following:

* A video with voice over the video must:
	1. demonstrate the feature(s) you added
	2. explain how you implemented the features
	3. especially speak to the data structures you used and how they helped in the implementation.
	4. This video should be around 2 to 3 minutes.  Any video over 5 minutes long will receive a reduced grade.  Be succint in your explanation.

* Submit the video using Seneca's one-drive and share it so that anyone with link can view the video.  Make sure that the access is properly given as an inability to view the video can result in a reduced grade
* Alternative you can can put it on youtube as an unlisted video and submit the link for that.


See rubric for grading

