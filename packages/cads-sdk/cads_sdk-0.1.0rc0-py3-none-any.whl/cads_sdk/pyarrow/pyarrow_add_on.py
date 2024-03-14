import json
import pyarrow as pa
from pyarrow import fs
from pyarrow import parquet as pq
import pandas as pd
# from cads_sdk.pyspark.pyspark_add_on import PySpark
from cads_sdk.utils import choose_num_core, choose_executor_memory, choose_driver_memory, \
    _check_series_convert_timestamps_internal, _get_local_timezone, contains_duplicates, modulereload, get_today


class Utf8Encoder(object):
    def __init__(self, fp):
        self.fp = fp

    def write(self, data):
        if not isinstance(data, bytes):
            data = data.encode('utf-8')
        self.fp.write(data)


class PyArrow:
    def __init__(self, existing_data_behavior='overwrite_or_ignore'):
        # Install latest Pyarrow version
        import os
        from ..conf import (HADOOP_HOST, HADOOP_PORT)
        if HADOOP_HOST and HADOOP_PORT:
            self.hdfs = fs.HadoopFileSystem(host=HADOOP_HOST, port=HADOOP_PORT)
            self.existing_data_behavior = existing_data_behavior
        else:
            self.hdfs = fs.LocalFileSystem()

    def check_keys_path_format(self, keys_path):
        import re
        if re.search('json$', keys_path):
            return True
        else:
            raise Exception("keys_path must end with '.json'")

    def autogenerate_key(self, length_key=22):
        import string
        import random

        key = ''.join(
            random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(length_key))
        key = key + "=="
        return key

    def read_json(self, path):
        with self.hdfs.open_input_file(path) as file:
            return json.load(file)

    def write_json(self, data, path):
        with self.hdfs.open_output_stream(path) as file:
            json.dump(data, Utf8Encoder(file))

    def append_keys_to_file(self, table_name, column_name='', keys_path='keys.json'):
        from datetime import datetime
        import json

        if self.check_is_file(keys_path):
            list_keys = self.read_json(keys_path)
        else:
            list_keys = []

        c = column_name
        keys = {}

        keys["name"] = f"secret_for_{table_name}_{c}"
        keys["description"] = ""
        keys["created"] = round(datetime.timestamp(datetime.now()))
        keys["material"] = self.autogenerate_key()
        list_keys.append(keys)

        with self.hdfs.open_output_stream(keys_path) as file:
            json.dump(list_keys, Utf8Encoder(file))

    def auto_generate_list_keys(self, table_name, column_name='', keys_path='keys.json'):
        from datetime import datetime
        import json

        if self.check_is_file(keys_path):
            list_keys = self.read_json(keys_path)
        else:
            list_keys = []

        for c in column_name.split(','):
            if c:
                keys = {}

                keys["name"] = f"secret_for_{table_name}_{c}"
                keys["description"] = f"This is secret_for_{table_name}_{c}"
                keys["created"] = round(datetime.timestamp(datetime.now()))
                keys["material"] = self.autogenerate_key()

                list_keys.append(keys)
        return list_keys

    def read_key_from_json(self, keys_path, table_name, column_names=[]):
        if self.check_is_file(keys_path):
            # Opening JSON file
            list_keys = self.read_json(keys_path)
        else:
            list_keys = []

        keys_exist = {}
        for c in column_names:
            name = f"secret_for_{table_name}_{c}"
            # check if key in file
            for k in list_keys:
                if name == k["name"]:
                    keys_exist[c] = k["material"]
        return keys_exist

    def encrypt_column(self, data, table_name, column_names=[], keys_path=''):
        # check file keys exist
        keys_exist = self.read_key_from_json(keys_path, table_name, column_names=column_names)

        for c in column_names:
            # if not found key generate new key append to keys.json
            if c not in keys_exist.keys():
                print('Append key for', c)
                self.append_keys_to_file(table_name, c, keys_path)

        list_keys = self.read_key_from_json(keys_path=keys_path, table_name=table_name, column_names=column_names)

        from cads_sdk.pandas.pandas_decrypt import encrypt_column
        for c in column_names:
            data[c] = data[c].encrypt_column(keys_exist[c])

        return data

    def pandas_to_parquet(self, pandas_type):
        TYPE_MAPPER = {
            'object': 'STRING',
            'float64': 'DOUBLE',
            'float32': 'DOUBLE',
            'int64': 'INT64',
            'int32': 'INT32',
            'bool': 'BOOLEAN',
            'datetime64': 'timestamp[s]',
            'datetime64[ns]': 'timestamp[s]',
            'datetime64[ns, Asia/Jakarta]': 'timestamp[s]',
            'datetime64[ns, UTC]': 'timestamp[s]'
        }

        return TYPE_MAPPER.get(pandas_type, 'None')

    def _check_series_convert_column_pyarrow(self, data, partition_by):

        new_type = {}

        # check column duplicated
        if contains_duplicates(data.columns):
            print("Columns is duplicated, check your data ")

        for c in data.columns:
            if str(data[c].dtype) == 'category':
                if max(data[c].str.len()) == min(data[c].str.len()):
                    data[c] = pd.to_datetime(data[c])
            if c == partition_by:
                new_type[partition_by] = pa.date64()
            else:

                data[c] = _check_series_convert_timestamps_internal(data[c], timezone=None)
                new_type[c] = self.pandas_to_parquet(str(data[c].dtype))

        fields = [pa.field(x, y) for x, y in new_type.items()]
        new_schema = pa.schema(fields)
        table = pa.Table.from_pandas(
            data,
            schema=new_schema,
            preserve_index=False
        )

        return table

    def check_is_file(self, hdfs_path):
        check = self.hdfs.get_file_info(hdfs_path)
        if check.type._name_ in ["Directory", "File"]:
            return True
        else:
            return False

    def read_table(self, source, filters=''):
        if filters:
            return pq.read_table(source=source, filters=filters, filesystem=self.hdfs)
        else:
            return pq.read_table(source=source, filesystem=self.hdfs)

    def read_first_file(self, hdfs_path):
        '''
        Read schema pyarrow
        '''
        first_hdfs = pa.HadoopFileSystem().ls(hdfs_path)[-1]
        return self.read_table(source=first_hdfs)


    def compare_data_type(self, first_sparkDF, second_sparkDF, partition_by):
        """
        Function to check when write data second time
        """
        error = {}
        first_sparkDF_schema = {}
        second_sparkDF_schema = {}

        for c in first_sparkDF.schema:
            c_name = c.name
            if partition_by == c_name and partition_by != '':
                continue
            first_sparkDF_schema[c.name] = c.type

        for c in second_sparkDF.schema:
            c_name = c.name
            if partition_by == c_name and partition_by != '':
                continue
            second_sparkDF_schema[c.name] = c.type

        if len(first_sparkDF_schema.keys()) != len(second_sparkDF_schema.keys()):
            print(f'First time have columns', first_sparkDF.schema.names)
            print(f'Second time have columns', second_sparkDF.schema.names)

            raise ValueError(f"First time have {len(first_sparkDF)} columns but second time have {len(second_sparkDF.schema)} columns")

        for c in second_sparkDF_schema.keys():
            second_type = second_sparkDF_schema[c]
            first_type = first_sparkDF_schema[c]

            if first_type != second_type:
                error[c] = {'first_time': first_type, 'second_time': second_type}

            if error.keys():
                print('Error', error)
                del first_sparkDF
                del second_sparkDF
                raise TypeError(f"DataType of Columns this time store is not like first time")
        print('Check schema OK')
        del first_sparkDF

    def to_dwh_pyarrow(self, data, hdfs_path, database, table_name, partition_by='', partition_date='',
                       use_deprecated_int96_timestamps=True, existing_data_behavior='overwrite_or_ignore',encrypt_columns=[], keys_path=''):

        if encrypt_columns:
            if keys_path:
                if self.check_keys_path_format(keys_path):
                    data = self.encrypt_column(data=data, table_name=table_name, column_names=encrypt_columns, keys_path=keys_path)
            else:
                raise Exception("You must add parameters keys_path=")


        if partition_by:
            if partition_by in data.columns:
                table = self._check_series_convert_column_pyarrow(data, partition_by)
            else:
                if not partition_date:
                    self.query_yes_no("""You should config partition_date, default today \nContinues Y/n?""")
                    partition_date = get_today()

                data[partition_by] = pd.to_datetime(partition_date)
                table = self._check_series_convert_column_pyarrow(data, partition_by)

            print('HDFS path: ', hdfs_path)

            if self.check_is_file(hdfs_path):
                self.compare_data_type(self.read_first_file(hdfs_path), table, partition_by)

            pq.write_to_dataset(
                table,
                root_path=hdfs_path,
                partition_cols=[partition_by],
                use_deprecated_int96_timestamps=use_deprecated_int96_timestamps,
                filesystem=self.hdfs,
                existing_data_behavior=existing_data_behavior
            )

        else:
            table = self._check_series_convert_column_pyarrow(data, partition_by='')
            pq.write_to_dataset(
                table,
                root_path=hdfs_path,
                use_deprecated_int96_timestamps=use_deprecated_int96_timestamps,
                filesystem=self.hdfs,
                existing_data_behavior=existing_data_behavior
            )

