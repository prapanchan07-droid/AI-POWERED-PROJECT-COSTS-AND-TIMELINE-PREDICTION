import pandas as pd
from sklearn.ensemble import RandomForestRegressor

data = pd.read_csv("final_dataset.csv")

X = data[["Team_Size", "Budget", "Tools", "Complexity"]]

y_cost = data["Cost"]
y_time = data["Time"]

model_cost = RandomForestRegressor()
model_time = RandomForestRegressor()

model_cost.fit(X, y_cost)
model_time.fit(X, y_time)

def predict_project(team, budget, tools, complexity):
    input_df = pd.DataFrame({
        "Team_Size": [team],
        "Budget": [budget],
        "Tools": [tools],
        "Complexity": [complexity]
    })

    cost = model_cost.predict(input_df)[0]
    time = model_time.predict(input_df)[0]

    return cost, time