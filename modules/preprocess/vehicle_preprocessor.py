import os
import random
import numpy as np
import pandas as pd
from shapely.geometry import Point, Polygon, MultiPolygon
import itertools
import geopandas as gpd
import osmnx as ox

# -----------------------------------------------------------

# 스케줄 관련 함수

# schedule time conversion
def convert_schedule_time(start_str, end_str):
    """자정 넘는 스케줄 처리"""
    start, end = int(float(start_str)), int(float(end_str))
    if end <= start:
        end += 24
    return start, end

# build schedule rows
def build_rows(start_id: int, total: int, splits):
    """교대패턴 기반 스케줄 생성"""
    counts = [int(round(total * p)) for _, _, p in splits]
    diff = total - sum(counts)
    if counts:
        counts[0] += diff

    rows, cur = [], start_id
    for (ws, we, _), cnt in zip(splits, counts):
        start_h, end_h = convert_schedule_time(ws, we)
        for _ in range(cnt):
            rows.append((cur, start_h, end_h, 0))
            cur += 1

    return pd.DataFrame(rows, columns=["vehicle_id", "work_start", "work_end", "temporary_stopTime"])

# adaptive shift patterns
def adaptive_shift_patterns(start_min: int, end_min: int):
    """시뮬 시간대별 자동 교대패턴"""
    start_h, end_h = start_min // 60, end_min // 60
    duration = (end_min - start_min) / 60

    if duration <= 3:
        return [(str(max(start_h - 2, 0)), str(end_h + 4), 1.0)]
    elif duration <= 6:
        return [(str(max(start_h - 2, 0)), str(end_h + 2), 0.6),
                (str(start_h), str(end_h + 3), 0.4)]
    elif duration <= 10:
        return [(str(max(start_h - 3, 0)), str(end_h + 2), 0.4),
                (str(start_h), str(end_h + 4), 0.4),
                (str(start_h + 2), str(end_h + 6), 0.2)]
    else:
        return [("06","14",0.33),("14","22",0.33),("22","30",0.34)]

# build vehicle schedule
def build_vehicle_schedule(n_total, start_min, end_min, use_shift=False):
    """교대패턴 옵션에 따라 스케줄 생성"""
    if use_shift:
        splits = adaptive_shift_patterns(start_min, end_min)
        df = build_rows(0, n_total, splits)
        print(f"[ShiftMode] Automatic vehicle shift scheduling applied.")
    else:
        df = pd.DataFrame({
            "vehicle_id": range(n_total),
            "work_start": start_min,
            "work_end": end_min,
            "temporary_stopTime": 0
        })
        print("[SimpleMode] Uniform working schedule applied to all vehicles.")
    return df


# -----------------------------------------------------------

# 초기 위치 관련 함수

# *조회가 안 될때, https://www.openstreetmap.org 기입하고 싶은 지역명을 먼저 확인하고 실행하세요. 
# road_type : 1(고속도로), 2(간선도로), 3(집산도로)
class point_generator_with_OSM:
    
    def __init__(self):
        self.road_type = [2, 3]  # Main roads and minor roads
        
    # Filter road edges by highway type and minimum length
    def filter_edges(self, edges):
        edges['highway'] = [i if type(i) != list else "-".join(i) for i in edges['highway']]

        highway_cat_lst = ['motorway', 'motorway_link', 'rest_area', 'services', 'trunk', 'trunk_link']
        mainRoad_cat_lst = ['primary', 'primary_link', 'secondary', 'secondary_link', 'tertiary', 'tertiary_link']
        minorRoad_cat_lst = list(set(edges['highway']) - set(highway_cat_lst + mainRoad_cat_lst))
        road_type_dict = {1: highway_cat_lst, 2: mainRoad_cat_lst, 3: minorRoad_cat_lst}

        target_road = list(itertools.chain(*[road_type_dict[i] for i in self.road_type]))
        edges = edges.loc[[i in target_road for i in edges['highway']]]
        edges = edges.loc[(edges['length'] >= 10)]    
        edges = edges.reset_index()
        return edges
    
    # Generate random points along road edges
    def generate_point(self, target_edges, count):
        generated_nodes = []
        for _ in range(count):
            # Randomly select edge, cutting ratio and direction
            random_row = np.random.randint(len(target_edges))
            random_ratio = np.random.choice([0.1, 0.2, 0.3, 0.4, 0.5])
            random_reverse = np.random.choice([True, False])
            
            selected_row = target_edges.iloc[[random_row]].reset_index(drop=True)
            selected_row = selected_row.to_crs(5174)

            linestring = selected_row['geometry'].iloc[0]
            cut_length = selected_row['geometry'].length.iloc[0] * random_ratio    
            
            if random_reverse:
                linestring = linestring.reverse()
            
            split_point = linestring.interpolate(cut_length)    
            generated_nodes.append(split_point)
            
        generated_nodes = gpd.GeoDataFrame(generated_nodes, columns=['geometry'], geometry='geometry', crs=5174)
        generated_nodes = generated_nodes.to_crs(4326)

        generated_nodes['lon'] = [i.x for i in generated_nodes['geometry']]
        generated_nodes['lat'] = [i.y for i in generated_nodes['geometry']]

        return generated_nodes
    
    # Generate points for a specific place name
    def point_generator_about_placeName(self, place, count):
        # Load road network
        G = ox.graph_from_place(place, network_type="drive_service", simplify=True)
        _, edges = ox.graph_to_gdfs(G)
        edges = edges.reset_index(drop=True)

        # Filter roads by type
        edges = self.filter_edges(edges)
        
        # Generate points
        generated_nodes = self.generate_point(edges, count)
        return generated_nodes

    # Generate points for multiple geometries
    def point_generator_about_geometry(self, geoData):
        # Load roads for all unique place names
        place_lst = list(set(geoData['geoName']))
        edges_lst = []
        for plc in place_lst:
            G = ox.graph_from_place(plc, network_type='drive_service', simplify=True)
            _, edge = ox.graph_to_gdfs(G)
            edge = self.filter_edges(edge)
            edges_lst.append(edge)
        edges = pd.concat(edges_lst).reset_index(drop=True)

        # Generate points for each geometry
        generated_nodes_lst = []
        for _, row in geoData.iterrows():
            sub_edges = edges.loc[(edges['geometry'].intersects(row['geometry']))].reset_index(drop=True)

            generated_nodes = self.generate_point(sub_edges, row['count'])
            generated_nodes['id'] = row['id']
            generated_nodes = generated_nodes[['id', 'geometry', 'lon', 'lat']]
            generated_nodes_lst.append(generated_nodes)
        generated_nodes_lst = pd.concat(generated_nodes_lst).reset_index(drop=True)
        return generated_nodes_lst



