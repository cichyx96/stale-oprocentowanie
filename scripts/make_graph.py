from datetime import datetime, timedelta

import os
import pathlib

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm  # For colormap


# Step 1: Define the base directory
base_dir = pathlib.Path(__file__).parent.parent / "dane"
img_output_dir = base_dir.parent / "img"
# Step 2: Initialize an empty list to store data
data = []

# Step 3: Walk through the directory structure and read JSON files
for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith(".json"):
            file_path = os.path.join(root, file)
            print(f"Reading file: {file_path}")
            # Load JSON data and append to the list
            with open(file_path, "r", encoding="utf-8") as f:
                data.extend(pd.read_json(f).to_dict(orient="records"))

# Step 4: Create a DataFrame from the collected data
df = pd.DataFrame(data)

# Step 5: Take only the last (most recent) offer for each bank
df_fixed = df.sort_values("offer_collection_date").groupby("bank").last().reset_index()

# Step 6: Sort the DataFrame by fixed_interest_rate
df_fixed = df_fixed.sort_values(by="fixed_interest_rate", ascending=True)

# Step 7: Visualize the data for fixed interest rates
plt.figure(figsize=(12, 6))

# Generate a colormap with as many colors as there are banks
colors = cm.get_cmap("tab10", len(df_fixed))  # Use a colormap like 'tab10'

bars = plt.bar(df_fixed["bank"], df_fixed["fixed_interest_rate"], color=[colors(i) for i in range(len(df_fixed))])

# Add values on top of the bars
for bar in bars:
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"{bar.get_height():.2f}",
        ha="center",
        va="bottom",
        fontsize=8,
    )

plt.xlabel("Bank")
plt.ylabel("Fixed Interest Rate (%)")
plt.title("Best (Lowest) Fixed Interest Rates by Bank")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(img_output_dir / "output_fixed_rate_plot.png")
plt.show()

# Step 8: Filter out rows where APR is 0 and take the best (lowest) APR for each bank
df_apr = df[df["apr"] > 0]  # Exclude rows where APR is 0
df_apr = df_apr.loc[df_apr.groupby("bank")["apr"].idxmin()]

# Step 9: Sort the DataFrame by APR
df_apr = df_apr.sort_values(by="apr", ascending=True)

# Step 10: Visualize the data for APR
plt.figure(figsize=(12, 6))

# Generate a colormap with as many colors as there are banks
colors = cm.get_cmap("tab20", len(df_apr))  # Use a different colormap like 'tab20'

bars = plt.bar(df_apr["bank"], df_apr["apr"], color=[colors(i) for i in range(len(df_apr))])

# Add values on top of the bars
for bar in bars:
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"{bar.get_height():.2f}",
        ha="center",
        va="bottom",
        fontsize=8,
    )

plt.xlabel("Bank")
plt.ylabel("APR (%)")
plt.title("Best (Lowest) APR by Bank")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(img_output_dir / "output_apr_plot.png")
plt.show()


# Linear trend of interest rates over time
# Prepare the full data for time trend, not only best offers
df["offer_collection_date"] = pd.to_datetime(df["offer_collection_date"])

# Filter df for rows with valid fixed_interest_rate
df_fixed_full = df[df["fixed_interest_rate"].notna()]
df_fixed_full = df_fixed_full.sort_values(["bank", "offer_collection_date"])

plt.figure(figsize=(12, 6))

for bank, group in df_fixed_full.groupby("bank"):
    plt.plot(
        group["offer_collection_date"],
        group["fixed_interest_rate"],
        marker="o",
        label=bank
    )

plt.xlabel("Date")
plt.ylabel("Fixed Interest Rate (%)")
plt.title("Fixed Interest Rates Over Time by Bank")
plt.xticks(rotation=45, ha="right")
plt.legend(title="Bank", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout()
plt.savefig(img_output_dir / "output_fixed_rate_over_time_by_bank.png")
plt.show()

# Ensure offer_collection_date is in datetime format
df["offer_collection_date"] = pd.to_datetime(df["offer_collection_date"])

# Filter df for rows with valid fixed_interest_rate
df_fixed_full = df[df["fixed_interest_rate"].notna()]
df_fixed_full = df_fixed_full.sort_values(["bank", "offer_collection_date"])

# Filter for the last 3 months
three_months_ago = datetime.now() - timedelta(days=90)
df_fixed_last_3_months = df_fixed_full[df_fixed_full["offer_collection_date"] >= three_months_ago]

# Plot for the last 3 months
plt.figure(figsize=(12, 6))

for bank, group in df_fixed_last_3_months.groupby("bank"):
    plt.plot(
        group["offer_collection_date"],
        group["fixed_interest_rate"],
        marker="o",
        label=bank
    )

plt.xlabel("Date")
plt.ylabel("Fixed Interest Rate (%)")
plt.title("Fixed Interest Rates Over Last 3 Months by Bank")
plt.xticks(rotation=45, ha="right")
plt.legend(title="Bank", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout()
plt.savefig(img_output_dir / "output_fixed_rate_last_3_months_by_bank.png")
plt.show()


# Filter df for rows with valid apr
df_apr_full = df[(df["apr"] > 0) & (df["offer_collection_date"].notna())]
df_apr_full["offer_collection_date"] = pd.to_datetime(df_apr_full["offer_collection_date"])
df_apr_full = df_apr_full.sort_values(["bank", "offer_collection_date"])

plt.figure(figsize=(12, 6))

for bank, group in df_apr_full.groupby("bank"):
    plt.plot(
        group["offer_collection_date"],
        group["apr"],
        marker="o",
        label=bank
    )

plt.xlabel("Date")
plt.ylabel("APR (%)")
plt.title("APR Over Time by Bank")
plt.xticks(rotation=45, ha="right")
plt.legend(title="Bank", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout()
plt.savefig(img_output_dir / "output_apr_over_time_by_bank.png")
plt.show()


# Filter df for rows with valid apr
df_apr_full = df[(df["apr"] > 0) & (df["offer_collection_date"].notna())]
df_apr_full["offer_collection_date"] = pd.to_datetime(df_apr_full["offer_collection_date"])
df_apr_full = df_apr_full.sort_values(["bank", "offer_collection_date"])

# Filter for the last 3 months
three_months_ago = datetime.now() - timedelta(days=90)
df_last_3_months = df_apr_full[df_apr_full["offer_collection_date"] >= three_months_ago]

# Plot for the last 3 months
plt.figure(figsize=(12, 6))

for bank, group in df_last_3_months.groupby("bank"):
    plt.plot(
        group["offer_collection_date"],
        group["apr"],
        marker="o",
        label=bank
    )

plt.xlabel("Date")
plt.ylabel("APR (%)")
plt.title("APR Over Last 3 Months by Bank")
plt.xticks(rotation=45, ha="right")
plt.legend(title="Bank", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout()
plt.savefig(img_output_dir / "output_apr_last_3_months_by_bank.png")
plt.show()

