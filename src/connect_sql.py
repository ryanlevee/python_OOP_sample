import inspect

import pymssql

import interval_timer
from config import ARS_STATUS, PYMSSQL_STR_LIVE, PYMSSQL_STR_TEST
from loggers import EventLogger
from traceback_logger import traceback_logger

pymssql_str = PYMSSQL_STR_LIVE if ARS_STATUS == 'LIVE' else PYMSSQL_STR_TEST

logger = EventLogger()

def connection():
    logger.log_info('Connecting to SQL database...')
    sec = 60
    try:
        cnxn = pymssql.connect(
            server=pymssql_str[0],
            user=pymssql_str[1],
            password=pymssql_str[2],
            database=pymssql_str[3]
        )
        cur = cnxn.cursor()
        return cnxn, cur
    except Exception:
        logger.log_error(inspect.stack()[1].function)
        logger.log_error('SQL Server timed out. '
              f'Trying again in {round(sec/60, 2)} minutes...')
        traceback_logger('SQL')
        interval_timer.set_interval(connection, sec)


def pymssql_conn():
    # logger.log_info("pymssql_conn connecting...")
    try:
        conn = pymssql.connect(
            server=pymssql_str[0],
            user=pymssql_str[1],
            password=pymssql_str[2],
            database=pymssql_str[3]
        )
    except Exception as e:
        logger.log_error('exception:', e)
    return conn


def pymssql_query(conn, sql_str):
    # logger.log_info("pymssql_query executing...")
    # logger.log_info(sql_str,'\n')
    try:
        cur = conn.cursor(as_dict=True)
        cur.execute(sql_str)
    except Exception as e:
        logger.log_error('pymssql_query exception:', e)

    return cur


def execute_commit_sql(sql, cnxn_cur):
    logger.log_info(f'{sql}\n')
    cnxn_cur[1].execute(sql)
    cnxn_cur[0].commit()
