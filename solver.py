from dataclasses import dataclass
from collections import deque
from math import ceil

@dataclass
class State:
    hp: int
    invasion: list
    commands: list
    

def solve(challenge):
    solution = [bfs_solve(invasion) for invasion in challenge]
    return solution


def bfs_solve(challenge):
    """
    Solve a single challenge using BFS with pruning.
    Returns the best outcome (max HP, fewest aliens, shortest command sequence).
    """
    state = State(
        hp=challenge['hp'],
        invasion=challenge['aliens'],
        commands=[],
    )
    challenge_id = challenge['challengeID']
    visited = set()
    best_result = None

    queue = deque()
    queue.append(state)

    while queue:
        turn = queue.popleft()

        # Step 1: Check if visited already
        key = (turn.hp, tuple((a["hp"], a["atk"]) for a in turn.invasion))
        if key in visited:
            continue
        visited.add(key)

        # Step 2: Check if our best state dominates
        if can_prune(turn, best_result):
            continue

        # Step 2.5: Check if gameover
        if turn.hp <= 0 or not turn.invasion:
            if best(turn, best_result):
                best_result = State(turn.hp, turn.invasion, turn.commands)
            continue
        
        # Step 3: Create all new possibilites and add to queue
        turn_outcomes = apply_moves(turn)
        queue.extend(turn_outcomes)

    return {
        "challengeID": challenge_id,
        "state": {
            "remainingHP": best_result.hp,
            "remainingAliens": len(best_result.invasion),
            "commands": best_result.commands
        }
    }


def apply_moves(state):
    """Creates three possible states with volley, focusedVolley, and focusedShot and adds to queue"""
    outcomes = []
    for command, func in COMMANDS.items():
        new_invasion = [dict(a) for a in state.invasion]
        func(new_invasion, state.hp)
        remaining_aliens = sorted(
            (a for a in new_invasion if a["hp"] > 0),
            key=lambda a: (-(a["hp"] + a["atk"]), a["hp"])
            )

        new_hp = state.hp - sum(a["atk"] for a in remaining_aliens)
        new_commands = state.commands + [command]

        outcome = State(new_hp, remaining_aliens, new_commands)
        outcomes.append(outcome)

    return outcomes


def cmd_volley(invasion, hp):
    """
    Damages a set amount of aliens by 1 hp by descending power.
    Target amount is hp modulo invasion
    """
    num_of_targets = hp % len(invasion)
    for i in range(num_of_targets):
        invasion[i]["hp"] -= 1


def cmd_focused_volley(invasion, hp):
    """
    Damages a set amount of aliens by 2 hp by descending power,
    Target amount is half of invasion rounded up
    """
    num_of_targets = ceil(len(invasion) / 2)
    for i in range(num_of_targets):
        invasion[i]["hp"] -= 2


def cmd_focused_shot(invasion, hp):
    invasion[0]["hp"] = 0


COMMANDS = {
    "volley": cmd_volley,
    "focusedVolley": cmd_focused_volley,
    "focusedShot": cmd_focused_shot,
}

def best(state, best_result):
    """Return True if this state is better than current best"""
    if not best_result:
        return True
    if len(state.invasion) < len(best_result.invasion):
        return True
    if len(state.invasion) == len(best_result.invasion) and state.hp > best_result.hp:
        return True
    if (len(state.invasion) == len(best_result.invasion) 
        and state.hp == best_result.hp 
        and len(state.commands) < len(best_result.commands)
        ):
        return True
    
    return False

def can_prune(state, best_result):
    if not best_result:
        return False

    if invasion_dominates(state.invasion, best_result.invasion):
        if state.hp < best_result.hp:
            return True
        if state.hp == best_result.hp and len(state.commands) > len(best_result.commands):
            return True

    return False

def invasion_dominates(inv1, inv2):
    """
    Return True if inv1 is at least as strong as inv2 for every alien
    NOTE: This func uses greedy (there might be edge cases this doesnt work)
    """
    if len(inv1) < len(inv2):
        return False

    i, j = 0, 0
    while j < len(inv2) and i < len(inv1):
        if (inv1[i]["hp"] >= inv2[j]["hp"] and
            inv1[i]["atk"] >= inv2[j]["atk"]):
            j += 1
        i += 1

    return j == len(inv2)
