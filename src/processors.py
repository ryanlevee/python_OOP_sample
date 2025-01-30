import itertools

from config import HISTORICAL_RUN
from exceptions import ProcessingError
from holders import ConfigHolder, DataHolder
from interfaces import IDataProcessor
from loggers import EventLogger
from utilities import Utility


class SqlStringCreator(IDataProcessor):
    def __init__(
        self,
        data_holder: DataHolder,
        config_holder: ConfigHolder
    ):
        self.data_holder = data_holder
        self.proc = config_holder.proc
        self.sql_insert_limit = config_holder.sql_insert_limit

    @property
    def asset_ids(self):
        return self.data_holder.asset_ids

    @property
    def xml_data(self):
        return self.data_holder.xml_data

    @xml_data.setter
    def xml_data(self, new_xml_data):
        self.data_holder.xml_data = new_xml_data

    @property
    def sql_string(self):
        return self.data_holder.sql_string

    @sql_string.setter
    def sql_string(self, new_sql_string):
        self.data_holder.sql_string = new_sql_string

    def process(self):
        sql_dict_list = [{}]

        if any(self.xml_data):
            split_data = Utility.split_list(
                self.xml_data, self.sql_insert_limit
            )
            sql_dict_list = [
                Utility.create_sql_insert_str(data)
                for data in split_data
            ]

        if not HISTORICAL_RUN and self.asset_ids:
            sql_dict_list[-1] |= Utility.create_asset_id_sql_str(
                self.asset_ids
            )

        if not any(sql_dict_list):
            return False

        result_sql_list = (
            Utility.create_sql_str(sql_dict, self.proc)
            for sql_dict in sql_dict_list
        )

        self.sql_string = result_sql_list


class DataNormalizer(IDataProcessor):
    def __init__(
        self,
        data_holder: DataHolder
    ):
        self.data_holder = data_holder

    @property
    def xml_data(self):
        return self.data_holder.xml_data

    @xml_data.setter
    def xml_data(self, new_xml_data):
        self.data_holder.xml_data = new_xml_data

    def process(self):
        if not any(self.xml_data):
            return False

        try:
            self.modified_xml_data = []
            self._normalize_data()
            self.xml_data = self.modified_xml_data
        except Exception as e:
            raise ProcessingError(f'Error while normalizing data: {e}')

    def _normalize_data(self):
        self.modified_xml_data = [
            self._normalize_values(xd) for xd in self.xml_data
        ]

    def _normalize_values(self, xd):
        return {
            k: 'NULL'
            if isinstance(v, dict) or v == 'None' else Utility.sqlize_dt(v)
            if 'date' in str(k) and not isinstance(v, dict) else v
            for k, v in xd.items()
        }


class XmlProcessor(IDataProcessor):
    def __init__(
        self,
        data_holder: DataHolder,
        config_holder: ConfigHolder
    ):
        self.data_holder = data_holder
        self.call = config_holder.call
        self.keys = config_holder.keys
        self.logger = EventLogger()
        self.soap_env = config_holder.soap_env
        self.soap_body = config_holder.soap_body
        self.ns1_response = config_holder.ns1_response
        self.return_key = config_holder.return_key
        self.soap_fault = config_holder.soap_fault
        self.fault_string = config_holder.fault_string
        self.flag_hour_limit = config_holder.flag_hour_limit

    @property
    def asset_ids(self):
        return self.data_holder.asset_ids

    @property
    def database_data(self):
        return self.data_holder.database_data

    @database_data.setter
    def database_data(self, new_database_data):
        self.data_holder.database_data = new_database_data

    @property
    def xml_data(self):
        return self.data_holder.xml_data

    @xml_data.setter
    def xml_data(self, new_xml_data):
        self.data_holder.xml_data = new_xml_data

    def process(self):
        try:
            self.result_xml_data = self.xml_data
            self.result_database_data = self.database_data
            self._extract_xml_data()
            self._extract_xml_data_by_keys()
            self._verify_xml_data()
            self.xml_data = self.result_xml_data
            self.database_data = self.result_database_data
        except Exception as e:
            raise ProcessingError(f'{self._extract_xml_fault_string(e)}')

    def _extract_xml_data(self):
        self.result_xml_data = [
            d[self.soap_env][self.soap_body]
            [self.ns1_response.format(call=self.call)]
            [self.return_key] for d in self.xml_data
        ]

    def _extract_xml_data_by_keys(self):
        if self.keys and any(self.result_xml_data):
            self.result_xml_data = self._navigate_keys()

    def _navigate_keys(self):
        return (
            (
                [d[key] for d in rd[key]]
                if isinstance(rd[key], tuple) else [rd[key]]
                if isinstance(rd[key], dict) else rd[key]
            )
            if rd is not None else []
            for rd in self.result_xml_data
            for key in self.keys
        )

    def _verify_xml_data(self):
        result_xml_list = []
        result_db_list = []

        for x_data, db_data in itertools.zip_longest(
            self.result_xml_data,
            self.result_database_data,
            fillvalue={}
        ):
            x_data = Utility.to_list(x_data)
            flag_hours = db_data.get('flag_last_on_hrs') or 0

            if not self._check_flag_hours(x_data, db_data, flag_hours):
                continue

            if any(x_data):
                asset_id_dict = Utility.get_asset_id_dict(db_data)
                x_data = ({**xd, **asset_id_dict} for xd in x_data)

            result_xml_list.extend(x_data)
            result_db_list.append(db_data)

        self.result_xml_data = filter(lambda x: x, result_xml_list)
        self.result_database_data = result_db_list

    def _check_flag_hours(self, xml_d, db_dict, flag_hours):
        if (
            not HISTORICAL_RUN
            and not any(xml_d)
            and flag_hours < self.flag_hour_limit
        ):
            self.logger.log_info(
                f' {db_dict.get('AssetID')} /'
                f' {db_dict.get('Case_ID') or "N/A"} ->'
                f' no child cases but less than {self.flag_hour_limit} hours.'
            )
            return False
        return True

    def _extract_xml_fault_string(self, error):
        return f'{error}: {
            self.xml_data[self.soap_env][self.soap_body]
            [self.soap_fault][self.fault_string]
        }'


class AssetIdExtractor(IDataProcessor):
    def __init__(
            self,
            data_holder: DataHolder
    ):
        self.data_holder = data_holder

    @property
    def database_data(self):
        return self.data_holder.database_data

    @property
    def asset_ids(self):
        return self.data_holder.asset_ids

    @asset_ids.setter
    def asset_ids(self, new_asset_ids):
        self.data_holder.asset_ids = new_asset_ids

    def process(self):
        self.asset_ids.extend(d['AssetID'] for d in self.database_data)


class CaseIdExtractor(IDataProcessor):
    def __init__(
            self,
            data_holder: DataHolder
    ):
        self.data_holder = data_holder

    @property
    def database_data(self):
        return self.data_holder.database_data

    @property
    def case_ids(self):
        return self.data_holder.case_ids

    @case_ids.setter
    def case_ids(self, new_case_ids):
        self.data_holder.case_ids = new_case_ids

    def process(self):
        self.case_ids.extend(d['Case_ID'] for d in self.database_data)
