import pandas as pd

# Load cleaned dataset
df = pd.read_csv(
    r"D:\Indian-Ecommerce-Sales-Analytics\datasets\indian_ecommerce_sales_cleaned.csv"
)

print("Dataset loaded successfully!")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

print("\nFirst 5 rows:")
print(df.head())

print("\n========== DATA QUALITY CHECK ==========")

print("\nDataset Information:")
df.info()

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:", df.duplicated().sum())

# ==============================
# BUSINESS KPIs
# ==============================

total_revenue = df["Sales_INR"].sum()
total_profit = df["Profit_INR"].sum()
total_orders = df["Order_ID"].nunique()
total_customers = df["Customer_ID"].nunique()
total_units = df["Quantity"].sum()

profit_margin = (total_profit / total_revenue) * 100

print("\n========== BUSINESS KPIs ==========")
print(f"Total Revenue: ₹{total_revenue:,.2f}")
print(f"Total Profit: ₹{total_profit:,.2f}")
print(f"Total Orders: {total_orders:,}")
print(f"Total Customers: {total_customers:,}")
print(f"Total Units Sold: {total_units:,}")
print(f"Profit Margin: {profit_margin:.2f}%")

# ==============================
# MONTHLY SALES TREND
# ==============================

df["Order_Date"] = pd.to_datetime(df["Order_Date"])

monthly_sales = (
    df.groupby(df["Order_Date"].dt.to_period("M"))
    .agg(
        Revenue=("Sales_INR", "sum"),
        Profit=("Profit_INR", "sum"),
        Orders=("Order_ID", "nunique")
    )
    .reset_index()
)

monthly_sales["Order_Date"] = monthly_sales["Order_Date"].astype(str)

print("\n========== MONTHLY SALES ==========")
print(monthly_sales.to_string(index=False))

import matplotlib.pyplot as plt

plt.figure(figsize=(14, 6))

plt.plot(
    monthly_sales["Order_Date"],
    monthly_sales["Revenue"],
    marker="o"
)

plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue (INR)")
plt.xticks(rotation=45)
plt.tight_layout()

plt.show()
# Highest revenue month
highest_month = monthly_sales.loc[
    monthly_sales["Revenue"].idxmax()
]

# Lowest revenue month
lowest_month = monthly_sales.loc[
    monthly_sales["Revenue"].idxmin()
]

print("\n========== SALES TREND INSIGHTS ==========")

print(
    f"Highest Revenue Month: "
    f"{highest_month['Order_Date']} "
    f"(₹{highest_month['Revenue']:,.2f})"
)

print(
    f"Lowest Revenue Month: "
    f"{lowest_month['Order_Date']} "
    f"(₹{lowest_month['Revenue']:,.2f})"
)
# ==============================
# YEAR-OVER-YEAR ANALYSIS
# ==============================

yearly_sales = (
    df.groupby("Year")
    .agg(
        Revenue=("Sales_INR", "sum"),
        Profit=("Profit_INR", "sum"),
        Orders=("Order_ID", "nunique"),
        Units=("Quantity", "sum")
    )
    .reset_index()
)

yearly_sales["Profit_Margin"] = (
    yearly_sales["Profit"] /
    yearly_sales["Revenue"] * 100
)

print("\n========== YEARLY PERFORMANCE ==========")
print(yearly_sales.to_string(index=False))


# ==============================
# YEAR-OVER-YEAR GROWTH
# ==============================

revenue_growth = (
    (yearly_sales.loc[1, "Revenue"] -
     yearly_sales.loc[0, "Revenue"])
    / yearly_sales.loc[0, "Revenue"]
) * 100

profit_growth = (
    (yearly_sales.loc[1, "Profit"] -
     yearly_sales.loc[0, "Profit"])
    / yearly_sales.loc[0, "Profit"]
) * 100

orders_growth = (
    (yearly_sales.loc[1, "Orders"] -
     yearly_sales.loc[0, "Orders"])
    / yearly_sales.loc[0, "Orders"]
) * 100

print("\n========== GROWTH ANALYSIS ==========")
print(f"Revenue Growth: {revenue_growth:.2f}%")
print(f"Profit Growth: {profit_growth:.2f}%")
print(f"Orders Growth: {orders_growth:.2f}%")
# ==============================
# CATEGORY PERFORMANCE
# ==============================

category_analysis = (
    df.groupby("Category")
    .agg(
        Revenue=("Sales_INR", "sum"),
        Profit=("Profit_INR", "sum"),
        Units=("Quantity", "sum"),
        Orders=("Order_ID", "nunique")
    )
    .reset_index()
)

category_analysis["Profit_Margin"] = (
    category_analysis["Profit"] /
    category_analysis["Revenue"] * 100
)