def assign_osm_points(vehicle_df, sgn_union=None, use_osm_vehicle=False, count=None):
    """
    차량 초기위치를 OSM 도로망 기반으로 생성.
    Polygon 기반 네트워크가 없을 경우 즉시 에러 발생 (fallback 없음).
    """
    if not use_osm_vehicle:
        raise ValueError("[Error] use_osm_vehicle=False state is not allowed to call assign_osm_points().")
    
    if sgn_union is None:
        raise ValueError("[Error] sgn_union(city boundary) is not provided. Please provide the GeoJSON boundary data.")

    pg = point_generator_with_OSM()

    try:
        # 반드시 polygon 기반으로 도로망 로드
        G = ox.graph_from_polygon(sgn_union, network_type="drive", simplify=True)
        _, edges = ox.graph_to_gdfs(G)
        edges = pg.filter_edges(edges)
        nodes = pg.generate_point(edges, count or len(vehicle_df))
    except Exception as e:
        # fallback 없음: 즉시 강제 중단
        raise RuntimeError(f"[OSM Error] Failed to load road network based on polygon: {e}")

    # 결과 반영
    vehicle_df["lat"] = nodes["lat"]
    vehicle_df["lon"] = nodes["lon"]
    print(f"[OSM] Generated {len(vehicle_df)} initial vehicle positions using the road network.")

    return vehicle_df


# -----------------------------------------------------------


# generate vehicle fields
def generate_vehicle_fields(df: pd.DataFrame):
    """공통 필드 추가"""
    df["taxi_type"] = 0
    df["lat"] = np.nan
    df["lon"] = np.nan
    df["cartype"] = 0
    return df


# save vehicle data
def save_vehicle_data(vehicle_df, output_dir):
    """CSV 파일 저장"""
    os.makedirs(f"{output_dir}/vehicle", exist_ok=True)
    path = f"{output_dir}/vehicle/vehicle_data.csv"
    vehicle_df.to_csv(path, index=False)
    return path


# main preprocess function
def preprocess_vehicles(
    sgn_union,
    n_total: int,
    start_min: int,
    end_min: int,
    use_shift: bool = False,
    seed: int | None = None,
    output_dir: str = "./data/agents"
):
    """
    교대패턴 + 랜덤 초기위치 포함 차량 전처리 메인 함수
    """
    # 1. set seed
    # Seed 고정
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    # 2. build vehicle schedule
    vehicle_df = build_vehicle_schedule(n_total, start_min, end_min, use_shift)

    # 3. generate vehicle fields
    vehicle_df = generate_vehicle_fields(vehicle_df)

    # 4. assign osm points
    vehicle_df = assign_osm_points(vehicle_df, sgn_union=sgn_union, use_osm_vehicle=True, count=len(vehicle_df))
    save_vehicle_data(vehicle_df, output_dir)

    return vehicle_df