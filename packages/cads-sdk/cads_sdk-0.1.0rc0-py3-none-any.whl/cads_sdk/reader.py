from cads_sdk.pyarrow.pyarrow_add_on import PyArrow
from cads_sdk.pyspark.pyspark_add_on import PySpark
from .add_on import get_location_from_table, render_filters_pyarrow, get_spark


######################
def read_table(full_table_name, engine='spark'):
    """
    Convert a table in DWH to spark.sql.DataFrame


    Parameters
    ----------
    full_table_name: str
        Full table name in format database.table_name
    engine: str
        Default: spark


    Returns
    -------
    pyspark.sql.DataFrame


    Examples
    --------
    .. code-block: python
    >>> import cads_sdk as cs
    >>> df = cs.read_table("database.table_name")
    """

    PS = get_spark()
    if engine == 'spark':
        return PS.spark.read.table(full_table_name)
    # not support pyarrow because of delta table
    # elif engine == 'pyarrow':
    #     return PyArrow().read_table(full_table_name)


def sql(query):
    """
    Convert a SQL in spark.DataFrame object


    Parameters
    ----------
    query: str
        SQL query state



    Returns
    -------
    pyspark.sql.DataFrame


    Examples
    --------
    >>> import cads_sdk as cs
    >>> df = cs.sql("SELECT * FROM database.table_name")
    """
    PS = get_spark()
    return PS.spark.sql(query)


def refresh_table(full_table_name):
    """

    Parameters
    ----------
    full_table_name

    """
    PS = get_spark()
    return PS.spark.sql(f"""REFRESH TABLE {full_table_name}""")


def read_dwh_pd(full_table_name, filters='', engine='spark'):
    """
    Convert a table to pandas object


    Parameters
    ----------
    full_table_name: str
        Full table name in format database.table_name
    filters: str
        Filter value if needed
    engine: str
        Default: spark


    Returns
    -------
    pandas.DataFrame


    Examples
    --------
    >>> import cads_sdk as cs
    >>> import pandas as pd
    >>> pdf = pd.read_dwh("database.table_name", filter="d='2023-01-01'")
    """
    # ========================LINEAGE======================
    try:
        from cads_sdk.pyspark.pylineage import emitPythonJob
        emitPythonJob(full_table_name = full_table_name, outputNode=False)
    except:
        pass
    # =====================================================
    if engine == 'pyarrow':
        df_arrow = PyArrow().read_table(source=get_location_from_table(full_table_name), filters=render_filters_pyarrow(filters))
        df = df_arrow.to_pandas()
        return df

    if engine == 'spark':
        PS = get_spark()
        if filters:
            filters = 'where ' + filters

        df_spark = PS.spark.sql(f"select * from {full_table_name} {filters}")
        df = df_spark.toPandas()
        return df
    return "Your engine is not correct"


def read_dwh(full_table_name, filters=''):
    """
    Read table from dwh as spark.sql.DataFrame


    Parameters
    ----------
    full_table_name: str
        Full table name in format database.table_name
    engine: str
        Default: spark


    Returns
    -------
    pyspark.sql.DataFrame


    Examples
    --------
    >>> import cads_sdk as cs
    >>> import pandas as pd
    >>> df = cs.read_dwh("database.table_name", filter="d='2023-01-01'")
    """

    PS = get_spark()
    if filters:
        filters = 'where ' + filters
    df_spark = PS.spark.sql(f"select * from {full_table_name} {filters}")
    return df_spark


def read_csv(path, sep=',', header=True):
    """
    Convert csv file in Datalake to spark.sql.DataFrame


    Parameters
    ----------
    path: str
        Absolute path of csv file
    sep: str
        Default: ','
        Seperator
    header: bool
        Default: True

        If True:
        Get first line as headers


    Returns
    -------
    pyspark.sql.DataFrame


    Examples
    --------
    >>> import cads_sdk as cs
    >>> df = cs.read_csv("file:/home/user/a.csv", sep='\t')
    """
    PS = get_spark()
    return PS.read_csv(path=path, sep=sep, header=header)


def read_parquet(path):
    """
    Read parquet file from datalake as spark.sql.DataFrame


    Parameters
    ----------
    path: str
        Absolute path of parquet file


    Returns
    -------
    pyspark.sql.DataFrame


    Examples
    --------
    >>> import cads_sdk as cs
    >>> df = cs.read_parquet("file:/home/user/a.parquet")
    >>> df = cs.read_parquet("hdfs:/home/user/a.parquet")
    """
    PS = get_spark()
    return PS.read_parquet(path=path)


def read_json(path):
    """
    Convert a JSON file from datalake as spark.sql.DataFrame


    Parameters
    ----------
    path: str
        Absolute path of json file


    Returns
    -------
    Json


    Examples
    --------
    >>> import cads_sdk as cs
    >>> df = cs.read_json("file:/home/user/a.json", sep='\t')
    """
    return PyArrow().read_json(path)

