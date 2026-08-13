import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("../datasets/Indian_ecommerce_sales_raw.csv")
df.info()
df.describe(include="all").T
df.isnull().sum()

duplicate_count = df.duplicated().sum()

print("Duplicate rows:", duplicate_count)

df = df.drop_duplicates().copy()

print("Rows after removing duplicates:", len(df))
df["Order_Date"] = pd.to_datetime(df["Order_Date"])

print(df["Order_Date"].dtype)

df["Year"] = df["Order_Date"].dt.year
df["Month"] = df["Order_Date"].dt.month
df["Month_Name"] = df["Order_Date"].dt.month_name()
df["Quarter"] = df["Order_Date"].dt.quarter

print(df.isnull().sum())
df["Customer_Rating"] = df["Customer_Rating"].fillna(
    df["Customer_Rating"].median()
)
df["Delivery_Days"] = df["Delivery_Days"].fillna(
    df["Delivery_Days"].median()
)
df["Payment_Method"] = df["Payment_Method"].fillna(
    df["Payment_Method"].mode()[0]
)
print("Negative sales:", (df["Sales_INR"] < 0).sum())
print("Negative profit:", (df["Profit_INR"] < 0).sum())
print("Invalid quantity:", (df["Quantity"] <= 0).sum())
print("Invalid discount:", ((df["Discount_Pct"] < 0) | 
                            (df["Discount_Pct"] > 100)).sum())
print("Invalid rating:", ((df["Customer_Rating"] < 1) | 
                          (df["Customer_Rating"] > 5)).sum())
df["Calculated_Sales"] = (
    df["Unit_Price_INR"] *
    df["Quantity"] *
    (1 - df["Discount_Pct"] / 100)
)
df["Sales_Difference"] = (
    df["Sales_INR"] - df["Calculated_Sales"]
).abs()

print(df["Sales_Difference"].max())

df.drop(
    columns=["Calculated_Sales", "Sales_Difference"],
    inplace=True
)
df["Profit_Margin_Pct"] = (
    df["Profit_INR"] / df["Sales_INR"] * 100
).round(2)

df["Order_Month"] = df["Order_Date"].dt.to_period("M").astype(str)

df["Actual_Unit_Selling_Price"] = (
    df["Sales_INR"] / df["Quantity"]
).round(2)
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())

df.to_csv(
    "indian_ecommerce_sales_cleaned.csv",
    index=False
)

print("Cleaned dataset saved successfully!")