category_analysis = category_analysis.sort_values(
    "Revenue",
    ascending=False
)

print("\n========== CATEGORY PERFORMANCE ==========")
print(category_analysis.to_string(index=False))

plt.figure(figsize=(10, 6))

plt.bar(
    category_analysis["Category"],
    category_analysis["Revenue"]
)

plt.title("Revenue by Category")
plt.xlabel("Category")
plt.ylabel("Revenue (INR)")
plt.xticks(rotation=30)
plt.tight_layout()

plt.show()

plt.figure(figsize=(10, 6))

plt.bar(
    category_analysis["Category"],
    category_analysis["Profit"]
)

plt.title("Profit by Category")
plt.xlabel("Category")
plt.ylabel("Profit (INR)")
plt.xticks(rotation=30)
plt.tight_layout()

plt.show()

# ==============================
# TOP 10 PRODUCTS
# ==============================

product_analysis = (
    df.groupby("Product")
    .agg(
        Revenue=("Sales_INR", "sum"),
        Profit=("Profit_INR", "sum"),
        Units=("Quantity", "sum"),
        Orders=("Order_ID", "nunique")
    )
    .reset_index()
)

product_analysis["Profit_Margin"] = (
    product_analysis["Profit"] /
    product_analysis["Revenue"] * 100
)

top_10_products = product_analysis.sort_values(
    "Revenue",
    ascending=False
).head(10)

print("\n========== TOP 10 PRODUCTS ==========")
print(top_10_products.to_string(index=False))
# ==============================
# STATE-WISE PERFORMANCE
# ==============================

state_analysis = (
    df.groupby("State")
    .agg(
        Revenue=("Sales_INR", "sum"),
        Profit=("Profit_INR", "sum"),
        Orders=("Order_ID", "nunique"),
        Customers=("Customer_ID", "nunique")
    )
    .reset_index()
)

state_analysis["Profit_Margin"] = (
    state_analysis["Profit"] /
    state_analysis["Revenue"] * 100
)

state_analysis = state_analysis.sort_values(
    "Revenue",
    ascending=False
)

print("\n========== STATE-WISE PERFORMANCE ==========")
print(state_analysis.to_string(index=False))
# ==============================
# CUSTOMER ANALYSIS
# ==============================

customer_orders = (
    df.groupby("Customer_ID")
    .agg(
        Orders=("Order_ID", "nunique"),
        Revenue=("Sales_INR", "sum"),
        Profit=("Profit_INR", "sum")
    )
    .reset_index()
)

customer_orders["Customer_Type"] = customer_orders["Orders"].apply(
    lambda x: "Returning" if x > 1 else "One-Time"
)

print("\n========== CUSTOMER ANALYSIS ==========")
print(customer_orders.head())

customer_segments = (
    customer_orders["Customer_Type"]
    .value_counts()
)

