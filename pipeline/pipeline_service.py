"""
Wraps pipeline/run_pipeline.py so it can be triggered from an API call.

Every run is recorded in the `pipeline_execution` table (already defined
in models/models.py) so we have a history of every pipeline run - when
it started, when it finished, whether it succeeded, and how many
records were processed vs failed. This also lets the API answer
"is a pipeline running right now?" without needing any extra
infrastructure like Celery or Redis.
"""

from datetime import date

from database.database_connection import sessionLocal
from models.models import PipelineExecution
from pipeline.run_pipeline import run_pipeline
from logger_config import logger

PIPELINE_NAME = "enterprise_retail_pipeline"

# Simple in-memory flag so we can reject a second run while one is
# already in progress (prevents two runs writing to the DB at once).
_pipeline_running = {"status": False}


def is_pipeline_running() -> bool:
    return _pipeline_running["status"]


def _record_execution(status: str, records_processed: int, records_failed: int):
    """Insert one row into pipeline_execution for this run."""
    session = sessionLocal()
    try:
        execution = PipelineExecution(
            pipeline_name=PIPELINE_NAME,
            start_time=date.today(),
            end_time=date.today(),
            status=status,
            records_processed=records_processed,
            records_failed=records_failed,
        )
        session.add(execution)
        session.commit()
    except Exception as e:
        session.rollback()
        logger.exception(f"Failed to record pipeline execution: {e}")
    finally:
        session.close()


def run_pipeline_background():
    """
    Meant to be called via FastAPI's BackgroundTasks so the API can
    respond immediately instead of making the caller wait for the
    whole ETL run to finish.
    """
    if _pipeline_running["status"]:
        logger.warning("Pipeline trigger ignored - a run is already in progress")
        return

    _pipeline_running["status"] = True
    try:
        logger.info("Pipeline triggered via API")
        result = run_pipeline()
        _record_execution(
            status="SUCCESS",
            records_processed=result.get("total_records_loaded", 0),
            records_failed=result.get("total_records_rejected", 0),
        )
    except Exception as e:
        logger.exception(f"Pipeline run triggered via API failed: {e}")
        _record_execution(status="FAILED", records_processed=0, records_failed=0)
    finally:
        _pipeline_running["status"] = False


def get_latest_execution():
    """Return the most recent pipeline_execution row, or None if the
    pipeline has never been run."""
    session = sessionLocal()
    try:
        return (
            session.query(PipelineExecution)
            .order_by(PipelineExecution.execution_id.desc())
            .first()
        )
    finally:
        session.close()


def get_execution_history(limit: int = 10):
    """Return the last `limit` pipeline_execution rows, most recent first."""
    session = sessionLocal()
    try:
        return (
            session.query(PipelineExecution)
            .order_by(PipelineExecution.execution_id.desc())
            .limit(limit)
            .all()
        )
    finally:
        session.close()
