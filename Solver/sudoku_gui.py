from tkinter import (
    Button,
    Canvas,
    Checkbutton,
    Frame,
    BOTH,
    IntVar,
    LEFT,
    Text,
    filedialog,
)

from sudoku import Sudoku
from sudoku_human_solver import SudokuSolver
from sudoku_parser import SudokuParser

CELL_SIZE = 50
GRID_SIZE = 9
CANVAS_SIZE = CELL_SIZE * GRID_SIZE + 2 * CELL_SIZE


class SudokuUI(Frame):

    def __init__(self, parent, sudoku):
        super().__init__(parent)
        self.parent = parent
        self.sudoku = sudoku
        self.solver = SudokuSolver(sudoku)
        self.selected_cell = None
        self.canvas = None
        self.stats_text = None
        self.show_candidates = IntVar(value=1)
        self.init_ui()

    def init_ui(self):
        self.parent.title("Sudoku")
        self.parent.configure(bg="white")
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self, width=CANVAS_SIZE, height=CANVAS_SIZE)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=1)
        self.canvas.bind("<Button-1>", self.cell_clicked)
        self.canvas.bind("<Key>", self.key_pressed)
        self.canvas.configure(bg="white")
        self.canvas.focus_set()
        self.draw_grid()
        self.draw_sudoku()

        button_frame = Frame(self)
        button_frame.pack(pady=10)

        solve_button = Button(
            button_frame,
            text="Solve",
            command=self.solve_sudoku,
            font=("Arial", 14, "bold"),
            bg="#4CAF50",
            fg="white",
            relief="raised",
            borderwidth=3,
            padx=10,
            pady=5,
        )
        solve_button.pack(side=LEFT, padx=5)

        import_button = Button(
            button_frame,
            text="Import",
            command=self.import_sudoku,
            font=("Arial", 14, "bold"),
            bg="#2196F3",
            fg="white",
            relief="raised",
            borderwidth=3,
            padx=10,
            pady=5,
        )
        import_button.pack(side=LEFT, padx=5)

        button_frame2 = Frame(self)
        button_frame2.pack(pady=5)

        remove_candidates_button = Button(
            button_frame2,
            text="Remove candidates",
            command=self.remove_candidates,
            font=("Arial", 14, "bold"),
            bg="#FFC107",
            fg="white",
            relief="raised",
            borderwidth=3,
            padx=10,
            pady=5,
        )
        remove_candidates_button.pack(side=LEFT, padx=5)

        clear_button = Button(
            button_frame,
            text="Clear",
            command=self.clear_sudoku,
            font=("Arial", 14, "bold"),
            bg="#FF5722",
            fg="white",
            relief="raised",
            borderwidth=3,
            padx=10,
            pady=5,
        )
        clear_button.pack(side=LEFT, padx=5)

        self.stats_text = Text(self, height=10, width=50)
        self.stats_text.pack()

        # Third line for the checkbox
        checkbox_frame = Frame(self)
        checkbox_frame.pack(pady=5)

        candidates_checkbox = Checkbutton(
            checkbox_frame,
            text="Show Candidates",
            variable=self.show_candidates,
            command=self.draw_sudoku,
            font=("Arial", 14, "bold"),
            bg="white",
        )
        candidates_checkbox.pack(side=LEFT, padx=5)

    def draw_grid(self):
        for i in range(GRID_SIZE + 1):
            color = "black" if i % 3 == 0 else "gray"
            self.canvas.create_line(
                CELL_SIZE,
                CELL_SIZE + i * CELL_SIZE,
                CANVAS_SIZE - CELL_SIZE,
                CELL_SIZE + i * CELL_SIZE,
                fill=color,
            )
            self.canvas.create_line(
                CELL_SIZE + i * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE + i * CELL_SIZE,
                CANVAS_SIZE - CELL_SIZE,
                fill=color,
            )

    def draw_sudoku(self):
        self.canvas.delete("numbers")
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                cell = self.sudoku.cells[row][col]
                if cell.value:
                    self.canvas.create_text(
                        CELL_SIZE * (col + 1.5),
                        CELL_SIZE * (row + 1.5),
                        text=cell.value,
                        font=("Arial", 20),
                        tags="numbers",
                        fill="#344861",
                    )
                elif self.show_candidates.get():
                    candidates = list(cell.candidates)
                    for i, candidate in enumerate(candidates):
                        x_offset = (i % 3) * (CELL_SIZE // 3) + CELL_SIZE // 6
                        y_offset = (i // 3) * (CELL_SIZE // 3) + CELL_SIZE // 6
                        self.canvas.create_text(
                            CELL_SIZE * col + x_offset + CELL_SIZE,
                            CELL_SIZE * row + y_offset + CELL_SIZE,
                            text=candidate,
                            font=("Arial", 10),
                            tags="numbers",
                            fill="#D3D3D3",
                        )

    def cell_clicked(self, event):
        x, y = event.x, event.y
        if (
            CELL_SIZE <= x <= CANVAS_SIZE - CELL_SIZE
            and CELL_SIZE <= y <= CANVAS_SIZE - CELL_SIZE
        ):
            row, col = (y - CELL_SIZE) // CELL_SIZE, (x - CELL_SIZE) // CELL_SIZE
            self.selected_cell = (row, col)
            self.draw_selection()
            self.draw_sudoku()

    def draw_selection(self):
        self.canvas.delete("selection")
        if self.selected_cell:
            row, col = self.selected_cell

            # Highlight the row and column
            for i in range(GRID_SIZE):
                self.canvas.create_rectangle(
                    CELL_SIZE + col * CELL_SIZE + 1,
                    CELL_SIZE + i * CELL_SIZE + 1,
                    CELL_SIZE * (col + 2) - 1,
                    CELL_SIZE * (i + 2) - 1,
                    outline="",
                    fill="#E0F7FA",
                    tags="selection",
                )
                self.canvas.create_rectangle(
                    CELL_SIZE + i * CELL_SIZE + 1,
                    CELL_SIZE + row * CELL_SIZE + 1,
                    CELL_SIZE * (i + 2) - 1,
                    CELL_SIZE * (row + 2) - 1,
                    outline="",
                    fill="#E0F7FA",
                    tags="selection",
                )

            # Highlight the square
            start_row, start_col = (row // 3) * 3, (col // 3) * 3
            for i in range(3):
                for j in range(3):
                    self.canvas.create_rectangle(
                        CELL_SIZE + (start_col + j) * CELL_SIZE + 1,
                        CELL_SIZE + (start_row + i) * CELL_SIZE + 1,
                        CELL_SIZE * (start_col + j + 2) - 1,
                        CELL_SIZE * (start_row + i + 2) - 1,
                        outline="",
                        fill="#E0F7FA",
                        tags="selection",
                    )

            # Highlight the selected cell
            self.canvas.create_rectangle(
                CELL_SIZE + col * CELL_SIZE + 1,
                CELL_SIZE + row * CELL_SIZE + 1,
                CELL_SIZE * (col + 2) - 1,
                CELL_SIZE * (row + 2) - 1,
                outline="",
                fill="#B2EBF2",
                tags="selection",
            )

    def key_pressed(self, event):
        if self.selected_cell and event.char.isdigit() and 1 <= int(event.char) <= 9:
            row, col = self.selected_cell
            self.sudoku.set_value(row, col, int(event.char))
            self.draw_sudoku()
        # if event is an arrow key move selected cell
        elif event.keysym == "Up":
            self.move_selection(-1, 0)
        elif event.keysym == "Down":
            self.move_selection(1, 0)
        elif event.keysym == "Left":
            self.move_selection(0, -1)
        elif event.keysym == "Right":
            self.move_selection(0, 1)

    def import_sudoku(self):
        file_path = filedialog.askopenfilename(filetypes=[("All files", "*.*")])
        if file_path:
            self.sudoku = SudokuParser.parse_sudoku(file_path)
            self.solver = SudokuSolver(self.sudoku)
            self.draw_sudoku()
            self.stats_text.delete(1.0, "end")

    def remove_candidates(self):
        # self.solver.hidden_n_tuples()
        self.solver.naked_n_tuples()
        self.draw_sudoku()

    def solve_sudoku(self):
        self.solver.solve()
        self.draw_sudoku()
        self.show_stats()

    def show_stats(self):
        self.stats_text.delete(1.0, "end")
        if self.sudoku.is_sudoku_solved():
            self.stats_text.insert("end", "Sudoku solved!\n")
        elif self.sudoku.is_impossible():
            self.stats_text.insert("end", "Sudoku is impossible\n")
        else:
            self.stats_text.insert("end", "Sudoku could not be solved\n")
        for strategy, counts in self.solver.count_strategies.items():
            self.stats_text.insert(
                "end", f"{strategy}: {counts[0]} times, {counts[1]} numbers found\n"
            )

    def clear_sudoku(self):
        self.sudoku = Sudoku()
        self.solver = SudokuSolver(self.sudoku)
        self.draw_sudoku()
        self.stats_text.delete(1.0, "end")

    def move_selection(self, row_move, col_move):
        if self.selected_cell:
            row, col = self.selected_cell
            if (
                (row == 0 and row_move == -1)
                or (row == 8 and row_move == 1)
                or (col == 0 and col_move == -1)
                or (col == 8 and col_move == 1)
            ):
                return
            new_row, new_col = row + row_move, col + col_move
            if 0 <= new_row < GRID_SIZE and 0 <= new_col < GRID_SIZE:
                self.selected_cell = (new_row, new_col)
                self.draw_selection()
                self.draw_sudoku()
