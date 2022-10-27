# snakes-battle

Every player in the competition creates an AI snake.
The players need to implement the 'make_decision' function so their snake will be 'smart' enough to survive and win.

Every frame, the method make_decision is being called so every snake will have to choose where it should go in order to win.

Some information about the game:

Logic:
1. When a snake hits itself is cuts itself in the hitting point.

Fruits:
1. 'Strawberry' - makes the snake one unit longer.
2. 'Dragon Fruit' - makes the snake two units longer.
3. 'Bomb' - shrinks the snake in 2 units.
4. 'Shield' -  protects the snake from getting hurt when eating a bomb. Snake with a shield can cross itself without cutting its body. Snake with a shield won't get hurt by Skull. The shield protects the snake only once.
5. 'Skull' -  kills the snake that eats it unless the snake is shielded.
6. 'King' - Snake moves and makes decision X2 from the other snakes
7. 'knife' - gives the snake the power to cut other snakes. This power is limited for cutting only one snake.


You can press + or - keys to adjust the delay between frames.