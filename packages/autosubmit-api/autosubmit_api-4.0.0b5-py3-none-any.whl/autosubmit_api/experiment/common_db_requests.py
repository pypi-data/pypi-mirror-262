import os
import traceback
import sqlite3
from datetime import datetime

from autosubmit_api.config.basicConfig import APIBasicConfig
APIBasicConfig.read()

DB_FILE_AS_TIMES = os.path.join(APIBasicConfig.DB_DIR, APIBasicConfig.AS_TIMES_DB) # "/esarchive/autosubmit/as_times.db"
DB_FILES_STATUS = os.path.join(APIBasicConfig.LOCAL_ROOT_DIR, "as_metadata", "test", APIBasicConfig.FILE_STATUS_DB) # "/esarchive/autosubmit/as_metadata/test/status.db"
# PATH_DB_DATA = "/esarchive/autosubmit/as_metadata/data/"


# STATUS ARCHIVE

def insert_archive_status(status, alatency, abandwidth, clatency, cbandwidth, rtime):

    try:
        conn = create_connection(DB_FILES_STATUS)
        sql = ''' INSERT INTO archive_status(status, avg_latency, avg_bandwidth, current_latency, current_bandwidth, response_time, modified ) VALUES(?,?,?,?,?,?,?)'''
        # print(row_content)
        cur = conn.cursor()
        cur.execute(sql, (int(status), alatency, abandwidth, clatency,
                          cbandwidth, rtime, datetime.today().strftime('%Y-%m-%d-%H:%M:%S')))
        # print(cur)
        conn.commit()
        return cur.lastrowid
    except Exception as exp:
        print((traceback.format_exc()))
        print(("Error on Insert : " + str(exp)))


def get_last_read_archive_status():
    """

    :return: status, avg. latency, avg. bandwidth, current latency, current bandwidth, response time, date
    :rtype: 7-tuple
    """
    try:
        conn = create_connection(DB_FILES_STATUS)
        sql = "SELECT status, avg_latency, avg_bandwidth, current_latency, current_bandwidth, response_time, modified FROM archive_status order by rowid DESC LIMIT 1"
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        status, alatency, abandwidth, clatency, cbandwidth, rtime, date = rows[0]
        return (status, alatency, abandwidth, clatency, cbandwidth, rtime, date)
        # print(rows)
    except Exception as exp:
        print((traceback.format_exc()))
        print(("Error on Get Last : " + str(exp)))
        return (False, None, None, None, None, None, None)

# INSERTIONS

def create_connection(db_file):
    # type: (str) -> sqlite3.Connection
    """
    Create a database connection to the SQLite database specified by db_file.
    :param db_file: database file name
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as exp:
        print(exp)


# SELECTS

def get_experiment_status():
    """
    Gets table experiment_status as dictionary
    conn is expected to reference as_times.db
    """
    # conn = create_connection(DB_FILE_AS_TIMES)
    experiment_status = dict()
    current_table = _get_exp_status()
    for item in current_table:
        exp_id, name, status, seconds_diff = item
        experiment_status[name] = status
    return experiment_status


def get_specific_experiment_status(expid):
    """
    Gets the current status from database.\n
    :param expid: Experiment name
    :type expid: str
    :return: name of experiment and status
    :rtype: 2-tuple (name, status)
    """
    exp_id, name, status, seconds_diff = _get_specific_exp_status(expid)
    print(("{} {} {} {}".format(exp_id, name, status, seconds_diff)))
    return (name, status)


def _get_exp_status():
    """
    Get all registers from experiment_status.\n
    :return: row content: exp_id, name, status, seconds_diff
    :rtype: 4-tuple (int, str, str, int)
    """
    try:
        conn = create_connection(os.path.join(APIBasicConfig.DB_DIR, APIBasicConfig.AS_TIMES_DB))
        conn.text_factory = str
        cur = conn.cursor()
        cur.execute(
            "SELECT exp_id, name, status, seconds_diff FROM experiment_status")
        rows = cur.fetchall()
        return rows
    except Exception as exp:
        print((traceback.format_exc()))
        return dict()


def _get_specific_exp_status(expid):
    """
    Get all registers from experiment_status.\n
    :return: row content: exp_id, name, status, seconds_diff
    :rtype: 4-tuple (int, str, str, int)
    """
    try:
        # print("Honk")
        conn = create_connection(os.path.join(APIBasicConfig.DB_DIR, APIBasicConfig.AS_TIMES_DB))
        cur = conn.cursor()
        cur.execute(
            "SELECT exp_id, name, status, seconds_diff FROM experiment_status WHERE name=?", (expid,))
        row = cur.fetchone()
        if row == None:
            return (0, expid, "NOT RUNNING", 0)
        # print(row)
        return row
    except Exception as exp:
        print((traceback.format_exc()))
        return (0, expid, "NOT RUNNING", 0)


# UPDATES
