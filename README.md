# PongClub

The Pong Club is a Pong Game in which you can play against an AI.



## Usage

The ```main.py``` file contains every parameter to play the game:

* ```action``` defines what the game will do once launched. It can be set to three parameters:
  * ```TRAINING``` the game will train the AI
  * ```PLAYING``` you will play the game alone
  * ```AGAINST_BEST``` you will play against an AI

To launch the game, simply launch the ```Main.py``` python file:

```python
python3 Main.py
```



### Training

Once launched, the game will simply train the AI and output the state.

The the *AI* section below for more informations.



### Playing

This option's main purpose is to debug the game.

For now, the game only supports one player. The ```NUMBER_OF_AI ``` parameter in the main file can be set from 0 to 2. 0 means you will play as the two players. If it is set to 1, you will play against one not trained AI. If set to 2, two not trained AI will play against each other.



### Against Best

The ```play_against``` parameter in the main file defines the generation against which you wish to play. The AI must be trained to that generation and the *Population* object must be serialized in the ```populations``` folder. The name of the file must be as follow:

```
populations/NUM_OF_GEN.pop
```

The game will select the best player of that generation and then you will play against that player. It may take some time to select the best player. The progression will be printed.



### Dependencies

* Python 3
* PyTorch
* PyGame
* Numpy



## The AI

The AI uses an hybrid of genetic algorithm and Neural Network. First, the neural network is randomly set. Then, a certain amount of AI Players (set by the parameter ```POPULATION_SIZE``` in the ```train.py``` file) will play against each other in randoms 1vs1 matches. Each player plays against one adversary randomly chosen. The winner is kept identical for the next generation (to prevent a generation to be worst than the previous one) while the looser is replaced by a mutated version of the winner. Once each player has played his match, the next generation replaced the old one.

To determine the action of each ai player, a neural network is used. It takes 6 inputs in this order:

* the player's vertical position
* the enemy's vertical position
* the ball's horizontal position
* the ball's vertical position
* the ball's horizontal velocity
* the ball's vertical velocity

and has 2 outputs determining whether the player must go up or down.



## Author

This game has been made by

* [Lorenzo Sonnino](https://github.com/lsonnino)

And is under license. Please, see the ```LICENSE``` file for more informations.

