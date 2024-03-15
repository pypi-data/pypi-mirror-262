import pandas as pd
from simba.roi_tools.ROI_multiply import create_emty_df
from simba.utils.read_write import read_df

RECTANGLES_CSV_PATH = ''
CIRCLES_CSV_PATH = ''
POLYGONS_CSV_PATH = ''

if RECTANGLES_CSV_PATH is not None:
    rectangles_df = read_df(file_path=RECTANGLES_CSV_PATH, file_type='csv')



