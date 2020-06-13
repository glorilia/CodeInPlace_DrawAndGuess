"""
File: GAproject.py
--------------------
This file contains Glorili Alejandro's final project
for Stanford's Code In Place python course, Spring 2020.

Run on Python 3 or higher.

This program, along with the file "Drawing_Coordinates" and images directory,
has the user trace over dots on a canvas to make a drawing.
The user has a specified amount of time to trace over all the dots.
Once time is up, or the drawing is fully traced, the user is prompted to guess
the subject of the drawing. They are told if they are correct, then shown the
image of the real drawing. The user is asked if they want to continue, and the game
continues until they exit by typing anything but 'y' or 'Y'.
"""


import tkinter
import time
import random
from PIL import ImageTk
from PIL import Image


GAME_NAME = "Guess Your Drawing"
COORDS_FILE_NAME = 'Drawing_Coordinates'
CANVAS_WIDTH = 600
CANVAS_HEIGHT = 600
PATH_SIZE = 5
DOT_SIZE = 10
ALLOWED_TIME = 30 # in seconds
DELAY = 1 / 75


def main():
    # Create blank canvas according constants.
    canvas = make_canvas(CANVAS_WIDTH, CANVAS_HEIGHT, GAME_NAME)

    # Continue playing drawing activity until user types in value for keep_playing
    # as something other than y or Y for yes. Initialized with 'y' to enter loop
    keep_playing = 'y'
    while keep_playing == 'y' or keep_playing == 'Y':
        keep_playing = play_drawing_activity(canvas)

    # Outro
    print('Okay, byeeee!')

    canvas.mainloop()


def play_drawing_activity(canvas):
    # Clear anything that might be on the canvas.
    canvas.delete("all")

    # Draw dots that make up the drawing with their state='hidden' (invisible to viewer).
    # Save dictionary of shape, with shape name as the key, and the list of dots as its value.
    invisible_shape = draw_invisible_dots(canvas)

    # Save the string of the shapes's name. Get dict's keys as a list, then the first list item.
    shape_name = list(invisible_shape.keys())[0]

    # Create hidden image of the full shape, to be revealed at the end
    image = ImageTk.PhotoImage(Image.open("images/"+shape_name+".jpg"))
    full_shape = canvas.create_image(0, 0, anchor="nw", image=image, state='hidden')

    # Get list of dots in order they will be drawn
    invisible_dots = invisible_shape[shape_name]

    # Reveal first dot, at index 0
    dot_index = 0
    target = reveal_next_dot(canvas, invisible_dots, dot_index)

    # Capture cursor coordinates to enter while loop
    mouse_x = canvas.winfo_pointerx() - canvas.winfo_rootx()
    mouse_y = canvas.winfo_pointery() - canvas.winfo_rooty()

    # Allow  the cursor to move to the first dot without leaving a trail
    while not mouse_on_target(canvas, mouse_x, mouse_y, target):
        # Each loop checks if cursor is on target, exits when cursor meets target
        mouse_x = canvas.winfo_pointerx() - canvas.winfo_rootx()
        mouse_y = canvas.winfo_pointery() - canvas.winfo_rooty()
        canvas.update()
        time.sleep(DELAY)

    # Determine start time and end time of drawing activity
    start_time = time.time()
    end_time = start_time + ALLOWED_TIME

    # Continue drawing activity until end time OR all dots are traced over
    while time.time() < end_time:
        # Capture cursor coordinates
        mouse_x = canvas.winfo_pointerx() - canvas.winfo_rootx()
        mouse_y = canvas.winfo_pointery() - canvas.winfo_rooty()

        # Draw squares that form the path
        draw_path(canvas, mouse_x, mouse_y)

        # Reveal next dot when cursor meets the current target
        if mouse_on_target(canvas, mouse_x, mouse_y, target):
            make_dot_black(canvas, invisible_dots, dot_index)

            # Change index, to specify next dot
            dot_index += 1

            # Exit loop if the index reaches the length of the invisible_dots list
            if dot_index == len(invisible_dots):
                break

            # Reveal next dot in invisible_dots, specified by the updated index
            # Save revealed dot as the next target for the loop
            target = reveal_next_dot(canvas, invisible_dots, dot_index)

        canvas.update()
        time.sleep(DELAY)

    # Ask user for a guess on what they just drew
    guess = input('What did you draw?: ')

    # Let user know if they got it right or wrong
    if shape_name.upper() in guess.upper():
        print("That's right! It's a", shape_name + '!')
    else:
        print("That's not it! It's a", shape_name + '!')

    # Show image of full shape behind drawing
    canvas.itemconfig(full_shape, state='normal')

    # Ask user if they'd like to continue, and return the response
    keep_playing = input('Wanna try another one? Type Y or N: ')

    return keep_playing


