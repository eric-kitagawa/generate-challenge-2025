from collections import deque
from math import ceil


def solve(challenge):
    solution = [bfs_solve(invasion) for invasion in challenge]
    return solution


def bfs_solve(invasion):
    challenge_id, hp, invasion = invasion['challengeID'], invasion['hp'], invasion['aliens']
    commands = []
    visited = set()
    best_result = None

    queue = deque()
    queue.append((hp, invasion, commands))

    while queue:
        hp, invasion, commands = queue.popleft()

        # Step 1: Check if this state was visited
        key = (hp, tuple((a["hp"], a["atk"]) for a in invasion))
        if key in visited:
            continue
        visited.add(key)

        # Step 2: Check if gameover
        if hp <= 0 or all(a["hp"] <= 0 for a in invasion):
            if best(hp, invasion, commands, best_result):
                best_result = (hp, invasion, commands)
            continue
        
        # Step 3: Apply turn
        for command in ["volley", "focusedVolley", "focusedShot"]:
            new_invasion = [dict(a) for a in invasion]
            if command == "volley":
                num_of_targets = hp % len(new_invasion)
                for i in range(num_of_targets):
                    new_invasion[i]["hp"] -= 1

            elif command == "focusedVolley":
                num_of_targets = ceil(len(new_invasion) / 2)
                for i in range(num_of_targets):
                    new_invasion[i]["hp"] -= 2

            elif command == "focusedShot":
                new_invasion[0]["hp"] = 0

            new_invasion = [dict(a) for a in new_invasion if a["hp"] > 0]
            new_invasion = sorted(
                new_invasion,
                key=lambda a: (-(a["hp"] + a["atk"]), a["hp"])
            )

            alien_atk = sum(a["atk"] for a in new_invasion)
            new_hp = hp - alien_atk
            new_commands = commands + [command]

            queue.append((new_hp, new_invasion, new_commands))

    return {
        "challengeID": challenge_id,
        "state": {
            "remainingHP": best_result[0],
            "remainingAliens": len(best_result[1]),
            "commands": best_result[2]
        }
    }
        


def best(hp, invasion, commands, best_result):
    if not best_result:
        return True
    
    best_hp, best_invasion, best_commands = best_result

    if len(invasion) < len(best_invasion):
        return True
    if len(invasion) == len(best_invasion) and hp > best_hp:
        return True
    if len(invasion) == len(best_invasion) and hp == best_hp and len(commands) < len(best_commands):
        return True
    
    return False
