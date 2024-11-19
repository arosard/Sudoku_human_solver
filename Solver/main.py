from tkinter import Tk
from sudoku import Sudoku
from sudoku_gui import SudokuUI


def main():
    root = Tk()
    sudoku = Sudoku()

    sudoku_ui = SudokuUI(root, sudoku)
    sudoku_ui.mainloop()

if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()
