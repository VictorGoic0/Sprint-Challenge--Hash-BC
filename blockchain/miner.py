import hashlib
import requests

import sys

from uuid import uuid4

from timeit import default_timer as timer

import random


def proof_of_work(last_proof):

    start = timer()

    print("Searching for next proof")
    proof = 0
    last = f'{last_proof}'.encode()
    last_hash = hashlib.sha256(last).hexdigest()
    while valid_proof(last_hash, proof) is False:
        proof += 1

    print("Proof found: " + str(proof) + " in " + str(timer() - start))
    return proof


def valid_proof(last_hash, proof):
    hashing = f'{proof}'.encode()
    hashed_proof = hashlib.sha256(hashing).hexdigest()
    first_6 = [None] * 6
    counter1 = 0
    for i in range(len(hashed_proof)):
        try:
            if int(hashed_proof[i]):
                first_6[counter1] = hashed_proof[i]
                counter1 += 1 
        except:
            continue
        if counter1 == 6:
            break
    last_6 = [None] * 6
    counter2 = 5
    for i in range(len(last_hash)-1, -1, -1):
        try:
            if int(last_hash[i]):
                last_6[counter2] = last_hash[i]
                counter2 -= 1
        except:
            continue
        if counter2 == -1:
            break
    return "".join(first_6) == "".join(last_6)


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "https://lambda-coin.herokuapp.com"

    coins_mined = 0

    # Load or create ID
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()
    if len(id) == 0:
        f = open("my_id.txt", "w")
        # Generate a globally unique ID
        id = str(uuid4()).replace('-', '')
        print("Created new ID: " + id)
        f.write(id)
        f.close()
    # Run forever until interrupted
    while True:
        # Get the last proof from the server
        r = requests.get(url=node + "/last_proof")
        data = r.json()
        new_proof = proof_of_work(data.get('proof'))

        post_data = {"proof": new_proof,
                     "id": id}

        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()
        if data.get('message') == 'New Block Forged':
            coins_mined += 1
            print("Total coins mined: " + str(coins_mined))
        else:
            print(data.get('message'))
