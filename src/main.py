import asyncio
from datetime import datetime
from time import time

from exceptions import Continue, ProcessingError
from handlers import DataProcessor, EventTypeHandler, SqlHandler, XmlHandler
from holders import ConfigHolder, ConnectionHolder, DataHolder, HolderFactory
from loggers import EventLogger
from operations import SqlExecutor, SqlGetter, XmlGetter
from processors import (AssetIdExtractor, CaseIdExtractor, DataNormalizer,
                        SqlStringCreator, XmlProcessor)
from traceback_logger import traceback_logger


async def main():
    logger = EventLogger()
    logger.log_info(f' {datetime.now()}')
    start = time()

    try:
        conn_holder = HolderFactory.create_holder(ConnectionHolder)
        data_holder = HolderFactory.create_holder(DataHolder)
        config_holder = HolderFactory.create_holder(ConfigHolder)

        sql_getter = SqlGetter(data_holder, conn_holder, config_holder)
        sql_executor = SqlExecutor(data_holder, conn_holder)
        sql_handler = SqlHandler(
            sql_getter,
            sql_executor
        )

        xml_getter = XmlGetter(data_holder, config_holder)
        xml_handler = XmlHandler(
            xml_getter
        )

        case_id_extractor = CaseIdExtractor(data_holder)
        xml_processor = XmlProcessor(data_holder, config_holder)
        asset_id_extractor = AssetIdExtractor(data_holder)
        data_normalizer = DataNormalizer(data_holder)
        sql_string_creator = SqlStringCreator(data_holder, config_holder)
        data_processor = DataProcessor(
            case_id_extractor,
            xml_processor,
            asset_id_extractor,
            data_normalizer,
            sql_string_creator
        )

        handler = EventTypeHandler(
            conn_holder,
            data_holder,
            config_holder,
            sql_handler,
            xml_handler,
            data_processor
        )

        await handler.handle()

    except ProcessingError as pe:
        logger.log_error(f'ProcessingError occurred: {pe}')
    except Exception as ex:
        traceback_logger('FC', ex)
    finally:
        end = time()
        logger.log_info('FC up to date.')
        logger.log_info(
            f'ChildCasePull completed in {round((end - start)/60, 2)} minutes '
            f'on {datetime.now()}.'
        )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as ex:
        traceback_logger('MAIN')
