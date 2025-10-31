import time
import json

"""
Nothing special for this Class it is just again a SCOPED based
with time and yea Glad i saw some classmate code for that perfcounterns()"""

class Timer:
    def __init__(self, work_done, emit_json=False):
        self.work_done = work_done
        self.emit_json = emit_json
        self.start_time = None
        
    def __enter__(self):
        self.start_time = time.perf_counter_ns()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        end_time = time.perf_counter_ns()
        duration_ns = end_time - self.start_time
        
        if self.emit_json:
            print(json.dumps({
                "type": "timing",
                "work": self.work_done,
                "duration_ns": duration_ns
            }))
        else:
            print(f"{self.work_done}")
            print(f"Time: {duration_ns / 1e6:.3f} ms")
        
        return False