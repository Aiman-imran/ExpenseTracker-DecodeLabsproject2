import tkinter as tk
from tkinter import messagebox, font
from expense_manager import ExpenseManager

BG_DARK      = "#1a1a2e"
BG_CARD      = "#16213e"
BG_INPUT     = "#0f3460"
ACCENT       = "#e94560"
ACCENT_HOVER = "#c73652"
TEXT_WHITE   = "#eaeaea"
TEXT_DIM     = "#8892a4"
TEXT_GREEN   = "#4ecca3"
BORDER       = "#0f3460"

class ExpenseTrackerApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("700x800")
        self.root.resizable(False, False)
        self.root.configure(bg=BG_DARK)
        self.manager = ExpenseManager()

        self._build_header()
        self._build_input_section()
        self._build_stats_bar()
        self._build_expense_list()
        self._build_footer()

    def _build_header(self):
        header_frame = tk.Frame(self.root, bg=ACCENT, pady=18)
        header_frame.pack(fill="x")

        tk.Label(
            header_frame,
            text="Expense Tracker",
            font=("Helvetica", 22, "bold"),
            bg=ACCENT,
            fg=TEXT_WHITE
        ).pack()

        tk.Label(
            header_frame,
            text="Track your spendings here",
            font=("Helvetica", 10),
            bg=ACCENT,
            fg="#f7c5ce"
        ).pack()

    def _build_input_section(self):
        card = tk.Frame(self.root, bg=BG_CARD, padx=24, pady=20)
        card.pack(fill="x", padx=20, pady=(18, 8))

        tk.Label(card, text="spending type?",
                 font=("Helvetica", 10, "bold"),
                 bg=BG_CARD, fg=TEXT_DIM).pack(anchor="w")

        self.label_var = tk.StringVar()
        label_entry = tk.Entry(
            card, textvariable=self.label_var,
            font=("Helvetica", 13),
            bg=BG_INPUT, fg=TEXT_WHITE,
            insertbackground=TEXT_WHITE,
            relief="flat", bd=0
        )
        label_entry.pack(fill="x", ipady=9, pady=(4, 12))
        label_entry.insert(0, "e.g. food, Transport, rents")
        # Clear placeholder on click
        label_entry.bind("<FocusIn>",  lambda e: self._clear_placeholder(label_entry, "e.g. food, Transport, rents"))
        label_entry.bind("<FocusOut>", lambda e: self._restore_placeholder(label_entry, "e.g. food, Transport, rents"))

        tk.Label(card, text="Amount",
                 font=("Helvetica", 10, "bold"),
                 bg=BG_CARD, fg=TEXT_DIM).pack(anchor="w")

        self.amount_var = tk.StringVar()
        self.amount_entry = tk.Entry(
            card, textvariable=self.amount_var,
            font=("Helvetica", 13),
            bg=BG_INPUT, fg=TEXT_WHITE,
            insertbackground=TEXT_WHITE,
            relief="flat", bd=0
        )
        self.amount_entry.pack(fill="x", ipady=9, pady=(4, 16))

        self.amount_entry.bind("<Return>", lambda event: self._add_expense())

        add_btn = tk.Button(
            card,
            text="＋  Add",
            font=("Helvetica", 12, "bold"),
            bg=ACCENT, fg=TEXT_WHITE,
            activebackground=ACCENT_HOVER,
            activeforeground=TEXT_WHITE,
            relief="flat", bd=0,
            cursor="hand2",
            command=self._add_expense
        )
        add_btn.pack(fill="x", ipady=10)
        self._bind_hover(add_btn, ACCENT, ACCENT_HOVER)

    def _build_stats_bar(self):
        stats_frame = tk.Frame(self.root, bg=BG_DARK)
        stats_frame.pack(fill="x", padx=20, pady=(0, 8))
        self.total_label   = self._stat_box(stats_frame, "Total spent",    "PKR 0.00")
        self.count_label   = self._stat_box(stats_frame, "Expenses",        "0")
        self.average_label = self._stat_box(stats_frame, "AVERAGE",         "PKR 0.00")

    def _stat_box(self, parent, title, initial_value):
        box = tk.Frame(parent, bg=BG_CARD, padx=12, pady=12)
        box.pack(side="left", expand=True, fill="both", padx=4)

        tk.Label(box, text=title,
                 font=("Helvetica", 8, "bold"),
                 bg=BG_CARD, fg=TEXT_DIM).pack()

        value_lbl = tk.Label(box, text=initial_value,
                             font=("Helvetica", 14, "bold"),
                             bg=BG_CARD, fg=TEXT_GREEN)
        value_lbl.pack()
        return value_lbl
    def _build_expense_list(self):
        header_row = tk.Frame(self.root, bg=BG_DARK)
        header_row.pack(fill="x", padx=24, pady=(4, 4))

        tk.Label(header_row, text="History",
                 font=("Helvetica", 11, "bold"),
                 bg=BG_DARK, fg=TEXT_WHITE).pack(side="left")

        clear_btn = tk.Button(
            header_row, text="Clear history",
            font=("Helvetica", 9),
            bg=BG_DARK, fg=TEXT_DIM,
            activeforeground=ACCENT,
            relief="flat", bd=0,
            cursor="hand2",
            command=self._clear_all
        )
        clear_btn.pack(side="right")

        container = tk.Frame(self.root, bg=BG_DARK)
        container.pack(fill="both", expand=True, padx=20)

        canvas = tk.Canvas(container, bg=BG_DARK, highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        self.list_frame = tk.Frame(canvas, bg=BG_DARK)
        self.canvas_window = canvas.create_window((0, 0), window=self.list_frame, anchor="nw")

        self.list_frame.bind("<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>",
            lambda e: canvas.itemconfig(self.canvas_window, width=e.width))

        canvas.bind_all("<MouseWheel>",
            lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

        self.canvas = canvas

        self.empty_label = tk.Label(
            self.list_frame,
            text="No expenses right now. ",
            font=("Helvetica", 11),
            bg=BG_DARK, fg=TEXT_DIM,
            justify="center"
        )
        self.empty_label.pack(pady=40)

    def _build_footer(self):
        tk.Label(
            self.root,
            text="Built with Python & Tkinter  •  Internship Project",
            font=("Helvetica", 8),
            bg=BG_DARK, fg=TEXT_DIM
        ).pack(pady=8)

    def _add_expense(self):
        label  = self.label_var.get()
        amount_str = self.amount_var.get().strip()

        if label in ("", "e.g. food, Transport, rents"):
            label = "Expense"

        # Guard: amount field is empty
        if not amount_str:
            messagebox.showwarning( "Please enter an amount first.")
            return

        # Guard: amount must be a valid number
        try:
            amount = float(amount_str)
        except ValueError:
            messagebox.showerror("Invalid Amount", f'"{amount_str}" is not a valid number.')
            return

        if amount <= 0:
            messagebox.showwarning("Invalid Amount")
            return

        expense = self.manager.add_expense(label, amount)

        self.label_var.set("")
        self.amount_var.set("")
        self.amount_entry.focus()
        self._refresh_list()
        self._refresh_stats()

    def _delete_expense(self, index):
        self.manager.delete_expense(index)
        self._refresh_list()
        self._refresh_stats()

    def _clear_all(self):
        if not self.manager.expenses:
            return
        confirmed = messagebox.askyesno(
            "Clear history", "Do you want to delete all expenses?"
        )
        if confirmed:
            self.manager.clear_all()
            self._refresh_list()
            self._refresh_stats()

    def _refresh_stats(self):
        self.total_label.config(text=f"PKR {self.manager.total:,.2f}")
        self.count_label.config(text=str(self.manager.get_count()))
        self.average_label.config(text=f"PKR {self.manager.get_average():,.2f}")

    def _refresh_list(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        if not self.manager.expenses:
            self.empty_label = tk.Label(
                self.list_frame,
                text="No any expense right now.",
                font=("Helvetica", 11),
                bg=BG_DARK, fg=TEXT_DIM,
                justify="center"
            )
            self.empty_label.pack(pady=40)
            return

        for idx, expense in enumerate(self.manager.expenses):
            self._draw_expense_row(idx, expense)

    def _draw_expense_row(self, idx, expense):
        row = tk.Frame(self.list_frame, bg=BG_CARD, pady=10, padx=14)
        row.pack(fill="x", pady=3)

        left = tk.Frame(row, bg=BG_CARD)
        left.pack(side="left", fill="x", expand=True)

        tk.Label(left, text=expense["label"],
                 font=("Helvetica", 11, "bold"),
                 bg=BG_CARD, fg=TEXT_WHITE,
                 anchor="w").pack(anchor="w")

        tk.Label(left, text=expense["date"],
                 font=("Helvetica", 8),
                 bg=BG_CARD, fg=TEXT_DIM,
                 anchor="w").pack(anchor="w")

        right = tk.Frame(row, bg=BG_CARD)
        right.pack(side="right")

        tk.Label(right, text=f"PKR {expense['amount']:,.2f}",
                 font=("Helvetica", 12, "bold"),
                 bg=BG_CARD, fg=TEXT_GREEN).pack(side="left", padx=(0, 12))

        del_btn = tk.Button(
            right, text="✕",
            font=("Helvetica", 10, "bold"),
            bg=BG_CARD, fg=TEXT_DIM,
            activeforeground=ACCENT,
            relief="flat", bd=0,
            cursor="hand2",
            command=lambda i=idx: self._delete_expense(i)
        )
        del_btn.pack(side="left")

    def _clear_placeholder(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, "end")
            entry.config(fg=TEXT_WHITE)

    def _restore_placeholder(self, entry, placeholder):

        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.config(fg=TEXT_DIM)

    def _bind_hover(self, widget, normal_color, hover_color):
        widget.bind("<Enter>", lambda e: widget.config(bg=hover_color))
        widget.bind("<Leave>", lambda e: widget.config(bg=normal_color))
