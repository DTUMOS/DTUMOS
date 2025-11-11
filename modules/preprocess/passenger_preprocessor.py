# modules/preprocess/passenger_preprocessor.py
import os
import pandas as pd
import geopandas as gpd
from shapely.ops import unary_union
import numpy as np

# 1. Load raw data
def load_raw_data(raw_data_path: str) -> pd.DataFrame:
    if raw_data_path.endswith(".xlsx") or raw_data_path.endswith(".xls"):
        df = pd.read_excel(raw_data_path)
    else:
        df = pd.read_csv(raw_data_path)
    return df

# 2. Remove coordinate outliers (대한민국 범위 + 0,0 제외)
def filter_valid_coordinates(df: pd.DataFrame) -> pd.DataFrame:
    valid_lat = (33, 39)
    valid_lon = (124, 132)
    mask_pickup = (
        df["승차Y좌표"].between(*valid_lat)
        & df["승차X좌표"].between(*valid_lon)
        & (df["승차Y좌표"] != 0)
        & (df["승차X좌표"] != 0)
    )
    mask_drop = (
        df["하차Y좌표"].between(*valid_lat)
        & df["하차X좌표"].between(*valid_lon)
        & (df["하차Y좌표"] != 0)
        & (df["하차X좌표"] != 0)
    )
    filtered = df.loc[mask_pickup & mask_drop].copy()
    return filtered

# 3. Filter within Seongnam boundary
def filter_within_boundary(df: pd.DataFrame, boundary_path: str):
    sgn = gpd.read_file(boundary_path)
    sgn_union = unary_union(sgn.geometry.values)
    print(f"[DEBUG] sgn_union 생성 완료 — 타입: {type(sgn_union)}")
    print(f"[DEBUG] 경계 도형 개수: {len(sgn)}")
    print(f"[DEBUG] CRS: {sgn.crs}")
    pickup_gdf = gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(df["승차X좌표"], df["승차Y좌표"]),
        crs="EPSG:4326"
    )
    filtered = df.loc[pickup_gdf.within(sgn_union)].copy()
    return filtered, sgn_union

# 4. Filter by time range (UPDATED SIGNATURE)
def filter_by_time_range(df: pd.DataFrame, base_date: str, start_min: int, end_min: int) -> pd.DataFrame:
    """
    base_date: 'YYYY-MM-DD' (string) - 기준일 (예: '2024-04-18')
    start_min, end_min: 분 단위 누적 (0~, end_min may exceed 1440 to indicate next day)
    This builds start_dt and end_dt by adding minutes to base_date. If end_dt < start_dt,
    adds one day to end_dt so ranges crossing midnight are handled.
    """
    df["승차시간"] = pd.to_datetime(df["승차시간"], errors="coerce")

    start_dt = pd.Timestamp(base_date) + pd.Timedelta(minutes=int(start_min))
    end_dt = pd.Timestamp(base_date) + pd.Timedelta(minutes=int(end_min))
    # If end_dt is earlier than start_dt (e.g., start=1380, end=180), move end to next day
    if end_dt < start_dt:
        end_dt += pd.Timedelta(days=1)

    # inclusive="left" keeps times >= start_dt and < end_dt
    filtered = df.loc[df["승차시간"].between(start_dt, end_dt, inclusive="left")].copy()
    print(f"[Time filter] {start_dt} ~ {end_dt} -> {len(filtered)} rows")
    return filtered

# 5. Compute ride_time (minutes since base_date)
def compute_ride_time(df: pd.DataFrame, base_date: str) -> pd.DataFrame:
    base = pd.Timestamp(base_date).normalize()
    df["ride_time"] = ((df["승차시간"] - base).dt.total_seconds() // 60).astype(int)
    return df

# 6. Map taxi type
def map_taxi_type_column(df: pd.DataFrame) -> pd.DataFrame:
    def _map(v):
        s = ("" if pd.isna(v) else str(v)).strip().lower()
        if "개인" in s: return 0
        if ("법인" in s) or ("일반" in s): return 1
        return 1
    df["taxi_type"] = df["구분"].map(_map).fillna(1).astype(int)
    return df

# 7. Generate passenger DataFrame
def build_passenger_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    passenger_df = pd.DataFrame({
        "ID": range(len(df)),
        "ride_time": df["ride_time"],
        "dispatch_time": 0,
        "ride_lat": df["승차Y좌표"],
        "ride_lon": df["승차X좌표"],
        "alight_lat": df["하차Y좌표"],
        "alight_lon": df["하차X좌표"],
        "taxi_type": df["taxi_type"],
        "type": 0
    })
    return passenger_df

# Main function
def preprocess_passengers(
    raw_data_path: str,
    boundary_path: str,
    base_date: str,
    start_min: int,
    end_min: int,
    output_dir: str = "./data/agents"
):
    """
    Returns:
      passenger_df (pd.DataFrame),
      sgn_union (shapely.geometry)  -- so caller can reuse boundary for vehicle preprocessing
    """
    print("[passenger_preprocessor] Loading raw data...")
    df = load_raw_data(raw_data_path)

    print("[passenger_preprocessor] Filtering invalid coordinates...")
    df = filter_valid_coordinates(df)

    print("[passenger_preprocessor] Filtering by Seongnam boundary...")
    df, sgn_union = filter_within_boundary(df, boundary_path)

    print("[passenger_preprocessor] Filtering by time range...")
    df = filter_by_time_range(df, base_date, start_min, end_min)

    print("[passenger_preprocessor] Computing ride_time...")
    df = compute_ride_time(df, base_date)

    print("[passenger_preprocessor] Mapping taxi type...")
    df = map_taxi_type_column(df)

    print("[passenger_preprocessor] Building passenger dataframe...")
    passenger_df = build_passenger_dataframe(df)

    os.makedirs(f"{output_dir}/passenger", exist_ok=True)
    passenger_path = f"{output_dir}/passenger/passenger_data.csv"
    passenger_df.to_csv(passenger_path, index=False)
    print(f"[passenger_preprocessor] Saved → {passenger_path}")

    return passenger_df, sgn_union