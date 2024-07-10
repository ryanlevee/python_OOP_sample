
import asyncio
from collections import deque

import aiohttp

import xmltodict
from config import HISTORICAL_QUERY, HISTORICAL_RUN, NON_HISTORICAL_QUERY
from connect_sql import execute_commit_sql, pymssql_query
from holders import ConfigHolder, DataHolder
from interfaces import IConnectionHolder, IDatabaseOperation, ISoapOperation
from loggers import EventLogger


class XmlGetter(ISoapOperation):
    def __init__(
        self,
        data_holder: DataHolder,
        config_holder: ConfigHolder
    ):
        self.data_holder = data_holder
        self.call = config_holder.call
        self.url = config_holder.url
        self.xml = config_holder.xml_template % '\
        <ns:get{call}><case_id>%i</case_id></ns:get{call}>'
        self.logger = EventLogger()

    @property
    def case_ids(self):
        return self.data_holder.case_ids

    @property
    def xml_data(self):
        return self.data_holder.xml_data

    @xml_data.setter
    def xml_data(self, new_xml_data):
        self.data_holder.xml_data = new_xml_data

    async def execute(self):
        xml_list = await self._get_all_xml()
        self.xml_data = xml_list

    async def _get_all_xml(self):
        async with aiohttp.ClientSession() as session:
            tasks = [
                self._get_xml(session, [i, len(self.case_ids)], id)
                for i, id in enumerate(self.case_ids, 1) if id
            ]
            return await asyncio.gather(*tasks)

    async def _get_xml(self, session, ii, id):
        self.logger.log_info(
            f' {ii[0]} / {ii[1]}:'
            ' Getting xml from 3rd party database...'
        )
        xml_string = self.xml.format(call=self.call) % id

        async with session.post(self.url, data=xml_string) as resp:
            text = await resp.text()
            return xmltodict.parse(text)


class SqlExecutor(IDatabaseOperation):
    def __init__(
        self,
        data_holder: DataHolder,
        conn_holder: IConnectionHolder
    ):
        self.data_holder = data_holder
        self.cnxn_cur = conn_holder.get_cnxn_cur()

    @property
    def sql_string(self):
        return self.data_holder.sql_string

    def execute(self):
        if not self.sql_string:
            return False

        deque(execute_commit_sql(
            sql, self.cnxn_cur) for sql in self.sql_string
        )


class SqlGetter(IDatabaseOperation):
    def __init__(
        self,
        data_holder: DataHolder,
        conn_holder: IConnectionHolder,
        config_holder: ConfigHolder
    ):
        self.data_holder = data_holder
        self.conn = conn_holder.get_conn()
        self.table = config_holder.table
        self.logger = EventLogger()

    @property
    def database_data(self):
        return self.data_holder.database_data

    @database_data.setter
    def database_data(self, new_database_data):
        self.data_holder.database_data = new_database_data

    def execute(self):
        df = pymssql_query(
            self.conn,
            HISTORICAL_QUERY if HISTORICAL_RUN else NON_HISTORICAL_QUERY
        )

        if not HISTORICAL_RUN and df.rowcount == 0:
            self.logger.log_info(f'No new flags in {self.table}.')
            return False

        df = df.fetchall()
        self.database_data = df
        self.logger.log_info(f' Database query returned {len(df)} rows.')
