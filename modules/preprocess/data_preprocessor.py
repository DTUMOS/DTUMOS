import sys
import pandas as pd 
import numpy as np 
import copy 
import warnings
from datetime import datetime
from modules.preprocess.passenger_preprocessor import preprocess_passengers
from modules.preprocess.vehicle_preprocessor import preprocess_vehicles
from modules.engine.io_manager import generate_path_to_save, save_json_data, checking_progress
from modules.utils.distance_utils import filter_outside_region

warnings.filterwarnings('ignore')

# Convert time standard from datetime to minutes
def convert_time_standard(operation_record):
    operation_record['ride_time'] = pd.to_datetime(operation_record['ride_time'])
    
    YMD = list(set(operation_record['ride_time'].dt.strftime('%Y%m%d')))
    target_YMD = min([datetime.strptime(i, '%Y%m%d') for i in YMD])
    
    operation_record['ride_time'] = operation_record['ride_time'] - target_YMD
    operation_record['ride_time'] = operation_record['ride_time'] / pd.Timedelta(minutes=1)
    operation_record['ride_time'] = np.floor(operation_record['ride_time']).astype('int')
    
    return operation_record, target_YMD


# Preprocess passenger data
def passenger_preprocessing(passengers, configs):
    passengers = passengers[[
        'ID', 'ride_time', 'ride_lat', 'ride_lon', 
        'alight_lat', 'alight_lon', 'dispatch_time', 'type'
    ]]
    return passengers


# Preprocess vehicle data
def vehicle_preprocessing(vehicles, configs):
    vehicles = vehicles[[
        'vehicle_id', 'cartype', 'work_start', 'work_end', 
        'temporary_stopTime', 'lat', 'lon'
    ]]
    
    # Convert work hours to minutes
    vehicles['work_start'] = vehicles['work_start'] * 60
    vehicles['work_end'] = vehicles['work_end'] * 60

    # Apply corp/private vehicle split if configured
    if configs.get("corp_priv_split"):
        # TODO: implement corp/priv split logic
        pass

    # Filter vehicles outside region boundary if configured
    if configs.get("filter_out_of_region", False):
        vehicles = filter_outside_region(vehicles, configs['relocation_region'])
    
    return vehicles


# Get preprocessed passenger and vehicle data
def get_preprocessed_data(passengers, vehicles, configs):
    passengers = passenger_preprocessing(passengers, configs)
    vehicles = vehicle_preprocessing(vehicles, configs)
    return passengers, vehicles


# Crop data to simulation time range
def crop_data_by_timerange(passengers, vehicles, inform):
    start_time, end_time = inform['time_range']
    
    # Filter passengers within time range
    passengers = passengers[
        (passengers['ride_time'] >= start_time) & 
        (passengers['ride_time'] < end_time)
    ].reset_index(drop=True)
    
    # Adjust vehicle schedules to time range
    vehicles = vehicles[vehicles['work_end'] > start_time]
    vehicles.loc[vehicles['work_start'] < start_time, 'work_start'] = start_time
    vehicles.loc[vehicles['work_end'] > end_time, 'work_end'] = end_time
    vehicles = vehicles.reset_index(drop=True)
    
    return passengers, vehicles


def extract_main(raw_data_path, boundary_path, base_date, start_min, end_min, num_taxis, use_shift, seed):
    #Passenger preprocess
    passenger_df, sgn_union = preprocess_passengers(
        raw_data_path=raw_data_path,
        boundary_path=boundary_path,
        base_date=base_date,
        start_min=start_min,
        end_min=end_min,
        output_dir="./data/agents"
    )

    # Vehicle preprocess
    vehicle_df = preprocess_vehicles(
        sgn_union=sgn_union,
        n_total=num_taxis,
        start_min=start_min,
        end_min=end_min,
        use_shift=use_shift,
        seed=seed,
        output_dir="./data/agents"
    )

    # Return both and YMD
    YMD = pd.Timestamp(base_date)
    return passenger_df, vehicle_df, YMD

