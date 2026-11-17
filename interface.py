import random
import tkinter as tk
from tkinter import messagebox
from solver import GOAL, inversions, is_solvable, h, neighbors, astar

class TaquinApp:
    def __init__(self, root):
        self.root = root
        root.title("Taquin 3x3 - Algorithme A*")
        self.state = (2, 8, 3, 1, 6, 4, 7, 0, 5)
        self.busy = False

        left = tk.Frame(root, padx=10, pady=10)
        left.grid(row=0, column=0, sticky="n")

        tk.Label(left, text="État initial (cliquez un jeton\npour le glisser vers la case vide)",
                 font=("Arial", 11, "bold")).pack()
        board = tk.Frame(left, pady=8)
        board.pack()
        self.buttons = []
        for i in range(9):
            b = tk.Button(board, width=4, height=2, font=("Arial", 22, "bold"),
                          command=lambda i=i: self.on_click(i))
            b.grid(row=i // 3, column=i % 3, padx=2, pady=2)
            self.buttons.append(b)

        tk.Label(left, text="Saisir un état (9 chiffres, 0 = vide) :").pack()
        self.entry = tk.Entry(left, width=14, font=("Arial", 12), justify="center")
        self.entry.pack()
        self.entry.insert(0, "283164705")
        tk.Button(left, text="Appliquer l'état saisi", command=self.apply_entry).pack(pady=2)
        tk.Button(left, text="Mélanger (aléatoire solvable)", command=self.shuffle).pack(pady=2)
        tk.Button(left, text="Résoudre avec A*", bg="#4CAF50", fg="white",
                  font=("Arial", 11, "bold"), command=self.solve).pack(pady=8)

        self.info = tk.Label(left, text="", justify="left", wraplength=250)
        self.info.pack()

        tk.Label(left, text="État final (fixe) :", font=("Arial", 10, "bold")).pack(pady=(10, 0))
        goal_txt = "\n".join(" ".join(str(x) if x else "_" for x in GOAL[r*3:r*3+3])
                             for r in range(3))
        tk.Label(left, text=goal_txt, font=("Courier", 14)).pack()

        right = tk.Frame(root, padx=10, pady=10)
        right.grid(row=0, column=1)
        tk.Label(right, text="Étapes d'exploration (g, h, f)",
                 font=("Arial", 11, "bold")).pack()
        self.text = tk.Text(right, width=38, height=28, font=("Courier", 10))
        sb = tk.Scrollbar(right, command=self.text.yview)
        self.text.config(yscrollcommand=sb.set)
        self.text.pack(side="left")
        sb.pack(side="left", fill="y")

        self.refresh()

    def refresh(self):
        for i, v in enumerate(self.state):
            self.buttons[i].config(text=str(v) if v else "",
                                   bg="#DDDDDD" if v == 0 else "#FFFFFF")
        inv = inversions(self.state)
        self.info.config(text=f"Inversions : {inv} "
                              f"({'impair' if inv % 2 else 'pair'})\nh(n) = {h(self.state)}")

    def on_click(self, i):
        if self.busy:
            return
        b = self.state.index(0)
        (r1, c1), (r2, c2) = divmod(i, 3), divmod(b, 3)
        if abs(r1 - r2) + abs(c1 - c2) == 1:
            lst = list(self.state)
            lst[i], lst[b] = lst[b], lst[i]
            self.state = tuple(lst)
            self.refresh()

    def apply_entry(self):
        s = self.entry.get().strip().replace(",", "").replace(" ", "")
        if len(s) != 9 or sorted(s) != list("012345678"):
            messagebox.showerror("Erreur", "Saisissez les chiffres 0 à 8, chacun une seule fois.")
            return
        self.state = tuple(int(c) for c in s)
        self.refresh()

    def shuffle(self):
        if self.busy:
            return
        s = GOAL
        for _ in range(40):
            s = random.choice(neighbors(s))
        self.state = s
        self.refresh()

    def solve(self):
        if self.busy:
            return
        if self.state == GOAL:
            messagebox.showinfo("Info", "L'état initial est déjà l'état final.")
            return
        if not is_solvable(self.state):
            messagebox.showwarning(
                "Insoluble",
                f"{inversions(self.state)} inversions (pair) alors que l'état final en a "
                f"{inversions(GOAL)} (impair).\nCet état ne peut pas atteindre l'état final.")
            return

        path, log = astar(self.state)

        self.text.delete("1.0", "end")
        for k, (st, g, hh, f) in enumerate(log, 1):
            self.text.insert("end", f"Exploration {k} : g={g} h={hh} f={f}\n")
            for r in range(3):
                row = " ".join(str(x) if x else "_" for x in st[r*3:r*3+3])
                self.text.insert("end", f"    {row}\n")
        self.text.insert("end", f"\nSolution : {len(path)-1} coups, "
                                f"{len(log)} états explorés.\n")
        self.text.see("end")

        self.busy = True
        self.animate(path, 0)

    def animate(self, path, k):
        self.state = path[k]
        self.refresh()
        if k < len(path) - 1:
            self.root.after(600, self.animate, path, k + 1)
        else:
            self.busy = False
            messagebox.showinfo("Terminé", f"État final atteint en {len(path)-1} coups !")


if __name__ == "__main__":
    root = tk.Tk()
    TaquinApp(root)
    root.mainloop()