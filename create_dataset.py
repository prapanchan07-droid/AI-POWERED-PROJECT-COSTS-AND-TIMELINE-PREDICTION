import pandas as pd

data = pd.read_csv("data.csv")

# Create realistic features
data["Team_Size"] = (data["Resource_Allocation_Score"] // 2).astype(int)
data["Budget"] = (data["Estimated_Cost_USD"] * 0.8).astype(int)
data["Tools"] = (data["Resource_Allocation_Score"] // 10).astype(int)

# Keep complexity numeric
# (Already exists: Scope_Complexity_Numeric)

# Save new dataset
data.to_csv("enhanced_data.csv", index=False)

print("✅ enhanced_data.csv created successfully")