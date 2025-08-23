# 👾 NU Generate Challenge (Fall 2025)
**Track 2: Alien Invasion Challenge (Backend)**  

The solution implements a **Breadth-First Search (BFS) with pruning** to explore
possible command sequences and determine the optimal defense strategy.

---

## 🚀 Challenge Overview
Aliens are invading! Each alien has:
- **HP** (health points)
- **ATK** (attack power)

At each turn, the commander (you) can issue one of three commands:

- **`volley`**  
  - Targets `(your HP % number of aliens)` aliens (sorted by descending power).  
  - Deals **1 HP damage** to each target.

- **`focusedVolley`**  
  - Targets **half of the aliens (rounded up)**, sorted by descending power.  
  - Deals **2 HP damage** to each target.

- **`focusedShot`**  
  - Instantly kills the alien with the **highest power**.


## Turn Order
1. **Commander attacks** (apply chosen command).  
2. **Surviving aliens attack** (each deals damage equal to its ATK).  

The invasion ends when:
- Your HP ≤ 0, or  
- All aliens are defeated.  

## Oracle Scoring Priorities
1. **Fewest aliens remaining**  
2. **Highest HP remaining**  
3. **Fewest commands used**  


## Solution Approach
The solution uses **BFS with pruning** to explore all possible command
sequences.  

- **State Representation**  
  Each state tracks:
  - Remaining HP
  - Remaining aliens (sorted by power)
  - Command sequence used so far

- **Pruning**  
  - States are skipped if they are strictly worse than a previously found state.  
  - Alien lists are compared using a greedy **dominance check**.

- **Best State Selection**  
  - Fewer aliens > more HP > fewer commands.