def make_dot_black(canvas, dot_list, index):
    """
    Changes the fill of a dot at a specified index in dot_list to black, returns filled dot.

    :param canvas: canvas for drawings
    :param dot_list: list of dots that make up the drawing
    :param index : specifies which dot the function is configuring
    :return dot_list[index]: returns dot at index from dot_list, now with fill='black'
    """
    canvas.itemconfig(dot_list[index], fill='black')
    return dot_list[index]


def reveal_next_dot(canvas, dot_list, index):
    """
    Changes the state of a dot at a specified index in dot_list to 'normal', returns that dot.

    :param canvas: canvas for drawings
    :param dot_list: list of dots that make up the drawing
    :param index : specifies which dot the program is revealing (changing state to 'normal')
    :return dot_list[index]: returns dot at index from dot_list, now with state='normal'
    """
    canvas.itemconfig(dot_list[index], state='normal')
    return dot_list[index]


def draw_invisible_dots(canvas):
    """
    This function reads the coordinates file, usually "Drawing_Coordinates", line by line.
    It then draws 'hidden' dots on the canvas. Their state will change to
    'normal' in the animation loop according to the user's actions.
    It returns a list of the dots in the order they will be revealed.

    *IMPT*  Specifics about the coordinates file:
    FILE MUST END WITH TWO AND ONLY TWO BLANK LINES!
    SHAPE NAME LINE MUST BE AS FOLLOWS: "Shape, <shape-name-here>" ex: "Shape, Flower"
    MUST HAVE ONE AND ONLY ONE BLANK LINE BETWEEN EACH SHAPE!

    :param canvas: canvas for drawings
    :return list of dots: an ordered list of the dots the user will trace
    """
    shapes_list = []
    dot_dict = {}
    label = 'name'
    for line in open(COORDS_FILE_NAME):
        # checks if line is blank.
        if line.strip() == "":
            shapes_list.append(dot_dict)
            continue
        # Look at line in loop, get rid of white space and ends, and split at ', '.
        content = (line.strip().split(', '))
        if content[0] == 'Shape':
            dot_dict = {}
            label = content[1]
            dot_dict[label] = []
        else:
            dot_x = int(content[0])
            dot_y = int(content[1])
            dot_dict[label].append(canvas.create_oval(dot_x, dot_y, dot_x + DOT_SIZE, dot_y + DOT_SIZE, state='hidden', fill='red', outline='white'))

    chosen_shape_num = random.randint(0, (len(shapes_list)-1))

    return shapes_list[chosen_shape_num]


def mouse_on_target(canvas, current_x, current_y, target):
    """
    Tells you if the current location of the cursor is within the area of a target shape.

    :param canvas: canvas for drawings
    :param current_x: the current x location of the cursor
    :param current_y: the current y location of the cursor
    :param target: the shape we are comparing the cursor location to
    :return boolean: True if both x and y locations of the cursor are within the target
    """
    target_x_min = canvas.coords(target)[0]
    target_x_max = canvas.coords(target)[2]
    target_y_min = canvas.coords(target)[1]
    target_y_max = canvas.coords(target)[3]
    mouse_in_x = target_x_min < current_x < target_x_max
    mouse_in_y = target_y_min < current_y < target_y_max
    return mouse_in_x and mouse_in_y


def draw_path(canvas, mouse_x, mouse_y):
    """
    Draws a black square of PATH_SIZE dimensions onto canvas at mouse location.

    :param canvas: canvas for drawings
    :param mouse_x: mouse's x location
    :param mouse_y: mouse's y location
    """
    canvas.create_rectangle(mouse_x, mouse_y, mouse_x + PATH_SIZE, mouse_y + PATH_SIZE, fill='black')


def make_canvas(width, height, title=None):
    """
    DO NOT MODIFY
    Creates and returns a drawing canvas
    ready for drawing.
    """
    objects = {}
    top = tkinter.Tk()
    top.minsize(width=width, height=height)
    if title:
        top.title(title)
    canvas = tkinter.Canvas(top, width=width + 1, height=height + 1)
    canvas.pack()
    return canvas


if __name__ == '__main__':
    main()
