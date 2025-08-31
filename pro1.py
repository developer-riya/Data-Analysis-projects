# Mobile Phone Price Comparison Project

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Load Excel File
df = pd.read_excel("mobiledataset.xlsx")   # make sure file is in same folder
print("Dataset Loaded\n")
print(df.head())

# Step 2: Data Cleaning
print("\nData Cleaning...")

# check missing values
print("Missing Values:\n", df.isnull().sum())

# fill null values with 0
df.fillna(0, inplace=True)

# remove duplicate rows
df.drop_duplicates(inplace=True)

# fix column names (lower case, no spaces)
df.columns = df.columns.str.strip().str.lower()

# clean price column (remove PKR, commas etc.)
if "launched price (pakistan)" in df.columns:
    df["price"] = (
        df["launched price (pakistan)"]
        .astype(str)
        .str.replace("PKR", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )
    df["price"] = pd.to_numeric(df["price"], errors="coerce")

# create brand column from company name
if "company name" in df.columns:
    df["brand"] = df["company name"].astype(str).str.strip().str.title()

print("Cleaning Done\n")

# Step 3: Basic Analysis
print("Data Analysis\n")

if "price" in df.columns:
    print("Average Price =", round(df["price"].mean(), 2))

if "brand" in df.columns:
    print("Phones per Brand:\n", df["brand"].value_counts())

if "price" in df.columns:
    print("High Price Phones:\n", df[df["price"] > 200000])  

if "price" in df.columns:
    print("Top 5 by Price:\n", df.sort_values(by="price", ascending=False).head())

# Step 4: Visualization

# 1. Bar Chart - phones per brand
if "brand" in df.columns:
    df["brand"].value_counts().plot(kind="bar", color="skyblue", edgecolor="black")
    plt.title("Number of Phones per Brand")
    plt.xlabel("Brand")
    plt.ylabel("Count")
    plt.savefig("brand_bar_chart.png")
    plt.show()

# 2. Scatter Plot - price vs battery
if "price" in df.columns and "battery" in df.columns:
    df["battery"] = pd.to_numeric(df["battery"], errors="coerce")
    sns.scatterplot(x="price", y="battery", data=df, hue="brand")
    plt.title("Price vs Battery")
    plt.xlabel("Price (PKR)")
    plt.ylabel("Battery (mAh)")
    plt.savefig("scatter_price_battery.png")
    plt.show()

# 3. Boxplot - price distribution by brand
if "price" in df.columns and "brand" in df.columns:
    plt.figure(figsize=(10, 6))
    sns.boxplot(x="brand", y="price", data=df)
    plt.xticks(rotation=45)
    plt.title("Price Distribution per Brand")
    plt.xlabel("Brand")
    plt.ylabel("Price (PKR)")
    plt.savefig("boxplot_price_brand.png")
    plt.show()

# 4. Line Chart - avg price by launch year
if "launch year" in df.columns and "price" in df.columns:
    df["launch year"] = pd.to_numeric(df["launch year"], errors="coerce")
    price_trend = df.groupby("launch year")["price"].mean().reset_index()

    plt.figure(figsize=(8, 5))
    sns.lineplot(x="launch year", y="price", data=price_trend, marker="o")
    plt.title("Average Price Trend by Launch Year")
    plt.xlabel("Year")
    plt.ylabel("Avg Price (PKR)")
    plt.grid(True)
    plt.savefig("linechart_price_trend.png")
    plt.show()

# Step 5: Export Cleaned Data
df.to_excel("cleaned_dataset.xlsx", index=False)
print("\nCleaned data saved as cleaned_dataset.xlsx")
