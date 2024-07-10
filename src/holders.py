from dataclasses import dataclass, field
from typing import Any

from config import (CCF_TABLE, FAULT_STRING, FC, FC_KEY, FLAG_HOUR_LIMIT,
                    NS1_RESPONSE, PC_CC_UPSERT_PROC, RETURN_KEY, SOAP_BODY,
                    SOAP_ENV, SOAP_FAULT, SQL_INSERT_LIMIT, URL, XML_TEMPLATE)
from connect_sql import connection, pymssql_conn
from interfaces import IConnectionHolder

CALL = FC
KEYS = FC_KEY
PROC = PC_CC_UPSERT_PROC
TABLE = CCF_TABLE


@dataclass
class ConfigHolder:
    call: str = CALL
    keys: list = field(default_factory=lambda: list(KEYS))
    proc: str = PROC
    table: str = TABLE
    url: str = URL
    xml_template: str = XML_TEMPLATE
    flag_hour_limit: int = FLAG_HOUR_LIMIT
    sql_insert_limit: int = SQL_INSERT_LIMIT
    soap_env: str = SOAP_ENV
    soap_body: str = SOAP_BODY
    ns1_response: str = NS1_RESPONSE
    return_key: str = RETURN_KEY
    soap_fault: str = SOAP_FAULT
    fault_string: str = FAULT_STRING


@dataclass
class DataHolder:
    database_data: Any = None
    case_ids: list = field(default_factory=lambda: [])
    asset_ids: list = field(default_factory=lambda: [])
    xml_data: Any = None
    sql_string: str = None


class ConnectionHolder(IConnectionHolder):
    def __init__(self):
        self.cnxn_cur, self.conn = (
            connection(),
            pymssql_conn()
        )

    def get_conn(self):
        return self.conn

    def get_cnxn_cur(self):
        return self.cnxn_cur


class HolderFactory:
    holder_dict = {
        ConnectionHolder: ConnectionHolder(),
        DataHolder: DataHolder(),
        ConfigHolder: ConfigHolder()
    }

    @staticmethod
    def create_holder(holder_type):
        if holder_type in HolderFactory.holder_dict:
            return HolderFactory.holder_dict[holder_type]
        else:
            raise ValueError('Invalid holder type')
