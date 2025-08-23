import argparse
from client import get_id, get_invasions, submit_challenge, register_challenge
from solver import solve


def run_challenge(email: str, nuid: str):
    print(f"🔗 Registering challenge for {email} ({nuid})...")
    register_challenge(email, nuid)

    challenge_id = get_id(email, nuid)
    print(f"✅ Challenge ID: {challenge_id}")

    invasions = get_invasions(challenge_id)
    print(f"👾 Retrieved {len(invasions)} invasions")

    print("⚡ Solving challenge...")
    solution = solve(invasions)

    result = submit_challenge(solution, challenge_id)
    print("📤 Submission Result:", result)


def main():
    # parser = argparse.ArgumentParser()
    # parser.add_argument("--email", type=str, help="Your Northeastern email")
    # parser.add_argument("--nuid", type=str, help="Your NUID")

    # args = parser.parse_args()

    # email = args.email or input("Enter your Northeastern email: ").strip()
    # nuid = args.nuid or input("Enter your NUID: ").strip()

    email = "kitagawa.e@northeastern.edu"
    nuid = "002777838"
    run_challenge(email, nuid)


if __name__ == "__main__":
    main()