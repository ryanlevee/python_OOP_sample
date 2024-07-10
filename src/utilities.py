from collections import deque

import pandas as pd


class Utility:
    @staticmethod
    def to_list(v):
        return [v] if not isinstance(v, list) else v

    @staticmethod
    def flatten_list(nested, flat):
        if isinstance(nested, list):
            for n in nested:
                Utility.flatten_list(n, flat)
        else:
            flat.append(nested)
        return flat

    @staticmethod
    def split_list(dict_list, chunk, new_list=[]):
        if len(dict_list) > 0:
            new_list.append(dict_list[:chunk])

        if len(dict_list) >= chunk:
            dict_list = dict_list[chunk:]
            return Utility.split_list(dict_list, chunk)

        return new_list

    @staticmethod
    def get_asset_id_dict(db_dict):
        return {k: v for k, v in db_dict.items() if k == 'AssetID'}

    @staticmethod
    def sqlize_dt(dt=pd.Timestamp.now()):
        return (
            'NULL' if not dt or dt == 'NULL' or dt == 'None'
            else pd.to_datetime(
                [dt], format='mixed'
            ).strftime("%Y-%m-%d %H:%M:%S").values[0]
        )

    @staticmethod
    def create_sql_insert_str(dict_list):
        columns_str = ''
        values_str = ''
        xd_keys = list(dict_list[0].keys())

        for i in range(len(xd_keys)):
            columns_str += xd_keys[i]

            if i < len(xd_keys) - 1:
                columns_str += ','

        for i in range(len(dict_list)):
            xd_values = tuple(str(v) for v in dict_list[i].values())
            values_str += str(xd_values)

            if i < len(dict_list) - 1:
                values_str += ','

        result_dict = {'ColumnString': columns_str}
        result_dict |= {'ValueString': values_str}

        return result_dict

    @staticmethod
    def create_asset_id_sql_str(id_list):
        asset_id_str = {'AssetIDString': ', '.join(str(i) for i in id_list)}
        return asset_id_str

    @classmethod
    def create_sql_str(cls, d, proc):
        x_dkv = cls._dict_to_sql_zip(d)
        sql_str = cls._assemble_sql_string(x_dkv)
        if '\\r\\n' in sql_str:
            sql_str = str(sql_str.replace(
                '\\r\\n', '\r\n').encode('utf-8'))[2:-1]
        sql = f"""EXEC {proc} \n{sql_str}""".replace("'NULL'", 'NULL')
        return sql

    def _dict_to_sql_zip(d):
        d_keys = d.keys()
        d_keys = deque(f'@{k}' for k in d_keys)
        d_values = d.values()
        return list(zip(d_keys, d_values))

    def _assemble_sql_string(sql_zip, sql_str=''):
        v_last = sql_zip[-1]
        for v in sql_zip[:-1]:
            sql_str += "=".join(
                [str(v[0]), "'" + str(v[1]).replace("'", "''") + "'"]) + ","
        sql_str += "=".join(
            [str(v_last[0]), "'" + str(v_last[1]).replace("'", "''") + "'"])
        return sql_str.replace("'NULL'", 'NULL')
