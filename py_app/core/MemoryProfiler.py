import os
import json

class MemoryProfiler:
    def __init__(self, work_done, emit_json=False):
        self.work_done = work_done
        self.emit_json = emit_json
        self.start_memory_kb = None
        
    def _get_memory_kb(self):
        """
        Now Here we share the same logic as C++'s MemoryProfiler 
        getting that C defined functions from os and reading htat statm 
        """
        try:
            # Linux/Unix
            if os.path.exists('/proc/self/statm'):
                with open('/proc/self/statm', 'r') as f:
                    # Second value is RSS in pages
                    pages = int(f.read().split()[1])
                    page_size = os.sysconf('SC_PAGE_SIZE')
                    return (pages * page_size) // 1024
            else:
                
                """
                Else it is again resource like resource.h for windows
                """
                import resource
                rusage = resource.getrusage(resource.RUSAGE_SELF)
                
                if os.uname().sysname == 'Darwin':
                    return rusage.ru_maxrss // 1024
                else:
                    return rusage.ru_maxrss
        except:
            return 0
    
    def __enter__(self):
        self.start_memory_kb = self._get_memory_kb()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        end_memory_kb = self._get_memory_kb()
        delta_kb = end_memory_kb - self.start_memory_kb
        
        if self.emit_json:
            print(json.dumps({
                "type": "memory",
                "work": self.work_done,
                "start_kb": self.start_memory_kb,
                "end_kb": end_memory_kb,
                "delta_kb": delta_kb
            }))
        else:
            print(f"{self.work_done}")
            print(f"Memory Start: {self.start_memory_kb} KB")
            print(f"Memory End: {end_memory_kb} KB")
            print(f"Memory Delta: {delta_kb} KB")
        
        return False