print("\n========== CUSTOMER SEGMENTS ==========")
print(customer_segments)
customer_type_analysis = (
    customer_orders.groupby("Customer_Type")
    .agg(
        Customers=("Customer_ID", "count"),
        Revenue=("Revenue", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Orders", "sum")
    )
    .reset_index()
)

customer_type_analysis["Revenue_Per_Customer"] = (
    customer_type_analysis["Revenue"] /
    customer_type_analysis["Customers"]
)

print("\n========== CUSTOMER TYPE PERFORMANCE ==========")
print(customer_type_analysis.to_string(index=False))

average_order_value = (
    df["Sales_INR"].sum() /
    df["Order_ID"].nunique()
)

print("\n========== CUSTOMER METRICS ==========")
print(f"Average Order Value: ₹{average_order_value:,.2f}")
print(
    f"Average Orders per Customer: "
    f"{total_orders / total_customers:.2f}"
)

# ==============================
# DISCOUNT ANALYSIS
# ==============================

discount_analysis = (
    df.groupby("Discount_Pct")
    .agg(
        Revenue=("Sales_INR", "sum"),
        Profit=("Profit_INR", "sum"),
        Orders=("Order_ID", "nunique"),
        Units=("Quantity", "sum")
    )
    .reset_index()
)

discount_analysis["Profit_Margin"] = (
    discount_analysis["Profit"] /
    discount_analysis["Revenue"] * 100
)

print("\n========== DISCOUNT ANALYSIS ==========")
print(discount_analysis.to_string(index=False))

# Discount vs Profit correlation

discount_correlation = df[
    ["Discount_Pct", "Profit_INR"]
].corr().iloc[0, 1]

print(
    f"\nDiscount vs Profit Correlation: "
    f"{discount_correlation:.3f}"
)

# Discount vs Profit chart

plt.figure(figsize=(10, 6))

plt.scatter(
    df["Discount_Pct"],
    df["Profit_INR"],
    alpha=0.4
)

plt.title("Discount vs Profit")
plt.xlabel("Discount (%)")
plt.ylabel("Profit (INR)")
plt.tight_layout()

plt.show()

# ==============================
# RETURN ANALYSIS
# ==============================

return_analysis = (
    df.groupby("Returned")
    .agg(
        Orders=("Order_ID", "nunique"),
        Revenue=("Sales_INR", "sum"),
        Profit=("Profit_INR", "sum"),
        Units=("Quantity", "sum")
    )
    .reset_index()
)

return_analysis["Profit_Margin"] = (
    return_analysis["Profit"] /
    return_analysis["Revenue"] * 100
)

print("\n========== RETURN ANALYSIS ==========")
print(return_analysis.to_string(index=False))

total_orders = df["Order_ID"].nunique()

returned_orders = df.loc[
    df["Returned"] == "Yes",
    "Order_ID"
].nunique()

return_rate = (returned_orders / total_orders) * 100

print(f"\nReturn Rate: {return_rate:.2f}%")

# ==============================
# RETURN REASONS
# ==============================

return_reasons = (
    df[df["Returned"] == "Yes"]
    .groupby("Return_Reason")
    .agg(
        Orders=("Order_ID", "nunique"),
        Revenue=("Sales_INR", "sum")
    )
    .reset_index()
    .sort_values("Orders", ascending=False)
)

print("\n========== RETURN REASONS ==========")
print(return_reasons.to_string(index=False))

# ==============================
# DELIVERY & CUSTOMER RATING
# ==============================

delivery_rating = (
    df.groupby("Delivery_Days")
    .agg(
        Orders=("Order_ID", "nunique"),
        Avg_Rating=("Customer_Rating", "mean"),
        Return_Rate=("Returned", lambda x: (x == "Yes").mean() * 100)
    )
    .reset_index()
)

print("\n========== DELIVERY & RATING ==========")
print(delivery_rating.to_string(index=False))

rating_delivery_corr = df[
    ["Delivery_Days", "Customer_Rating"]
].corr().iloc[0, 1]

print(
    f"\nDelivery Days vs Customer Rating Correlation: "
    f"{rating_delivery_corr:.3f}"
)

plt.figure(figsize=(10, 6))

plt.scatter(
    df["Delivery_Days"],
    df["Customer_Rating"],
    alpha=0.4
)

plt.title("Delivery Days vs Customer Rating")
plt.xlabel("Delivery Days")
plt.ylabel("Customer Rating")
plt.tight_layout()

plt.show()

# ==============================
# DELIVERY SPEED ANALYSIS
# ==============================

df["Delivery_Group"] = pd.cut(
    df["Delivery_Days"],
    bins=[0, 3, 5, 7, 10],
    labels=[
        "1-3 Days",
        "4-5 Days",
        "6-7 Days",
        "8-10 Days"
    ]
)

delivery_group_analysis = (
    df.groupby("Delivery_Group", observed=True)
    .agg(
        Orders=("Order_ID", "nunique"),
        Avg_Rating=("Customer_Rating", "mean"),
        Return_Rate=("Returned", lambda x: (x == "Yes").mean() * 100)
    )
    .reset_index()
)

print("\n========== DELIVERY GROUP ANALYSIS ==========")
print(delivery_group_analysis.to_string(index=False))

plt.figure(figsize=(10, 6))

plt.bar(
    delivery_group_analysis["Delivery_Group"],
    delivery_group_analysis["Return_Rate"]
)

plt.title("Return Rate by Delivery Speed")
plt.xlabel("Delivery Speed")
plt.ylabel("Return Rate (%)")
plt.tight_layout()

plt.show()

# ==============================
# PAYMENT METHOD ANALYSIS
# ==============================

payment_analysis = (
    df.groupby("Payment_Method")
    .agg(
        Orders=("Order_ID", "nunique"),
        Revenue=("Sales_INR", "sum"),
        Profit=("Profit_INR", "sum"),
        Units=("Quantity", "sum")
    )
    .reset_index()
)

payment_analysis["Profit_Margin"] = (
    payment_analysis["Profit"] /
    payment_analysis["Revenue"] * 100
)

payment_analysis["Revenue_Per_Order"] = (
    payment_analysis["Revenue"] /
    payment_analysis["Orders"]
)

print("\n========== PAYMENT METHOD ANALYSIS ==========")
print(payment_analysis.to_string(index=False))

plt.figure(figsize=(10, 6))

plt.bar(
    payment_analysis["Payment_Method"],
    payment_analysis["Revenue"]
)

plt.title("Revenue by Payment Method")
plt.xlabel("Payment Method")
plt.ylabel("Revenue (INR)")
plt.xticks(rotation=30)
plt.tight_layout()

plt.show()