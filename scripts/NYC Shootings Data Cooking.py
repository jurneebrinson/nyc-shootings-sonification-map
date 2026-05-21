import pandas as pd
import json
import os
print("Saving to:", os.getcwd())

shootings = pd.read_csv('/Users/jurnee/Desktop/MUSIC EDUCATION/SOUNDING DATA STUDIO/nyc-shootings-sonification-map/data/Shootings_(2006-Present)_20260417.csv')

# Preview the dataset
print(shootings.head())

# Check the borough names
print(shootings['BORO'].unique())

# Check for rows missing longitude and latitude values
print(shootings[['Latitude', 'Longitude']].isna().sum())

# Isolate missing rows
shootings_missing = shootings[
    shootings['Latitude'].isna() | shootings['Longitude'].isna()
]

print("Missing rows:", len(shootings_missing))

# Create clean dataset
shootings_clean = shootings.dropna(subset=['Latitude', 'Longitude']).copy()

print("Clean rows:", len(shootings_clean))

# Convert to datetime, merge date and time, and sort by date and time
shootings_clean['DATETIME'] = pd.to_datetime(
    shootings_clean['OCCUR_DATE'].astype(str) + ' ' + shootings_clean['OCCUR_TIME'].astype(str)
)

shootings_clean = shootings_clean.sort_values('DATETIME').reset_index(drop=True)

# Create time bins
shootings_clean["week"] = shootings_clean["DATETIME"].dt.to_period("W")
shootings_clean["month"] = shootings_clean["DATETIME"].dt.to_period("M")
shootings_clean["year"] = shootings_clean["DATETIME"].dt.to_period("Y")

print(shootings_clean.head())

# Take only necessary columns
shootings_small = shootings_clean[[
    "INCIDENT_KEY",
    "BORO",
    "Latitude",
    "Longitude",
    "DATETIME",
    "OCCUR_DATE",
    "OCCUR_TIME"
]].copy()

# Initialize column
shootings_small["t_norm"] = 0.0

# Compute normalized time per borough
for boro in shootings_small["BORO"].unique():
    mask = shootings_small["BORO"] == boro
    
    df_boro = shootings_small.loc[mask]
    
    min_time = df_boro["DATETIME"].min()
    max_time = df_boro["DATETIME"].max()
    
    # Avoid division by zero (edge case: if all timestamps identical)
    if min_time == max_time:
        shootings_small.loc[mask, "t_norm"] = 0.0
    else:
        shootings_small.loc[mask, "t_norm"] = (
            (df_boro["DATETIME"] - min_time) / (max_time - min_time)
        ).values

# Sanity Check
print(
    shootings_small
    .groupby("BORO")["t_norm"]
    .agg(["min", "max"])
)

print(shootings_small.head())

# Aggregation function
def aggregate_data(df, time_col, output_name):
    
    grouped = (
        df.groupby(["BORO", time_col])
        .agg({
            "Latitude": "mean",
            "Longitude": "mean",
            "INCIDENT_KEY": "count"
        })
        .rename(columns={"INCIDENT_KEY": "count"})
        .reset_index()
    )

    # Convert period → timestamp
    grouped["datetime"] = grouped[time_col].dt.to_timestamp()
    grouped = grouped.sort_values(["BORO", "datetime"]).reset_index(drop=True)

    # Normalize time per borough (same idea you already used)
    grouped["t_norm"] = 0.0

    for boro in grouped["BORO"].unique():
        mask = grouped["BORO"] == boro
        df_boro = grouped.loc[mask]

        min_time = df_boro["datetime"].min()
        max_time = df_boro["datetime"].max()

        if min_time == max_time:
            grouped.loc[mask, "t_norm"] = 0.0
        else:
            grouped.loc[mask, "t_norm"] = (
                (df_boro["datetime"] - min_time) / (max_time - min_time)
            ).values

    # Convert to GeoJSON
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }

    for _, row in grouped.iterrows():
        feature = {
            "type": "Feature",
            "properties": {
                "borough": row["BORO"],
                "datetime": row["datetime"].isoformat(),
                "count": int(row["count"]),             # Number of incidents in bin
                "t_norm": float(row["t_norm"])
            },
            "geometry": {
                "type": "Point",
                "coordinates": [
                    float(row["Longitude"]),
                    float(row["Latitude"])
                ]
            }
        }

        geojson["features"].append(feature)

    # Save
    with open(f"{output_name}.geojson", "w") as f:
        json.dump(geojson, f)

    print(f"Saved {output_name}.geojson with {len(grouped)} rows")

# Export
shootings_small.to_csv("data/shootings_normalized.csv", index=False)

# json Conversion for Mapbox
geojson = {
    "type": "FeatureCollection",
    "features": []
}

for _, row in shootings_small.iterrows():
    feature = {
        "type": "Feature",
        "properties": {
            "incident_key": int(row["INCIDENT_KEY"]),
            "borough": row["BORO"],
            "datetime": row["DATETIME"].isoformat(),
            "occur_date": row["OCCUR_DATE"],
            "occur_time": row["OCCUR_TIME"],
            "t_norm": float(row["t_norm"]),
        },
        "geometry": {
            "type": "Point",
            "coordinates": [
                float(row["Longitude"]),
                float(row["Latitude"])
            ]
        }
    }
    
    geojson["features"].append(feature)

# Save to file
with open("data/shootings.geojson", "w") as f:
    json.dump(geojson, f)

aggregate_data(shootings_clean, "week", "shootings_weekly")
aggregate_data(shootings_clean, "month", "shootings_monthly")
aggregate_data(shootings_clean, "year", "shootings_yearly")