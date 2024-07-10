from holders import DataHolder, HolderFactory
from interfaces import (IConnectionHolder, IDatabaseOperation, IDataProcessor,
                        ISoapOperation)
from operations import SqlExecutor, SqlGetter, XmlGetter
from processors import (CaseIdExtractor, DataNormalizer, SqlStringCreator,
                        XmlProcessor)


class SqlHandler:
    def __init__(
        self,
        sql_getter: SqlGetter,
        sql_executor: SqlExecutor
    ):
        self.sql_getter = sql_getter
        self.sql_executor = sql_executor

    def get_sql(self):
        self.sql_getter.execute()

    def execute_sql(self):
        self.sql_executor.execute()


class XmlHandler:
    def __init__(
        self,
        xml_getter: XmlGetter
    ):
        self.xml_getter = xml_getter

    def get_xml(self):
        return self.xml_getter.execute()


class DataProcessor:
    def __init__(
        self,
        case_id_extractor: CaseIdExtractor,
        xml_processor: XmlProcessor,
        asset_id_extractor: CaseIdExtractor,
        data_normalizer: DataNormalizer,
        sql_string_creator: SqlStringCreator
    ):
        self.case_id_extractor = case_id_extractor
        self.xml_processor = xml_processor
        self.asset_id_extractor = asset_id_extractor
        self.data_normalizer = data_normalizer
        self.sql_string_creator = sql_string_creator

    def extract_case_ids(self):
        self.case_id_extractor.process()

    def process_xml(self):
        self.xml_processor.process()

    def extract_asset_ids(self):
        self.asset_id_extractor.process()

    def normalize_data(self):
        self.data_normalizer.process()

    def create_sql_string(self):
        self.sql_string_creator.process()


class EventTypeHandler:
    def __init__(
            self,
            conn_holder: IConnectionHolder,
            data_holder: DataHolder,
            config_holder: HolderFactory,
            sql_handler: IDatabaseOperation,
            xml_handler: ISoapOperation,
            data_processor: IDataProcessor
    ):
        self.conn_holder = conn_holder
        self.data_holder = data_holder
        self.config_holder = config_holder
        self.sql_handler = sql_handler
        self.xml_handler = xml_handler
        self.data_processor = data_processor

    async def handle(self):
        self.sql_handler.get_sql()
        self.data_processor.extract_case_ids()
        await self.xml_handler.get_xml()
        self.data_processor.process_xml()
        self.data_processor.extract_asset_ids()
        self.data_processor.normalize_data()
        self.data_processor.create_sql_string()
        self.sql_handler.execute_sql()
