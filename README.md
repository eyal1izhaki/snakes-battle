# snakes-battle

Every player in the competition creates an AI snake.
The players need to implement the 'make_decision' function so their snake will be 'smart' enough to survive and win.

Every frame, the method make_decision is being called so every snake will have to choose where it should go in order to win.

Some information about the game:

Logic:
1. When a snake hits itself it loses.
2. When a snake hits a border it loses.
3. When a snake hits other snake it loses.
4. When snakes collide head to head, they both lose, unless one of the is a king, it will survive the collision.
5. The winner is the snake with the highest score when the time is over or when there are no more snakes in the board.

Fruits:
1. 'Strawberry' - makes the snake one unit longer.
2. 'Dragon Fruit' - makes the snake two units longer.
3. 'Bomb' - shrinks the snake in 2 units.
4. 'Shield' -  protects the snake from getting hurt when eating a bomb. Snake with a shield can cross itself without cutting its body. Snake with a shield won't get hurt by Skull. The shield protects the snake only once.
5. 'Skull' -  kills the snake that eats it unless the snake is shielded.
6. 'King' - Snake moves and makes decision X2 from the other snakes. Every fruit snake eats, increases the snake in two units (even skull).
7. 'knife' - gives the snake the power to cut other snakes. This power is limited for cutting only one snake.


You can press + or - keys to adjust the delay between frames.