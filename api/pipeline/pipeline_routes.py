import os
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query

from pipeline.pipeline_service import (
    run_pipeline_background,
    is_pipeline_running,
    get_latest_execution,
    get_execution_history,
)
from auth.auth_utils import get_current_user
from logger_config import logger

router = APIRouter(prefix="/api/pipeline", tags=["Pipeline"])


def _execution_to_dict(execution):
    return {
        "execution_id": execution.execution_id,
        "pipeline_name": execution.pipeline_name,
        "start_time": str(execution.start_time),
        "end_time": str(execution.end_time),
        "status": execution.status,
        "records_processed": execution.records_processed,
        "records_failed": execution.records_failed,
    }


@router.post("/run")
def trigger_pipeline(background_tasks: BackgroundTasks, current_user: dict = Depends(get_current_user)):
    """
    Kicks off the ETL pipeline (Extract -> Validate -> Transform -> Load)
    in the background and returns immediately. Use GET /api/pipeline/status
    afterwards to check progress/result.
    """
    if is_pipeline_running():
        raise HTTPException(
            status_code=409,
            detail="A pipeline run is already in progress. Check /api/pipeline/status.",
        )

    logger.info("POST /api/pipeline/run called")
    background_tasks.add_task(run_pipeline_background)

    return {
        "status": "STARTED",
        "message": "Pipeline started in the background. Poll /api/pipeline/status for progress.",
    }


@router.get("/status")
def pipeline_status():
    """Returns whether a pipeline is currently running, plus the result
    of the most recent completed run (if any)."""
    logger.info("GET /api/pipeline/status called")

    latest = get_latest_execution()

    return {
        "currently_running": is_pipeline_running(),
        "last_execution": _execution_to_dict(latest) if latest else None,
    }


@router.get("/history")
def pipeline_history(limit: int = Query(default=10, ge=1, le=100)):
    """Returns the last `limit` pipeline runs, most recent first."""
    logger.info("GET /api/pipeline/history called")

    executions = get_execution_history(limit=limit)
    return [_execution_to_dict(e) for e in executions]


@router.get("/logs")
def pipeline_logs(lines: int = Query(default=50, ge=1, le=1000)):
    """Returns the last `lines` lines from the pipeline's log file, useful
    for quickly debugging a failed run without SSH-ing into the server."""
    logger.info("GET /api/pipeline/logs called")

    log_path = "logs/pipeline.log"
    if not os.path.exists(log_path):
        return {"lines": []}

    with open(log_path, "r", encoding="utf-8", errors="replace") as f:
        all_lines = f.readlines()

    return {"lines": [line.rstrip("\n") for line in all_lines[-lines:]]}
