import customtkinter as ctk
from tkinter import messagebox

from calculator import calculate, save_history, read_history, clear_history


#Theme "Voyage" (modifiable facilement)
ctk.set_appearance_mode("light")          # "light" ou "dark"
ctk.set_default_color_theme("blue")      # theme interne, on override via couleurs

COL_BG = "#F6EFE6"        # sable
COL_CARD = "#EFE3D3"      # carte
COL_TEXT = "#1F1F1F"
COL_ACCENT = "#2F5D50"    # vert bouteille
COL_GOLD = "#B68D40"      # doré doux
COL_BTN = "#FFFFFF"
COL_BTN_OP = "#E7F0ED"
COL_BTN_DANGER = "#F3D9D9"


class TravelCalcCTK(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        self.title("Calculette Voyage ✈️")
        self.geometry("470x720")
        self.resizable(False, False)
        self.configure(fg_color=COL_BG)

        self.expr_var = ctk.StringVar(value="")

        # Header (carte)

        header = ctk.CTkFrame(self, fg_color=COL_CARD, corner_radius=18)
        header.pack(fill="x", padx=16, pady=(16, 10))

        top = ctk.CTkFrame(header, fg_color="transparent")
        top.pack(fill="x", padx=16, pady=(14, 4))

        ctk.CTkLabel(
            top,
            text="Hiba • Travel Calculator ✈️",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COL_TEXT,
        ).pack(side="left")

        ctk.CTkLabel(
            top,
            text="🧭",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COL_ACCENT,
        ).pack(side="right")

        ctk.CTkLabel(
            header,
            text="Ton calcul comme un itinéraire",
            font=ctk.CTkFont(size=12),
            text_color=COL_ACCENT,
            anchor="w",
        ).pack(fill="x", padx=16, pady=(0, 12))

        # Ligne dorée
        ctk.CTkFrame(self, fg_color=COL_GOLD, height=4, corner_radius=10).pack(
            fill="x", padx=16, pady=(0, 12)
        )

        # Display (écran)

        display = ctk.CTkEntry(
            self,
            textvariable=self.expr_var,
            height=54,
            corner_radius=16,
            fg_color="#FFFFFF",
            text_color=COL_TEXT,
            border_color=COL_CARD,
            border_width=2,
            font=ctk.CTkFont(size=22, weight="bold"),
            justify="right",
        )
        display.pack(fill="x", padx=16, pady=(0, 12))
        display.focus_set()

        # Boutons (carte + grid)

        btn_card = ctk.CTkFrame(self, fg_color=COL_CARD, corner_radius=18)
        btn_card.pack(fill="x", padx=16, pady=(0, 12))

        grid = ctk.CTkFrame(btn_card, fg_color="transparent")
        grid.pack(padx=12, pady=12)  # ✅ pack ici, et grid() pour les boutons seulement

        buttons = [
            ("7", "num"), ("8", "num"), ("9", "num"), ("/", "op"),
            ("4", "num"), ("5", "num"), ("6", "num"), ("*", "op"),
            ("1", "num"), ("2", "num"), ("3", "num"), ("-", "op"),
            ("0", "num"), (".", "num"), ("%", "op"), ("+", "op"),
            ("(", "op"), (")", "op"), ("^", "op"), ("C", "danger"),
            ("⌫", "act"), ("Carnet", "act"), ("Reset", "act"), ("=", "eq"),
        ]

        # placement 6 lignes x 4 colonnes
        idx = 0
        for r in range(6):
            for c in range(4):
                text, kind = buttons[idx]
                idx += 1
                btn = self._make_button(grid, text, kind)  # ✅ master = grid
                btn.grid(row=r, column=c, padx=6, pady=6, sticky="nsew")

        for c in range(4):
            grid.grid_columnconfigure(c, weight=1)

        # Historique (carte)

        hist_card = ctk.CTkFrame(self, fg_color=COL_CARD, corner_radius=18)
        hist_card.pack(fill="both", padx=16, pady=(0, 16), expand=True)

        ctk.CTkLabel(
            hist_card,
            text="🗒️ Carnet de voyage (historique)",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COL_TEXT,
        ).pack(anchor="w", padx=16, pady=(14, 8))

        self.history = ctk.CTkTextbox(
            hist_card,
            corner_radius=14,
            fg_color="#FFFFFF",
            text_color=COL_TEXT,
            font=ctk.CTkFont(size=12),
        )
        self.history.pack(fill="both", padx=16, pady=(0, 16), expand=True)
        self.history.configure(state="disabled")

        self.refresh_history()

        # Raccourcis
        self.bind("<Return>", lambda _e: self.on_equal())
        self.bind("<BackSpace>", lambda _e: self.backspace())

    def _make_button(self, parent: ctk.CTkFrame, text: str, kind: str) -> ctk.CTkButton:
        fg = COL_BTN
        text_col = COL_TEXT
        hover = "#EDEDED"

        if kind == "op":
            fg = COL_BTN_OP
            text_col = COL_ACCENT
            hover = "#DCEAE6"
        elif kind == "act":
            fg = COL_BG
            text_col = COL_TEXT
            hover = "#EFE3D3"
        elif kind == "danger":
            fg = COL_BTN_DANGER
            text_col = COL_TEXT
            hover = "#EFC8C8"
        elif kind == "eq":
            fg = COL_ACCENT
            text_col = "#FFFFFF"
            hover = "#264A40"

        return ctk.CTkButton(
            master=parent,
            text=text,
            width=92,
            height=48,
            corner_radius=16,
            fg_color=fg,
            hover_color=hover,
            text_color=text_col,
            font=ctk.CTkFont(size=16, weight="bold"),
            command=lambda t=text: self.on_button(t),
        )

    def on_button(self, t: str) -> None:
        if t == "C":
            self.expr_var.set("")
            return
        if t == "⌫":
            self.backspace()
            return
        if t == "🗺️ Carnet":
            self.refresh_history()
            return
        if t == "🧹 Reset":
            self.clear_hist()
            return
        if t == "=":
            self.on_equal()
            return

        self.expr_var.set(self.expr_var.get() + t)

    def backspace(self) -> None:
        s = self.expr_var.get()
        self.expr_var.set(s[:-1])

    def on_equal(self) -> None:
        expr = self.expr_var.get().strip()
        if not expr:
            return
        try:
            res = calculate(expr)
            self.expr_var.set(str(res))
            save_history(f"{expr} = {res}")
            self.refresh_history()
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def refresh_history(self) -> None:
        content = read_history()
        self.history.configure(state="normal")
        self.history.delete("1.0", "end")
        self.history.insert("end", content if content else "Historique vide.")
        self.history.configure(state="disabled")

    def clear_hist(self) -> None:
        if messagebox.askyesno("Confirmation", "Effacer le carnet (historique) ?"):
            clear_history()
            self.refresh_history()


def main() -> None:
    app = TravelCalcCTK()
    app.mainloop()


if __name__ == "__main__":
    main()
