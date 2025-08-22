from client import get_id, get_invasions, submit_challenge, register_challenge
from solver import solve

EMAIL = "kitagawa.e@northeastern.edu"
NUID = "002777838"

def main():
    register_challenge(EMAIL, NUID)
    challenge_id = get_id(EMAIL, NUID)
    invasions = get_invasions(challenge_id)
    
    solution = solve(invasions)
    result = submit_challenge(solution, challenge_id)

    print("Submission Result:", result)


if __name__ == "__main__":
    main()
