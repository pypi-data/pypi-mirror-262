from cads_sdk.pyspark.pyspark_add_on import PySpark
from cads_sdk.pyarrow.pyarrow_add_on import PyArrow

from cads_sdk.add_on import get_spark, refresh_table_metadata
from cads_sdk.utils import choose_num_core, choose_executor_memory, choose_driver_memory


def spark_dataframe_to_dwh(self, hdfs_path, database, table_name, repartition=False, numPartitions=None, partition_by='',
                           partition_date='', compression='snappy', encrypt_columns=[], keys_path=''
                           ):
    """
    Store spark DataFrame object to datalake using pyarrow


    Parameters
    ----------
    self
    hdfs_path:
    database:
    table_name:
    repartition:
    partition_by:
    partition_date:
    compressionL
    encrypt_columns:
    existing_data_behavior:
    encrypt_columns:
    keys_path:
        .. deprecated:: 1.1.0
            Not support in future, using parquet encryption instead


    Returns
    -------
    None or str


    Examples
    ----------
    .. code-block:: python

        import cads_sdk as cs

        df1 = cs.read_table("database.table_name")
        df1.to_dwh(
            hdfs_path="path/to/data/test1.delta", # just end path with delta then table will be store in delta format
            partition_by="m", # column time want to partition
            partition_date=ELT_DATE, # partition date
            database="database_name", # database name
            table_name="test1",
            repartition=True # table name
        )

    Function will store pandas object to Data warehouse with name database.test1
    """

    PS = get_spark()
    PS.store_spark_dataframe_to_dwh(data=self, hdfs_path=hdfs_path, database=database, table_name=table_name,
                                                    repartition=repartition, numPartitions=numPartitions, partition_by=partition_by, partition_date=partition_date, compression=compression,
                                                    encrypt_columns=encrypt_columns, keys_path=keys_path)


def to_dwh(self, hdfs_path, database, table_name, repartition=False, numPartitions=None, compression = 'snappy', partition_by='',
           partition_date='', encrypt_columns=[], keys_path='', num_executors='1', parallel=True,
           engine='spark',
           use_deprecated_int96_timestamps=True, existing_data_behavior='overwrite_or_ignore'):
    """


    Parameters
    ----------
    self
    hdfs_path
    database
    table_name
    repartition
    numPartitions
    compression
    partition_by
    partition_date
    encrypt_columns
    keys_path: str
            .. deprecated:: 1.1.0
            Not support in future, using parquet encryption instead
    num_executors
    parallel
    engine
    use_deprecated_int96_timestamps
    existing_data_behavior


    Returns
    -------
    None or str


    Examples
    ----------
    .. code-block:: python

        # step 1 read data
        ELT_DATE = '2021-12-01'
        ELT_STR = ELT_DATE[:7]
        import pandas as pd
        df1 = pd.read_csv('./data.csv', sep='\t')


        import cads_sdk as cs

        # function to store to dwh
        df1.to_dwh(
            hdfs_path="path/to/data/test1.parquet/", # path hdfs
            partition_by="m", # column time want to partition
            partition_date=ELT_DATE, # partition date
            database="database_name", # database name
            table_name="test1", # table name
            repartition=True
        )

    Function store df1 to database_name.test1 at location "path/to/data/test1.delta"
    """
    if repartition:
        engine='spark'

    df_memory = self.memory_usage(index=True).sum() / 1024 / 1024

    if engine == 'spark' or 'delta' in hdfs_path.lower():
        if parallel:
            num_executors = choose_num_core(df_memory)

        driver_memory = choose_driver_memory(df_memory)
        executor_memory = choose_executor_memory(df_memory, int(num_executors))
        PS = get_spark()
        PS.to_dwh_spark(data=self, hdfs_path=hdfs_path, repartition=repartition,
                                        numPartitions=numPartitions, partition_by=partition_by,
                                        partition_date=partition_date, compression=compression, database=database, table_name=table_name,
                                        encrypt_columns=encrypt_columns, keys_path=keys_path)
    else:
        PyArrow().to_dwh_pyarrow(data=self, hdfs_path=hdfs_path, database=database, table_name=table_name,
                                 partition_by=partition_by, partition_date=partition_date,
                                 use_deprecated_int96_timestamps=True, existing_data_behavior=existing_data_behavior, encrypt_columns=encrypt_columns, keys_path=keys_path)


def write_json(data, path):
    """
    Function to write json object to datalake


    Parameters
    ----------
    data: Json object
    path: str
        Hdfs path


    Returns
    -------
    None or str


    Examples
    -----------

    .. code-block:: python

        import cads_sdk as cs
        json__file = cs.read_json('/path/to/file.json')
        ss.write_json(data, '/path/to_file.json')
    """
    # ========================LINEAGE======================
    try:
        from cads_sdk.pyspark.pylineage import emitPythonJob
        emitPythonJob(hdfs_path=path, outputNode=True)
    except:
        pass
    # =====================================================
    return PyArrow().write_json(data=data, path=path)


def to_dwh_pyarrow(self, hdfs_path, database, table_name, partition_by='', partition_date='',
                   use_deprecated_int96_timestamps=True, existing_data_behavior='overwrite_or_ignore',
                   encrypt_columns=[], keys_path=''):
    """
    Store pandas object to datalake using pyarrow


    Parameters
    ----------
    self
    hdfs_path
    database
    table_name
    partition_by
    partition_date
    use_deprecated_int96_timestamps
    existing_data_behavior
    encrypt_columns
    keys_path


    Returns
    -------


    Examples:
    ----------

    """
    PyArrow().to_dwh_pyarrow(data=self, hdfs_path=hdfs_path, database=database, table_name=table_name, partition_by=partition_by,
                             partition_date=partition_date, use_deprecated_int96_timestamps=use_deprecated_int96_timestamps,
                             existing_data_behavior=existing_data_behavior, encrypt_columns=encrypt_columns,
                             keys_path=keys_path)
    refresh_table_metadata(database=database, table_name=table_name, hdfs_path=hdfs_path, partition_by=partition_by)