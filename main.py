

import tkinter as tk
from ui import ExpenseTrackerApp


def main():
    root = tk.Tk()

    app = ExpenseTrackerApp(root)

    root.mainloop()


if __name__ == "__main__":
    main()
