__doc__ = """
cads-sdk: Functions to help Data Scientist work more effectively with unstructured data and datalake
=====================================================================
**cads-sdk**
Function to convert 
-------------
Here are just a few of the things that cads_sdk does well:
# Image pre-processing ready for train
    - Function Convert from image folders to parquet: 
      from cads.nosql.converter import ConvertFromFolderImage
    - Function Convert from zip fize to parquet: 
      from cads.nosql.converter import ConvertFromFolderImage
    - Function Convert parquet to folder of image: 
      from cads.nosql.converter import ConvertToFolderImage
    - Function to display parquet image
      from cads.nosql import display
      
# Audio pre-processing ready for train
    - Function Convert from audio folders to parquet: 
      from cads.nosql.converter import ConvertToFolderAudio
    - Function Convert from audio folders to parquet: 
      from cads.nosql.converter import ConvertFromFolderAudio
# Video
    - Function Convert from video files to parquet of frame: 
      from cads.nosql.converter import ConvertFromVideo2Image
    - Function to display frame parquet
      from cads.nosql import display
"""
from .pyarrow import PyArrow
from .pyspark.pyspark_add_on import PySpark, Utf8Encoder
from .reader import read_dwh_pd, read_csv, read_json, read_parquet, read_dwh, read_table, sql
from .writter import write_json, to_dwh, spark_dataframe_to_dwh, refresh_table_metadata
from .add_on import drop_table, drop_table_and_delete_data, spark_dataframe_info, limit_timestamp, show
from cads_sdk import reader
from cads_sdk import writter
from cads_sdk import pyarrow

from cads_sdk.pandas.pandas_decrypt import decrypt, decrypt_column
from cads_sdk.pyarrow import ls, mkdir, cat, exists, info, open

try:
    from IPython import get_ipython
    # load magic function
    from makeup.magics import *
    _ = load_ipython_extension(get_ipython())
except:
    pass


import pandas as pd
from pandas import DataFrame
from pandas.core.series import Series
from .utils import modulereload


DataFrame.to_dwh = to_dwh
#DataFrame._repr_html_ = PandasDataFrame_repr_html_
modulereload(pd)

Series.decrypt_column = decrypt_column
pd.read_dwh = read_dwh_pd
modulereload(pd)


from pyspark.sql import DataFrame as SparkDataFrame
SparkDataFrame.to_dwh = spark_dataframe_to_dwh
SparkDataFrame.info = spark_dataframe_info

try:
    from cads_sdk.pyspark.pylineage import PandasConversionMixin
    SparkDataFrame.toPandas = PandasConversionMixin.toPandasLineage
except:
    pass


def start():
    return reader.PySpark().spark


def stop():
    return reader.PySpark().spark.stop()


SparkDataFrame.show = show

__version__ = '0.1.0rc0'
__all__ = ["reader", "writter", "pyarrow"]



