from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle

from p1 import Game2048

from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle

class Tile(Label):
    def _init_(self, **kwargs):
        super()._init_(**kwargs)
        self.rect = None
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_tile(self, value):
        self.canvas.before.clear()
        if value == 0:
            self.text = ""
        else:
            self.text = str(value)

            # Distinct and vibrant tile colors
            colors = {
                2: (0.4, 0.8, 0.4, 1),      # green
                4: (0.75, 0.85, 1.0, 1),       # sky blue
                8: (1.0, 0.75, 0.5, 1),        # light orange
                16: (1.0, 0.5, 0.3, 1),        # orange
                32: (1.0, 0.4, 0.3, 1),        # red-orange
                64: (1.0, 0.25, 0.2, 1),       # red
                128: (0.9, 0.85, 0.4, 1),      # gold
                256: (0.85, 0.75, 0.2, 1),     # darker gold
                512: (0.8, 0.7, 0.1, 1),       # brownish-gold
                1024: (0.8, 0.65, 0.0, 1),     # dark gold
                2048: (1.0, 0.6, 0.0, 1),      # bright orange-gold
            }

            color = colors.get(value, (0.6, 0.6, 0.6, 1))  # fallback gray

            with self.canvas.before:
                Color(*color)
                self.rect = Rectangle(pos=self.pos, size=self.size)

    def update_rect(self, *args):
        if self.rect:
            self.rect.pos = self.pos
            self.rect.size = self.size

class Game2048App(App):
    def build(self):
        Window.size = (400, 600)
        self.game = Game2048()

        root = BoxLayout(orientation='vertical', spacing=10, padding=10)

        self.score_label = Label(
            text=f"Score: {self.game.score}",
            size_hint=(1, 0.1),
            font_size='24sp'
        )
        root.add_widget(self.score_label)

        self.grid = GridLayout(cols=4, rows=4, spacing=5, size_hint=(1, 0.8))
        self.tiles = []
        for i in range(4):
            for j in range(4):
                tile = Tile(text="", font_size='32sp')
                tile.update_tile(self.game.board[i][j])
                self.tiles.append(tile)
                self.grid.add_widget(tile)
        root.add_widget(self.grid)

        # Buttons for moves
        buttons = BoxLayout(size_hint=(1, 0.1), spacing=10)
        btn_up = Button(text="UP", on_press=lambda x: self.make_move('up'))
        btn_left = Button(text="LEFT", on_press=lambda x: self.make_move('left'))
        btn_down = Button(text="DOWN", on_press=lambda x: self.make_move('down'))
        btn_right = Button(text="RIGHT", on_press=lambda x: self.make_move('right'))

        buttons.add_widget(btn_left)
        buttons.add_widget(btn_up)
        buttons.add_widget(btn_down)
        buttons.add_widget(btn_right)

        root.add_widget(buttons)

        self.update_grid()
        return root

    def make_move(self, direction):
        moved = False
        if direction == 'left':
            moved = self.game.move_left()
        elif direction == 'right':
            moved = self.game.move_right()
        elif direction == 'up':
            moved = self.game.move_up()
        elif direction == 'down':
            moved = self.game.move_down()

        if moved:
            self.update_grid()
            if not self.game.can_move():
                self.show_game_over()

    def update_grid(self):
        for i in range(4):
            for j in range(4):
                index = i*4 + j
                self.tiles[index].update_tile(self.game.board[i][j])
        self.score_label.text = f"Score: {self.game.score}"

    def show_game_over(self):
        popup = Popup(
            title="Game Over",
            content=Label(
                text=f"Game Over!\nYour Score: {self.game.score}",
                font_size='20sp'
            ),
            size_hint=(None, None),
            size=(300, 200)
        )
        popup.open()

if __name__ == '__main__':
    Game2048App().run()