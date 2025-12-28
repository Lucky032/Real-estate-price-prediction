import pandas as pd
import os

print("Merging year-wise Excel files...")

data_folder = "data"
all_files = os.listdir(data_folder)
print("Files found:", all_files)

df_list = []

for file in all_files:
    file_path = os.path.join(data_folder, file)
    df = pd.read_excel(file_path)

    # Drop unwanted column
    if "S.No" in df.columns:
        df.drop(columns=["S.No"], inplace=True)

    # Rename columns (MATCHING YOUR EXCEL)
    df.rename(columns={
        "Property Type": "Property_Type",
        "Size (Sq Ft)": "Size_sqft",
        "Average Price (INR)": "Price_INR"
    }, inplace=True)

    # Add Year column from filename
    year = file.replace(".xlsx", "")
    df["Year"] = int(year)

    df_list.append(df)

# Merge all years
final_df = pd.concat(df_list, ignore_index=True)

# Clean Price column
final_df["Price_INR"] = final_df["Price_INR"].astype(str)
final_df["Price_INR"] = final_df["Price_INR"].str.replace("₹", "").str.replace(",", "")
final_df["Price_INR"] = final_df["Price_INR"].astype(float)

# Clean Size column
final_df["Size_sqft"] = final_df["Size_sqft"].astype(str)
final_df["Size_sqft"] = final_df["Size_sqft"].str.replace("Sq Ft", "").str.replace("sq ft", "")
final_df["Size_sqft"] = final_df["Size_sqft"].astype(float)

final_df.dropna(inplace=True)

# Save clean data
final_df.to_excel("clean_real_estate_data.xlsx", index=False)

print("clean_real_estate_data.xlsx CREATED SUCCESSFULLY ✅")
print("Final columns:", final_df.columns.tolist())
print("Total rows:", len(final_df))
