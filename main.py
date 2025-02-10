import requests
import json

import numpy as np
import matplotlib.pyplot as plt
import random
from scipy.spatial import distance

token = input("Enter the token address:")


url = 'https://solana.drpc.org'
headers = {
    'Content-Type': 'application/json'
}

data = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "getTokenLargestAccounts",
    "params": [token]
}

response = requests.post(url, headers=headers, data=json.dumps(data))

if response.status_code != 200:
    exit()
accounts = response.json()['result']['value']

addr = []
balances = []
for account in accounts:
    addr.append(account['address'])
    balances.append(account['uiAmount'])
total = sum(balances)
relative_sizes = np.array(balances) / total

max_radi = 10
radii = np.sqrt(relative_sizes)*max_radi

pos = []
for r in radii:
    placed=False
    while not placed:
        x, y = random.uniform(-15, 15), random.uniform(-15, 15)
        if all(distance.euclidean((x, y), (px, py)) > (r + pr) for (px, py, pr) in pos):
            pos.append((x, y, r))
            placed = True



# Create figure and axis
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(-20, 20)
ax.set_ylim(-20, 20)
ax.set_aspect('equal')
ax.set_xticks([])
ax.set_yticks([])

# Store circle patches and labels
circles = []
labels = []

# Draw each circle
for (x, y, r), holder, balance in zip(pos, addr, balances):
    color = np.random.rand(3,)
    circle = plt.Circle((x, y), r, color=color, alpha=0.6, ec="black", picker=True)
    ax.add_patch(circle)
    circles.append((circle, (x, y, r), holder, balance))
    formatted_balance = f"{balance:,}"
    # Create label (initially hidden)
    label = ax.text(x, y, f"{holder}\n{formatted_balance}", ha='center', va='center',
                    fontsize=12, color="black", visible=False, bbox=dict(facecolor='white', alpha=0.7))
    labels.append(label)

# Click event handler
def on_pick(event):
    for i, (circle, (x, y, r), holder, balance) in enumerate(circles):
        if event.artist == circle:
            labels[i].set_visible(not labels[i].get_visible())  # Toggle visibility
        else:
            labels[i].set_visible(False)  # Hide others
    fig.canvas.draw()

# Connect event to figure
fig.canvas.mpl_connect('pick_event', on_pick)

plt.title("Click on a Circle to See Balance & Name")
plt.show()