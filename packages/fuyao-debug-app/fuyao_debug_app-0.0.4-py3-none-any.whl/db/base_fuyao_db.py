import configparser
import os
import logging
import traceback

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from .fuyao_run_info_tbl import FuyaoRunInfoTbl

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '../', 'config.properties'))

DB_URI_FUYAO_MGMT = config['DB_INFO']['FUYAO_MGMT_DB_SERVER']
db_engine_fuyao_mgmt = create_engine(DB_URI_FUYAO_MGMT)
Session_fuyao_mgmt = sessionmaker(bind=db_engine_fuyao_mgmt)
session_fuyao_mgmt = scoped_session(Session_fuyao_mgmt)


def get_job_info(job_name):
    try:
        db_session = session_fuyao_mgmt()
        job_info = (
            db_session.query(
                FuyaoRunInfoTbl.experiment_id,
                FuyaoRunInfoTbl.run_name,
                FuyaoRunInfoTbl.time_start,
                FuyaoRunInfoTbl.time_end,
                FuyaoRunInfoTbl.node_list,
                FuyaoRunInfoTbl.state,
                FuyaoRunInfoTbl.experiment_name,
                FuyaoRunInfoTbl.user_name,
                FuyaoRunInfoTbl.partition,
            )
            .filter(and_(FuyaoRunInfoTbl.run_name == job_name))
            .order_by(FuyaoRunInfoTbl.time_start.asc())
            .first()
        )
        db_session.close()

        return job_info, 200
    except SQLAlchemyError as e:
        db_session.rollback()
        logging.info(str(e))
        logging.info("Create fuyao failed job failed")
        return None, 500
    except Exception:
        logging.info("get job info failed.")
        logging.info(str(traceback.format_exc()))
        return [], 400
