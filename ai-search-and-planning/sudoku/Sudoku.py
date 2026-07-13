import time, csv, random
from tkinter import Tk, Frame, Label, Button, Entry, StringVar, filedialog, messagebox

class SudokuGUI:
    def __init__(self, root):
        root.title("AI Sudoku Solver (Backtracking + MRV + FC)")
        root.resizable(False, False)

        Label(root, text="AI Sudoku Solver", font=("Segoe UI", 18, "bold")).grid(
            row=0, column=0, columnspan=3, pady=(10, 6)
        )

        # ---- Grid ----
        self.grid_frame = Frame(root, bd=2, relief="groove", padx=8, pady=8)
        self.grid_frame.grid(row=1, column=0, padx=12, pady=10)

        self.cells = [[StringVar() for _ in range(9)] for _ in range(9)]
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.given = [[False for _ in range(9)] for _ in range(9)]  # track given numbers

        for r in range(9):
            for c in range(9):
                e = Entry(self.grid_frame, width=2, justify="center",
                          font=("Consolas", 16), textvariable=self.cells[r][c],
                          bd=1, relief="solid")
                pad_x = (4 if c % 3 == 0 else 1, 4 if (c+1) % 3 == 0 else 1)
                pad_y = (4 if r % 3 == 0 else 1, 4 if (r+1) % 3 == 0 else 1)
                e.grid(row=r, column=c, padx=pad_x, pady=pad_y, ipadx=2, ipady=2)
                self.entries[r][c] = e

        # ---- Buttons ----
        self.btn_frame = Frame(root)
        self.btn_frame.grid(row=1, column=1, sticky="n", padx=10)
        Button(self.btn_frame, text="Solve", width=18, command=self.solve).grid(row=0, pady=(0,6))
        Button(self.btn_frame, text="Clear", width=18, command=self.clear_grid).grid(row=1, pady=6)
        Button(self.btn_frame, text="Load from File", width=18, command=self.load_from_file).grid(row=2, pady=6)
        Label(self.btn_frame, text="Method: Backtracking + MRV + Forward Checking", fg="#666").grid(row=3, pady=(8,0))

        # ---- Metrics ----
        self.metrics = {"time": StringVar(value="—"), "bt": StringVar(value="—"), "calls": StringVar(value="—")}
        m = Frame(root, bd=1, relief="sunken", padx=10, pady=8)
        m.grid(row=1, column=2, sticky="n", padx=12)
        Label(m, text="Solver Metrics", font=("Segoe UI", 11, "bold")).grid(row=0, sticky="w")
        Label(m, textvariable=self.metrics["time"]).grid(row=1, sticky="w", pady=(4,0))
        Label(m, textvariable=self.metrics["bt"]).grid(row=2, sticky="w")
        Label(m, textvariable=self.metrics["calls"]).grid(row=3, sticky="w")

        self.recursive_calls = 0
        self.backtracks = 0

    # ---------- GUI Helpers ----------
    def clear_grid(self):
        for r in range(9):
            for c in range(9):
                self.cells[r][c].set("")
                self.entries[r][c].config(fg="black")
                self.given[r][c] = False
        self._reset_metrics()

    def _reset_metrics(self):
        self.recursive_calls = 0
        self.backtracks = 0
        self.metrics["time"].set("Time: —")
        self.metrics["bt"].set("Backtracks: —")
        self.metrics["calls"].set("Recursive Calls: —")

    def load_from_file(self):
        path = filedialog.askopenfilename(title="Select Sudoku .txt or .csv",
                                          filetypes=[("Text/CSV","*.txt *.csv"),("All Files","*.*")])
        if not path: return
        try:
            grid=[]
            if path.lower().endswith(".csv"):
                with open(path, newline="") as f:
                    for row in csv.reader(f):
                        vals=[self._to_int(t) for t in row if t.strip()!=""]
                        if vals: grid.append(vals)
            else:
                with open(path) as f:
                    for line in f:
                        vals=[self._to_int(t) for t in line.replace(","," ").split()]
                        if vals: grid.append(vals)
            if len(grid)!=9 or any(len(r)!=9 for r in grid): raise ValueError("Grid must be 9x9")
            self._reset_metrics()
            for r in range(9):
                for c in range(9):
                    v = grid[r][c]
                    if 1 <= v <= 9:
                        self.cells[r][c].set(str(v))
                        self.entries[r][c].config(fg="#007AFF")  # blue for given
                        self.given[r][c] = True
                    else:
                        self.cells[r][c].set("")
                        self.entries[r][c].config(fg="black")
                        self.given[r][c] = False
        except Exception as e:
            messagebox.showerror("Load Error", f"Could not load puzzle:\n{e}")

    def _to_int(self, t):
        if t in ("0",".","_","-"): return 0
        try:
            v=int(t); return v if 1<=v<=9 else 0
        except: return 0

    def read_grid(self):
        g=[[0]*9 for _ in range(9)]
        for r in range(9):
            for c in range(9):
                t=self.cells[r][c].get().strip()
                if t.isdigit() and 1<=int(t)<=9:
                    g[r][c]=int(t)
                    if not self.given[r][c]:
                        self.given[r][c] = True
                        self.entries[r][c].config(fg="#007AFF")  # mark as given if typed
        return g

    def write_grid(self, grid):
        for r in range(9):
            for c in range(9):
                v = grid[r][c]
                self.cells[r][c].set("" if v==0 else str(v))
                if not self.given[r][c] and v != 0:
                    self.entries[r][c].config(fg="#28A745")  # green for auto-filled

    # ---------- Solver ----------
    def solve(self):
        grid = self.read_grid()
        if not self.is_legal_grid(grid):
            messagebox.showerror("Invalid Puzzle","Initial grid violates Sudoku rules."); return
        self._reset_metrics()
        start = time.perf_counter()
        solved = self.bt_mrv_fc(grid)
        ms = (time.perf_counter()-start)*1000.0
        if solved: self.write_grid(grid)
        else: messagebox.showinfo("No Solution","This puzzle has no valid solution.")
        self.metrics["time"].set(f"Time: {ms:.2f} ms")
        self.metrics["bt"].set(f"Backtracks: {self.backtracks}")
        self.metrics["calls"].set(f"Recursive Calls: {self.recursive_calls}")

    def bt_mrv_fc(self, grid):
        self.recursive_calls += 1
        pos, dom = self.select_mrv_with_domain(grid)
        if pos is None: return True
        if not dom:
            self.backtracks += 1
            return False

        r, c = pos
        random.shuffle(dom)
        for v in dom:
            if self.is_safe(grid, r, c, v):
                grid[r][c] = v
                if not self.forward_check_failure(grid, r, c):
                    if self.bt_mrv_fc(grid):
                        return True
                grid[r][c] = 0
                self.backtracks += 1
        return False

    # ---------- CSP Helpers ----------
    def select_mrv_with_domain(self, grid):
        best_pos, best_dom, best_size = None, None, 10
        for r in range(9):
            for c in range(9):
                if grid[r][c]==0:
                    dom=self.legal_values(grid,r,c)
                    if len(dom)<best_size:
                        best_size=len(dom); best_pos=(r,c); best_dom=dom
        return (None,None) if best_pos is None else (best_pos,best_dom)

    def legal_values(self, grid, r, c):
        used=set(grid[r][x] for x in range(9) if grid[r][x]!=0)
        used.update(grid[x][c] for x in range(9) if grid[x][c]!=0)
        br,bc=(r//3)*3,(c//3)*3
        for i in range(br,br+3):
            for j in range(bc,bc+3):
                if grid[i][j]!=0: used.add(grid[i][j])
        return [v for v in range(1,10) if v not in used]

    def is_safe(self, grid, r, c, v):
        if any(grid[r][x]==v for x in range(9)): return False
        if any(grid[x][c]==v for x in range(9)): return False
        br,bc=(r//3)*3,(c//3)*3
        for i in range(br,br+3):
            for j in range(bc,bc+3):
                if grid[i][j]==v: return False
        return True

    def forward_check_failure(self, grid, r, c):
        peers=set()
        peers.update((r,cc) for cc in range(9) if cc!=c)
        peers.update((rr,c) for rr in range(9) if rr!=r)
        br,bc=(r//3)*3,(c//3)*3
        peers.update((i,j) for i in range(br,br+3) for j in range(bc,bc+3) if not (i==r and j==c))
        for rr,cc in peers:
            if grid[rr][cc]==0 and len(self.legal_values(grid,rr,cc))==0:
                return True
        return False

    def is_legal_grid(self, g):
        for r in range(9):
            row=[v for v in g[r] if v!=0]
            if len(row)!=len(set(row)): return False
        for c in range(9):
            col=[g[r][c] for r in range(9) if g[r][c]!=0]
            if len(col)!=len(set(col)): return False
        for br in range(0,9,3):
            for bc in range(0,9,3):
                blk=[]
                for i in range(br,br+3):
                    for j in range(bc,bc+3):
                        v=g[i][j]
                        if v!=0: blk.append(v)
                if len(blk)!=len(set(blk)): return False
        return True

# ---- Run ----
def main():
    root = Tk()
    SudokuGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()