# Gridworld

A small, dependency‑free Python implementation of **GridWorld** — the classic reinforcement‑learning
playground where an agent lives on a grid of cells. Some cells hold **rewards**, some are **walls**, and
you can even wire up **"jump" edges** that teleport the agent across the board.

You build a world entirely from the **command line** using a compact set of *directives* (single‑letter
commands like `G`, `V`, and `E`). The program then prints three things:

1. an **ASCII map of the grid** — showing which cells connect to which,
2. the **rewards** you placed (on cells and on edges), and
3. an **optimal policy** — the best direction to move from every cell.

Everything runs on plain **Python 3**. There is nothing to install.

---

## Table of contents

- [Quick start](#quick-start)
- [How cells are numbered](#how-cells-are-numbered)
- [The two solvers](#the-two-solvers)
- [Directives — building a world (`RLDP.py`)](#directives--building-a-world-rldppy)
  - [`G` — the graph (the board)](#g--the-graph-the-board)
  - [`V` — vertices: rewards, walls, terminals](#v--vertices-rewards-walls-terminals)
  - [`E` — edges: custom links and jumps](#e--edges-custom-links-and-jumps)
  - [Slice syntax for naming cells](#slice-syntax-for-naming-cells)
- [Simpler syntax (`RLSetup.py`)](#simpler-syntax-rlsetuppy)
- [How the grid is printed](#how-the-grid-is-printed)
  - [Alphabet 1 — the graph structure](#alphabet-1--the-graph-structure)
  - [Alphabet 2 — the policy](#alphabet-2--the-policy)
- [How the solvers reason](#how-the-solvers-reason)
- [Worked examples](#worked-examples)
- [Repository layout](#repository-layout)

---

## Quick start

```bash
# A 4x4 grid (16 cells) with a reward on cell 15, solved by dynamic programming:
python RLDP.py G16 V15R

# The same idea with the BFS solver and its simpler syntax:
python RLSetup.py 16 G0 R15
```

Typical output (the BFS run above):

```
SSSD
SSSD
SSSD
RRR*
```

Read as: the goal `*` is the bottom‑right cell, and every other cell is told which way to move toward
it — `R` = right, `D` = down, `S` = "right or down are equally good" (see the
[policy alphabet](#alphabet-2--the-policy)).

---

## How cells are numbered

Cells are numbered **`0 … size‑1`**, left‑to‑right then top‑to‑bottom:

```
 0  1  2  3
 4  5  6  7
 8  9 10 11
12 13 14 15
```

If you don't specify a **width** (cells per row), one is chosen automatically: the smallest factor of
`size` that is ≥ √size. So `16 → 4 wide`, `12 → 4 wide`, `9 → 3 wide`, and a prime `size` falls back to a
single row.

---

## The two solvers

The repo ships two independent programs that solve the same kind of world in different ways:

| File | Solver | How it thinks | Syntax |
|------|--------|---------------|--------|
| **`RLDP.py`** | **Dynamic programming** (policy / value iteration) | Repeatedly re‑estimates the *value* of every cell (discounted, `γ ≈ 0.99`) and greedily picks the best move, until the policy stops changing. | Full directive language — jumps, edge rewards, directed edges, per‑cell rewards. |
| **`RLSetup.py`** | **Breadth‑first search** | Runs a multi‑source BFS *outward from the reward cells*, recording each cell's distance to the nearest reward, then points every cell down the shortest path. | Simpler positional tokens. |

Use `RLDP.py` for the full feature set; `RLSetup.py` is the lighter, shortest‑path variant.

---

## Directives — building a world (`RLDP.py`)

A world is just a sequence of space‑separated tokens. **Each token is one directive.** They are applied
left to right, so later directives can modify what earlier ones built.

### `G` — the graph (the board)

```
G[type]<size>[W<width>][R<defaultReward>]
```

| Part | Meaning |
|------|---------|
| `<size>` | **Required.** Number of cells. |
| `type` | Omit for a normal grid. `N` = *non‑grid* graph with no geometry (a `size` of `0` also forces this). `G` = grid (explicit). |
| `W<width>` | Cells per row. Optional — auto‑computed if omitted. |
| `R<defaultReward>` | The value used whenever you later write `R` with no number. Defaults to `12`. |

Examples: `G16` · `G16W4` · `G20W5R30`

### `V` — vertices: rewards, walls, terminals

```
V<cells>[R[value]][B][T]
```

* **`<cells>`** — which cells, written as [slices](#slice-syntax-for-naming-cells).
* **`R`** — give these cells a **reward** (the graph default), or `R25` for a specific value. A reward
  cell is a **goal** the agent wants to reach.
* **`B`** — **toggle a wall** on these cells. This is a *toggle*, not a one‑way switch: the first `B`
  cuts every edge between the cell and its neighbours (isolating it); a **second `B` on the same cell
  restores those edges**. Handy for turning obstacles on and off.
* **`T`** — mark the cells as **terminal**.

Examples:
`V15R` (default reward on cell 15) · `V15R25` (reward 25 on cell 15) ·
`V5,6B` (wall off cells 5 and 6) · `V0:4R10` (reward 10 on cells 0,1,2,3).

> **Note on the wall toggle.** Because `B` toggles, `V5B` builds a wall at cell 5, while `V5B V5B` in the
> same command leaves the grid unchanged — the wall is added and then removed.

### `E` — edges: custom links and jumps

Edges let you rewire the board: remove connections, make one‑way streets, or create **jumps**
(teleports) between distant cells. Every `E` directive begins with an optional **management symbol**:

| Symbol | Action |
|:------:|--------|
| `+` | add the edge |
| `!` | remove the edge |
| `~` | **toggle** the edge — *this is also the default when no symbol is given* |
| `*` | add the edge **and** set its reward |
| `@` | only set the reward on an existing edge |

There are two ways to name the edge:

**Form 1 — connect specific cells (this is how you make a jump / teleport):**

```
E<mgmt><cellsA><link><cellsB>[R[value]]
```

* `<link>` is `=` for a **two‑way** edge, or `~` for a **one‑way** (directed) edge.
* `R[value]` attaches a **reward to the edge itself** — the agent collects it whenever it traverses that
  edge. This is what makes a long jump worth taking.

Example: `E*0=15R5` — add a **two‑way jump** between cells 0 and 15 worth **5**.

**Form 2 — connect by compass direction:**

```
E<mgmt><cells><directions><link>[R[value]]
```

* `<directions>` is any mix of `N E S W` (north / east / south / west).

Example: `E0ES~` — from cell 0, toggle the edges heading **East** and **South** as one‑way links.

### Slice syntax for naming cells

Anywhere cells are named, you can use Python‑style list slices, comma‑separated:

| You write | You get |
|-----------|---------|
| `3` | just cell 3 |
| `0:4` | cells 0, 1, 2, 3 |
| `0:10:2` | cells 0, 2, 4, 6, 8 (step 2) |
| `2,5,9` | those three cells |
| `::-1` | all cells, reversed (negative steps allowed) |

---

## Simpler syntax (`RLSetup.py`)

`RLSetup.py` uses positional tokens instead of the full directive language:

| Token | Meaning |
|-------|---------|
| `<size>` | number of cells, e.g. `16` |
| `G0` / `G1` | choose the solver mode |
| `R<cell>` | default reward on a cell, e.g. `R15` |
| `R<cell>:<value>` | reward with a specific value, e.g. `R15:30` |
| `R:<value>` | change the default reward value |
| `B<cells>` | **toggle walls** on cells, e.g. `B5` or `B5,6` (same toggle behaviour as `RLDP.py`) |
| `B<cell><dirs>` | remove a cell's edges in specific compass directions, e.g. `B5NE` |

Example: `python RLSetup.py 16 G0 R15 B5,6`

---

## How the grid is printed

Output is a picture the same shape as the grid — one character per cell. **Two different alphabets** are
used depending on what is being shown. In both, the four "bits" for a cell are read in the order
**East, West, South, North**.

### Alphabet 1 — the graph structure

Printed under `Graph:` (by `RLDP.py`). Each character shows **which of a cell's four neighbours it is
connected to** — think box‑drawing / pipe characters.

```
Graph:
rvv7
>++<
>++<
L^^J
```

| Char | Connects to | Shape |
|:----:|-------------|-------|
| `+` | E W S N | 4‑way crossroads |
| `-` | E W | horizontal pass‑through |
| `\|` | S N | vertical pass‑through |
| `^` | E W N | T opening up |
| `v` | E W S | T opening down |
| `<` | W S N | T opening left |
| `>` | E S N | T opening right |
| `L` | E N | corner |
| `J` | W N | corner |
| `r` | E S | corner |
| `7` | W S | corner |
| `N` | N only | dead‑end open north |
| `E` | E only | dead‑end open east |
| `S` | S only | dead‑end open south |
| `W` | W only | dead‑end open west |
| `.` | nothing | isolated cell / wall |

If any jumps exist, a `Jumps:` line is printed underneath, listing them (`=` two‑way, `~` one‑way).

### Alphabet 2 — the policy

Printed by `RLSetup.py`, and as the optimal policy from `RLDP.py`. Each character shows **which
direction(s) the agent should move** from that cell. The single‑direction letters are the intuitive ones:

| Char | Move | | Char | Move |
|:----:|------|---|:----:|------|
| `R` | → East (right) | | `L` | ← West (left) |
| `D` | ↓ South (down) | | `U` | ↑ North (up) |
| `*` | this cell **is** a reward / goal | | `.` | wall or unreachable |

When several moves are equally good, one combined character marks the tie:

| Char | Tied moves | Char | Tied moves |
|:----:|-----------|:----:|-----------|
| `-` | E + W | `\|` | S + N |
| `S` | E + S | `V` | E + N |
| `E` | W + S | `M` | W + N |
| `T` | E + W + S | `W` | E + S + N |
| `N` | E + W + N | `F` | W + S + N |
| `+` | all four | | |

---

## How the solvers reason

**`RLDP.py` — dynamic programming.** Every cell starts at value 0 (reward cells start at their reward
value). The value of a cell is repeatedly recomputed as the **discounted average value of the cells its
policy can move to** (`γ ≈ 0.99`); when a rewarding *edge* is used, its reward is added in. A value pass
and a "pick the greediest neighbour" policy pass alternate — this is **policy iteration** — until the
policy stops changing. Cells that settle at value ≤ 0 are given an empty policy (nowhere worth going).
The program then prints the valuation and the optimal policy as the set of best moves per cell.

**`RLSetup.py` — breadth‑first search.** Rather than iterating values, it runs a **multi‑source BFS
starting from the reward cells** and records each cell's distance to the nearest reward. The best move
from any cell is simply the neighbour with the smallest distance (walls and lesser rewards are excluded).
That yields the shortest‑path policy directly, rendered with the policy alphabet above.

---

## Worked examples

**1. Reward in the corner (BFS).**

```bash
$ python RLSetup.py 16 G0 R15
SSSD
SSSD
SSSD
RRR*
```

Every cell steers toward the goal at 15: interior cells can go right *or* down (`S`), the right column
goes down (`D`), the bottom row goes right (`R`).

**2. Add a wall, then solve (BFS).**

```bash
$ python RLSetup.py 16 G0 R15 B5
SRSD
D.SD
SSSD
RRR*
```

Cell 5 is now a wall (`.`), and its neighbours route around it.

**3. A jump with an edge reward (DP).**

```bash
$ python RLDP.py G16 "E*0=15R5"
Graph:
rvv7
>++<
>++<
L^^J
Jumps: 0=15;0~15
Rewards:
{'rwd': 12, 'width': 4}
(0,15): rwd:5
```

A two‑way jump now links cells 0 and 15, worth 5 to traverse.

---

## Repository layout

| File | Purpose |
|------|---------|
| `RLDP.py` | **Main solver** — full directive language + dynamic‑programming policy. |
| `RLSetup.py` | Alternative solver — simpler syntax + BFS shortest‑path policy. |
| `RLBandits.py` | Standalone UCB1 multi‑armed bandit (unrelated to the grid). |
| `RL2Monte.py`, `RLMonte2.py` | Experimental Monte‑Carlo policy sketches (work in progress). |
| `newBfs.py` | A small BFS helper / sketch. |
| `mnist_test.csv` | Unrelated dataset left in the repo. |

---

*Author: Ashwin Pulla, 2024.* (READ ME WAS MADE WITH AI CODE WAS NOT. CODE WAS ENTIRELY CREATED BY ME ASHWIN PULLA)
