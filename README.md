# SnakeTerminalPython
Full color snake game with live user input right in the terminal. 7 Lines (optimized, that is why its so small), uses minimal modules, and game rendering is all in pure python. 
# What is needed to run this program
This is a program written in python 3.9.13 . If you have a newer version of python, I doubt things will break but keep it in mind. 
The keyboard functionality requires your device to be compatible with the msvcrt module. I am fairly certain msvcrt only works for WINDOWS operating system
In order for the program to work properly, your terminal should be able to render ANSI escape code. If you do not know if your terminal does render ANSI escape code, simply run the program and if you  see a grey rectangle with red and green dots then the program is running fine.

# Documentation for Version 2
(each of these numbers correspond to the line number)

#1. Gets random integer between randint(a,b) where a and b are inlcuded integers
#2. kbhit() detetcts if any key was pressed. Getch() reads a keypress & returns the resulting character as a byte string
#3. sleep(x) stops the program for x seconds
#4. Declares almost all needed variables of the program in a single line. 
#4cont. dx: change in x(either 0 or 1). dy:change in y(either 0 or 1) 
#4cont. food: list of 2 ints [x,y] which stores location of food like a coordinate
#4cont. snake: a list of lists, and each sublist looks like [x,y] which stores each pixel of the snake
#4cont. definition: number of times a pixel is printed. Since the empty space character ' ' is not a square, setting this definition to 2 lets game look like squares
#4cont. pixel: empty string ' ' with some ANSI escape code inside. Since we use the ' ', the ANSI escape code of setting the background of this character essentially emulates a fully colered in character
#4cont. GameHeight and GameWidth are the integers the set the height and with of the game. 
#5. ANSI escape code to clear screen and set cursor to top left.
#6. Initialize never ending loop
#7. If a key is pressed, then go into the proceeding indented code
#8. Set variable b to the tuple asscociated with the letter that was pressed. This pair of numbers represents the proper (dx,dy) for WASD (up left down right) movement.
#9. If b exists(if the keyboard key pressed was a key in the dictionary), and the current direction (dx,dy) is not the opposite of the inputed direction, then we can move in that direction, so set (dx,dy) = b
#10. Set the new head to the old head updated with the current direction ---> newHead = (oldHeadX + dx,oldHeadY + dy) ---> head = [snake[0][0] + dx, snake[0][1] + dy] 
#11. If the new head is in the snake (if we have collided with ourself), or, our head went out of the boundaries of the game, break out of the loop, (which has nothing after so it ends the game)
#12. Insert the new head into the first element in the snake list.
#13. If the heads coordinates are the same as the foods coordinates (if the snake ate the food), spawn a new one randomnly within the games boundaries
#14. If we haven't eaten the food this frame, delete our tail. (The adding of the new head in the new direction, and deleting of the tail if we havent eaten the food mimics movement)
#15. Prints game. First we print ANSI escape code to go to top left corner.
#15cont. Print out string variable of pixel, which is a pre made string yet to fromat in the integer which corresponds to a color. This set the space character ' ' background to the color of the corresponding number.
#15cont. 10(which is green) if the [x,y] coordinate we are printing is in the snake list, 1(red) if the [x,y] coordinate we are printing is the food, and 8(grey) otherwise
#15cont. Multiply (or print this character) 'defintion' number of times. Then do this process for all x's in the width and y's in the height. 
#16. Wait .08 seconds if we are moving vertically(if |dy| = 1) otherwise wait a shorter period of .04 seconds. This is because if we waited the same time, it would look like the snake travels faster vertically, than horizontally, due to the ' ' character not being a perefect square
