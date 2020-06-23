# Parampreet Singh - 22/06/20
# Panda Library

import pandas as pd
# df = Data Frame

# Read Files
df = pd.read_csv("pokemon_data.csv")  # CSV File
"""
df = pd.read_csv("pokemon_data.csv")  # CSV File
df_xlsx = pd.read_excel("pokemon_data.xlsx")  # Excel File
df_txt = pd.read_csv("pokemon_data.txt", delimiter="\t")  # Text File

print(df.head(3))  # Top three rows
print(df_txt.tail(3))  # Bottom three rows

# Read Headers
print(df.columns)

# Read Columns
print(df[["Name", "Legendary"]])

# Read Rows
print(df.iloc[1:4])  # integer location
for index, row in df.iterrows():
    print(index, row["Name"])

# Locate data in df which has a Type 1 of Fire
print(df.loc[df["Type 1"] == "Fire"])

# Read a specific location (Rows, columns)
print(df.iloc[2, 1])

# Shows high level overview of data (Mean, min, max etc...)
print(df.describe())

# Sorts df
print(df.sort_values("Name"))
# (Type 1 from low to high) and (HP from high to low)
print(df.sort_values(["Type 1", "HP"], ascending=[1, 0]))

# Changing Data
print(df.head(5))
df["Total(A+D)"] = df["Attack"] + df["Defense"]  # Creates new column
print(df.head(5))
print(df.drop(columns=["Total(A+D)"]))  # deletes columns

# Creates a new column from specified rows and columns
# axis=0 vertically, axis=1 horizontally
df["Total"] = df.iloc[:, 4:10].sum(axis=1)
print(df.head(5))

# Save
df.to_csv("modified.csv", index=False)
df.to_csv("modified.txt", index=False, sep="\t")
df.to_excel("modified.xlsx", index=False)


# Filtering Data
print(df.head(3))
print(df.loc[(df["Type 1"] == "Grass") &
             (df["Type 2"] == "Poison") & (df["HP"] > 70)])

print(df.loc[df["Name"].str.contains("Mega")])
print(df.loc[~df["Name"].str.contains("Mega")])  # not = ~

print(df.loc[df["Type 1"].str.contains("Fire|Grass", regex=True)])

# Conditional Changes
df.loc[df["Type 1"] == "Fire", "Type 1"] = "Flamer"
print(df)

# Aggregate Statistics
print(df.groupby(["Type 1"]).mean().sort_values("Attack", ascending=False))
"""
