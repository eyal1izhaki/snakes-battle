# snakes-battle

Every player in the competition creates his version of of the ai-snake class.
The players need to implement the 'change_direction' function so their snake will be 'smart' enough to survive and win.



Some important functions and methods to know:
  1. Boad.add_snake() method obviously adds a snake to the board. We will not see the snake on the screen until we call the graphics.update_screen() function.
  2. Same as Boad.add_fruit()
  3. AISnake.change_direction(). This method is the method that the players in the competiton are implementing.
  4. Snake.move_one_cell() as it sounds. Again, we will see the change on the screen only when calling the update_screen function.
  5. rules.apply_rules(). This function is responsible for applying rules like find an empty cell for a new fruit or check if a snake hitted other snakes.
  

