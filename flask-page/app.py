from flask import Flask, request, jsonify, send_file
from client import get_id, get_invasions, submit_challenge, register_challenge
from solver import solve

app = Flask(__name__)

@app.route("/")
def index():
    return send_file("index.html")

@app.route("/run", methods=["POST"])
def run_challenge():
    data = request.json
    email, nuid = data["email"], data["nuid"]

    register_challenge(email, nuid)
    challenge_id = get_id(email, nuid)
    invasions = get_invasions(challenge_id)
    solution = solve(invasions)
    result = submit_challenge(solution, challenge_id)

    return jsonify(result)


if __name__ == "__main__":
    app.run()