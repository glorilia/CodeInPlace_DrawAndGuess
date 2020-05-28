"""
File: Get Drawing Coords.py
--------------------

This program, lets you click on a canvas to create a shape
and then gives you a list of the shapes' coordinates.
"""

import tkinter
from PIL import ImageTk
from PIL import Image

CANVAS_WIDTH = 600
CANVAS_HEIGHT = 600
DOT_SIZE = 7


def main():
    canvas = make_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    image = ImageTk.PhotoImage(Image.open("images/pineapple.jpg"))
    canvas.create_image(0, 0, anchor="nw", image=image)

    def make_dot(event):
        dot = canvas.create_oval(event.x, event.y, event.x + DOT_SIZE, event.y + DOT_SIZE, fill='black')
        print(str(int(canvas.coords(dot)[0])) + ', ' + str(int(canvas.coords(dot)[1])))

    canvas.bind('<Button-1>', make_dot)

    print()
    canvas.mainloop()


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
