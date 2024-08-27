import pandas as pd
import os 
from PIL import Image as PillowImage, ExifTags
import shutil

def get_folder(time, df):
    idx = df['start_time'].searchsorted(time, side='left')
    
    if idx > 0:
        return df.iloc[idx-1, 0]
    
    return df.iloc[-1, 0]


def prepare_df(df):
    df = df.sort_values('start_time').reset_index(drop=True)
    df = df[['folder', 'start_time']]
    print(df)

    return df


def get_photograph_time(file_path):
    try:
        with PillowImage.open(file_path) as pillow_img:
            img_exif = pillow_img.getexif()
            
            if img_exif.get(ExifTags.Base.DateTimeOriginal):
                return img_exif[ExifTags.Base.DateTimeOriginal]
    except:
        return None
        

def process_file(file_path, dir, mappings):
    photograph_time = get_photograph_time(file_path)
    
    if not photograph_time:
        return
    
    photograph_time = pd.to_datetime(photograph_time, format='%Y:%m:%d %H:%M:%S')
    folder = get_folder(photograph_time, mappings)
    
    out_dir = os.path.join(dir, folder)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    
    shutil.copy2(file_path, out_dir)
            

def organise(dir: str, mapping_file: str):
    mappings = pd.read_excel(mapping_file)
    mappings = prepare_df(mappings)
    
    
    for file in os.listdir(dir):
        file_path = os.path.join(dir, file)
        if os.path.isfile(file_path):
            print(f'.. processing... {file_path}')
            process_file(file_path, dir, mappings)
