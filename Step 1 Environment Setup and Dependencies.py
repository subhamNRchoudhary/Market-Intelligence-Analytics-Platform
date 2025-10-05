import pandas as pd
import numpy as np
import os
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from openpyxl import Workbook, load_workbook
from openpyxl.drawing.image import Image
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
import io
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Professional visualization settings
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")