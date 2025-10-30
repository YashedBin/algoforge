from Timer import Timer
from MemoryProfiler import MemoryProfiler
with Timer("Python Task", emit_json=True), MemoryProfiler("Python Task", emit_json=True):
    pass
