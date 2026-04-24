import pandas as pd
import random

data = []

for _ in range(2000):
    team = random.randint(1, 50)
    budget = random.randint(100000, 10000000)
    tools = random.randint(1, 10)
    complexity = random.randint(1, 3)  # 1=Low, 2=Medium, 3=High

    cost = (
        budget * 0.6 +
        team * 20000 +
        tools * 15000 +
        complexity * 100000
    )

    time = (
        500 +
        complexity * 150 -
        team * 5 -
        tools * 10
    )


    time = max(30, int(time))

    data.append([team, budget, tools, complexity, int(cost), int(time)])

df = pd.DataFrame(data, columns=[
    "Team_Size", "Budget", "Tools", "Complexity", "Cost", "Time"
])

df.to_csv("final_dataset.csv", index=False)

print("✅ final_dataset.csv created")