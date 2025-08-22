import requests

URL = "https://challenge.generatenu.com/api/v1"

def register_challenge(email, nuid):
    response = requests.post(
        f"{URL}/member/register", 
        json={
            "email": email,
            "nuid": nuid
            })
    return response.json()


def get_id(email, nuid):
    response = requests.get(
        f"{URL}/member?email={email}&nuid={nuid}"
    )
    data = response.json()
    id = data["id"]
    return id


def get_invasions(challenge_id):
    response = requests.get(
        f"{URL}/challenge/backend/{challenge_id}/aliens"
    )
    return response.json()


def submit_challenge(solution, id):
    url = f"{URL}/challenge/backend/{id}/aliens/submit"
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=solution, headers=headers)

    return response.json()