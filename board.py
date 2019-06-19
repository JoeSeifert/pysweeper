import tkinter as tk
from tkinter import ttk
import mechanics as m
import os

# TO DO:
# - add pretty border
# - comment, you lazy fuck

class Minesweeper:

    def __init__(self, root, difficulty, nrows_cust=None, ncols_cust=None, n_mines_cust=None):
        self.root = root
        self.difficulty = difficulty
        self.nrows_cust = nrows_cust
        self.ncols_cust = ncols_cust
        self.n_mines_cust = n_mines_cust
        self.box_size = 32
        self.time = -1
        self.timer = None
        self.top_row = None
        self.game_canvas = None
        self.game = None
        self.status_message = tk.StringVar()
        self.current_box_row = 0
        self.current_box_col = 0

        # Make all the images!
        path = f'{os.getcwd()}\\images\\'
        self.mine_image = tk.PhotoImage(file=path+'mine_16.png')
        self.mine_image = self.mine_image.zoom(2)
        self.wrong_mine_image = tk.PhotoImage(file=path+'wrong_mine_16.png')
        self.wrong_mine_image = self.wrong_mine_image.zoom(2)
        self.hit_mine_image = tk.PhotoImage(file=path+'hit_mine_16.png')
        self.hit_mine_image = self.hit_mine_image.zoom(2)
        self.blank_image = tk.PhotoImage(file=path+'blank_16.png')
        self.blank_image = self.blank_image.zoom(2)
        self.flag_image = tk.PhotoImage(file=path+'flag_16.png')
        self.flag_image = self.flag_image.zoom(2)
        self.face_image = tk.PhotoImage(file=path+'face_smile_26.png')
        self.face_image = self.face_image.zoom(2)
        self.win_face_image = tk.PhotoImage(file=path+'face_win_26.png')
        self.win_face_image = self.win_face_image.zoom(2)
        self.lose_face_image = tk.PhotoImage(file=path+'face_lose_26.png')
        self.lose_face_image = self.lose_face_image.zoom(2)
        self.shocked_face_image = tk.PhotoImage(file=path+'face_shocked_26.png')
        self.shocked_face_image = self.shocked_face_image.zoom(2)
        self.indented_face_image = tk.PhotoImage(file=path+'indented_face_smile_26.png')
        self.indented_face_image = self.indented_face_image.zoom(2)
        self.number_images = ()
        for i in range(9):
            fn = path+'{}_16.png'.format(i)
            temp = tk.PhotoImage(file=fn)
            self.number_images += temp.zoom(2),
        self.timer_number_images = ()
        for i in range(10):
            fn = path+'timer_{}.png'.format(i)
            temp = tk.PhotoImage(file=fn)
            self.timer_number_images += temp,

        self.make_new_game()

    def make_new_game(self):
        """
        In order:
        -Tries to destroy existing game, if it exists
        -Makes new game (constructs grid/squares etc.)
        -Builds top row (mine count, face, timer)
        -Builds game canvas and draws all of the blank squares
        -Binds left click to initial left click

        Notes:
        - self.***_click_preamble functions are usually for drawing images (such as pressed-button images), or if
          actions change based on whether multiple buttons are pressed (self.simultaneous_click)
        - self.initial_left_click exists because the game generates mines that are not underneath or next to the first
          square clicked. Thus, it needs the first clicked square and treats it special.
        :return:
        """
        try:
            self.top_row.destroy()
            self.game_canvas.destroy()
            self.timer.destroy()
            # self.debug.destroy()
        except AttributeError:
            pass
        self.game = m.Game(self.difficulty, self.nrows_cust, self.ncols_cust, self.n_mines_cust)
        self.top_row = tk.Canvas(self.root, width=self.box_size * self.game.ncols, height=52)
        self.top_row.pack()
        self.top_row.create_image(self.box_size * self.game.ncols // 2, 26,
                                  image=self.face_image)
        self.top_row.bind('<ButtonPress-1>', self.top_left_click_preamble)

        self.make_timer(0)

        self.make_mine_count()
        self.game_canvas = tk.Canvas(self.root, width=self.box_size * self.game.ncols,
                                     height=self.box_size * self.game.nrows, highlightthickness=0)
        self.game_canvas.pack()
        # self.make_debug_label()
        for i in range(self.game.ncols):
            for j in range(self.game.nrows):
                center_x = (i + 0.5) * self.box_size
                center_y = (j + 0.5) * self.box_size
                self.game_canvas.create_image(center_x, center_y,
                                              image=self.blank_image)

        self.game_canvas.bind("<ButtonPress-1>", self.left_click_preamble)
        self.game_canvas.bind("<ButtonRelease-1>", self.initial_left_click)

    def top_left_click_preamble(self, event):
        """
        Just makes the indented-face image when clicked, does nothing if you click outside the face
        :param event: where the mouse clicked
        :return: None
        """
        smile_image_x = self.box_size * self.game.ncols // 2
        smile_image_y = 26
        smile_image_dim = 52  # height = width
        x_range = [smile_image_x - smile_image_dim, smile_image_x + smile_image_dim]
        y_range = [smile_image_y - smile_image_dim, smile_image_y + smile_image_dim]
        if event.x >= x_range[0] and event.x <= x_range[1] and event.y >= y_range[0] and event.y <= y_range[1]:
            self.top_row.create_image(self.box_size * self.game.ncols // 2, 26,
                                      image=self.indented_face_image)
            self.top_row.bind('<ButtonRelease-1>', self.top_left_click)

    def top_left_click(self, event):
        """
        Actually makes a new game when clicking the face
        :param event:
        :return:
        """
        self.top_row.unbind('<ButtonRelease-1>')
        self.make_new_game()

    def make_timer(self, number):
        """
        Makes the timer based on an integer number 0 <= number <= 999
        :param number: Timer number
        :return: None
        """
        number = str(number).rjust(3, '0')
        img_1 = self.timer_number_images[int(number[0])]
        img_2 = self.timer_number_images[int(number[1])]
        img_3 = self.timer_number_images[int(number[2])]
        self.top_row.create_image(4 * (self.box_size * self.game.ncols // 5) - 24, 26, image=img_1)
        self.top_row.create_image(4 * (self.box_size * self.game.ncols // 5), 26, image=img_2)
        self.top_row.create_image(4 * (self.box_size * self.game.ncols // 5) + 24, 26, image=img_3)

    def make_mine_count(self):
        """
        Like the timer, makes the mine count in the top row. Does not need input since the flagged/mines are class
        variables
        :return: None
        """
        mine_count = str(self.game.n_mines - self.game.num_flagged)
        mine_count = mine_count.rjust(3, '0')
        img_1 = self.timer_number_images[int(mine_count[0])]
        img_2 = self.timer_number_images[int(mine_count[1])]
        img_3 = self.timer_number_images[int(mine_count[2])]
        self.top_row.create_image((self.box_size * self.game.ncols // 5) - 24, 26, image=img_1)
        self.top_row.create_image((self.box_size * self.game.ncols // 5), 26, image=img_2)
        self.top_row.create_image((self.box_size * self.game.ncols // 5) + 24, 26, image=img_3)

    def initial_left_click(self, event):
        """
        Places all the mines, ensures no mines surround your initially-clicked square
        :param event:
        :return:
        """
        self.game_canvas.unbind('<Motion>')
        self.timer = Timer(self)
        self.timer.update_timer()
        box_col = event.x // self.box_size
        box_row = event.y // self.box_size
        self.top_row.create_image(self.box_size * self.game.ncols // 2, 26,
                                  image=self.face_image)
        self.game.make_game(box_row, box_col)
        self.game[box_row][box_col].reveal()
        self.check_state(box_row, box_col)
        self.update()
        self.game_canvas.bind("<ButtonPress-1>", self.left_click_preamble)
        self.game_canvas.bind("<ButtonRelease-1>", self.left_click)
        self.game_canvas.bind('<Button-3>', self.right_click)

    def left_click_preamble(self, event):
        """
        Draws indented image on square you left-click, and the indent even moves around when you move the mouse!
        Also makes the `:o' face on the top row
        :param event: click event
        :return:
        """
        self.top_row.create_image(self.box_size * self.game.ncols // 2, 26,
                                  image=self.shocked_face_image)
        box_col = event.x // self.box_size
        box_row = event.y // self.box_size
        self.game_canvas.bind('<Button-3>', self.simultaneous_click)
        try:
            box_is_revealed = self.game[box_row][box_col].is_revealed
            box_is_flagged = self.game[box_row][box_col].is_flagged
            i_should_do_anything = not (box_is_revealed or box_is_flagged)
        except IndexError:
            i_should_do_anything = True
        if i_should_do_anything:
            self.game_canvas.create_image(self.box_size * (box_col + 0.5), self.box_size * (box_row + 0.5),
                                          image=self.number_images[0])
        self.game_canvas.bind('<Motion>', self.motion)

    def simultaneous_click(self, event):
        """
        If left click is pressed, clicking right click will reveal all squares surrounding the selected square
        :param event:
        :return:
        """
        box_col = event.x // self.box_size
        box_row = event.y // self.box_size
        reveal_list = ()
        for i in range(-1, 2):
            for j in range(-1, 2):
                if not ((box_row - i) == box_row and (box_col - j) == box_col):
                    reveal_list += ((box_row - i, box_col - j),)

        for row, col in reveal_list:
            try:
                if row > -1 and col > -1:
                    self.game[row][col].reveal()
            except IndexError:
                pass
        self.check_state(box_row, box_col)
        self.update()

    def motion(self, event):
        """
        If you are holding left-click and move your mouse button, the indented square needs to move with your mouse.
        Determines whether the new square needs its image updated, whether the old square needs its image updated,
        and updates the images.
        :param event:
        :return:
        """
        box_col = event.x // self.box_size
        box_row = event.y // self.box_size
        if box_col != self.current_box_col or box_row != self.current_box_row:
            try:
                new_box_is_revealed = self.game[box_row][box_col].is_revealed
                new_box_is_flagged = self.game[box_row][box_col].is_flagged
                old_box_is_revealed = self.game[self.current_box_row][self.current_box_col].is_revealed
                old_box_is_flagged = self.game[self.current_box_row][self.current_box_col].is_flagged
            except IndexError:
                new_box_is_revealed = False
                new_box_is_flagged = False
                old_box_is_revealed = False
                old_box_is_flagged = False

            new_box_motion_condition = not (new_box_is_revealed or new_box_is_flagged)
            old_box_motion_condition = not (old_box_is_revealed or old_box_is_flagged)
            # print('New box condition: {0}. Old box condition: {1}'.format(new_box_motion_condition, old_box_motion_condition))

            if new_box_motion_condition and old_box_motion_condition:
                # both newly-entered box and previous box need images changed
                self.game_canvas.create_image(self.box_size * (self.current_box_col + 0.5),
                                              self.box_size * (self.current_box_row + 0.5),
                                              image=self.blank_image)
                self.game_canvas.create_image(self.box_size * (box_col + 0.5),
                                              self.box_size * (box_row + 0.5),
                                              image=self.number_images[0])
            elif not new_box_motion_condition and old_box_motion_condition:
                # only previous box needs image changed
                self.game_canvas.create_image(self.box_size * (self.current_box_col + 0.5),
                                              self.box_size * (self.current_box_row + 0.5),
                                              image=self.blank_image)
            elif new_box_motion_condition and not old_box_motion_condition:
                # only newly-entered box needs image changed
                self.game_canvas.create_image(self.box_size * (box_col + 0.5),
                                              self.box_size * (box_row + 0.5),
                                              image=self.number_images[0])
            self.current_box_row = box_row
            self.current_box_col = box_col

    def left_click(self, event):
        """
        Reveals the clicked square. Check's the state of the game after the click, updates the squares appropriately
        :param event:
        :return:
        """
        self.game_canvas.unbind('<Motion>')
        self.game_canvas.bind('<Button-3>', self.right_click)
        self.top_row.create_image(self.box_size * self.game.ncols // 2, 26,
                                  image=self.face_image)
        box_col = event.x // self.box_size
        box_row = event.y // self.box_size
        self.game[box_row][box_col].reveal()
        self.check_state(box_row, box_col)
        self.update()
        # self.update_status_msg()

    def right_click(self, event):
        """
        Flags/Unflags right-clicked square
        Updates mine count
        Updates square images
        :param event:
        :return:
        """
        box_col = event.x // self.box_size
        box_row = event.y // self.box_size
        self.game[box_row][box_col].flag()
        self.make_mine_count()
        self.update()
        # self.update_status_msg()

    def check_state(self, row, col):
        """
        Ends game if game is won or lost.
        If won: flags rest of the mines and gives you a cool-face B)
        If lost: shows the mine you hit, reveals all the mines, shows which flags were incorrect
        If either: unbinds all events except left clicking the face
        :param row:
        :param col:
        :return:
        """
        if self.game.check_win():
            self.game_canvas.unbind('<Motion>')
            self.game_canvas.unbind("<ButtonPress-1>")
            self.game_canvas.unbind("<ButtonRelease-1>")
            self.game_canvas.unbind("<Button-3>")
            self.timer.destroy()
            self.top_row.create_image(self.box_size * self.game.ncols // 2, 26,
                                      image=self.win_face_image)
            for game_row in self.game:
                for sq in game_row:
                    if not sq.is_flagged:
                        sq.flag()
                        self.make_mine_count()
                        self.update()

        elif self.game.check_lose():
            self.game_canvas.unbind('<Motion>')
            self.game_canvas.unbind("<ButtonPress-1>")
            self.game_canvas.unbind("<ButtonRelease-1>")
            self.game_canvas.unbind("<Button-3>")
            self.timer.destroy()
            self.top_row.create_image(self.box_size * self.game.ncols // 2, 26,
                                      image=self.lose_face_image)
            for game_row in self.game:
                for sq in game_row:
                    if sq.is_mine and sq.is_revealed:
                        self.game_canvas.create_image(self.box_size * (sq.col + 0.5), self.box_size * (sq.row + 0.5),
                                                      image=self.hit_mine_image)
                    elif not sq.is_mine and sq.is_flagged:
                        self.game_canvas.create_image(self.box_size * (sq.col + 0.5), self.box_size * (sq.row + 0.5),
                                                      image=self.wrong_mine_image)
                    elif sq.is_mine and not sq.is_flagged and not (sq.row == row and sq.col == col):
                        self.game_canvas.create_image(self.box_size * (sq.col + 0.5), self.box_size * (sq.row + 0.5),
                                                      image=self.mine_image)

    def update(self):
        """
        Updates each square's image if it is in the self.game.updated_squares list.
        :return:
        """
        updated_squares = self.game.updated_squares
        while updated_squares:
            sq = updated_squares[-1]
            if sq.is_flagged:
                self.game_canvas.create_image(self.box_size * (sq.col + 0.5), self.box_size * (sq.row + 0.5),
                                              image=self.flag_image)
            elif sq.is_mine and sq.is_revealed:
                self.game_canvas.create_image(self.box_size * (sq.col + 0.5), self.box_size * (sq.row + 0.5),
                                              image=self.mine_image)
            elif sq.is_revealed:
                self.game_canvas.create_image(self.box_size * (sq.col + 0.5), self.box_size * (sq.row + 0.5),
                                              image=self.number_images[sq.neighboring_mines])
            else:
                self.game_canvas.create_image(self.box_size * (sq.col + 0.5), self.box_size * (sq.row + 0.5),
                                              image=self.blank_image)
            del updated_squares[-1]

    # def make_debug_label(self):
    #     self.debug = tk.Label(self.root, textvariable=self.status_message)  # ignoring PEP for now
    #     self.debug.pack()
    #
    # def update_status_msg(self):
    #     status_str = 'N_mines = {0}. N_revealed = {1}. N_flagged = {2}. ' \
    #                  'End_condition = {3}. Win_condition = {4}'.format(self.game.n_mines, self.game.num_revealed,
    #                                                                    self.game.num_flagged,
    #                                                                    self.game.end_condition,
    #                                                                    self.game.win)
    #     print(status_str)
    #     self.status_message.set(status_str)


class Timer:

    """
    Controls the timer! Stops if self.end_condition is True or if time > 999 seconds
    """

    def __init__(self, master_class):
        self.master_class = master_class
        self.time = -1
        self.end_condition = False

    def __str__(self):
        return str(self.time).rjust(3, '0')

    def update_timer(self):
        self.time += 1
        if not (self.end_condition or self.time > 999):
            self.master_class.make_timer(self.time)
            self.master_class.root.after(1000, self.update_timer)

    def destroy(self):
        self.end_condition = True
        del self


def main():
    root = tk.Tk()
    cust = (3, 8, 2)
    Minesweeper(root, 'beginner')
    root.mainloop()


if __name__ == '__main__':
    main()
