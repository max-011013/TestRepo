import pandas as pd

df = pd.read_csv("Untitled spreadsheet - Sheet1.csv")
df.to_json("BJWholesaleClub.json", indent=2, orient="records")