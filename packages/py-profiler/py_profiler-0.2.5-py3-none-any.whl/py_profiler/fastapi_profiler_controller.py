from fastapi import APIRouter

from .measure_service import profiling_service

#
# @author: andy
#
profiler_router = APIRouter()


@profiler_router.get("/profiler")
def index():
    return profiling_service.as_html()
