# orchestrator.py
import os
import subprocess
import json

class Orchestrator:
    def __init__(self, lang, code):
        self.lang = lang
        self.code = code

    def run(self):
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        # path variable from os's paths then we have 
        # main.c  , main.cpp  , main.py   , main.java 
        # are files which are files used for User's code to be written in
        cpp_root = os.path.join(base, "cpp_core")
        src_dir = os.path.join(cpp_root, "src")
        bin_dir = os.path.join(cpp_root, "bin")

        # 
        headers_dir = os.path.join(cpp_root, "headers")

        os.makedirs(src_dir, exist_ok=True)
        os.makedirs(bin_dir, exist_ok=True)

        if self.lang == "C++":
            file_path = os.path.join(src_dir, "main.cpp")
            exe_path = os.path.join(bin_dir, "main")
            compile_cmd = ["g++", file_path, "-I", headers_dir, "-o", exe_path]
            run_cmd = [exe_path]
        elif self.lang == "C":
            file_path = os.path.join(src_dir, "main.c")
            exe_path = os.path.join(bin_dir, "main")
            compile_cmd = ["gcc", file_path, "-I", headers_dir, "-o", exe_path]
            run_cmd = [exe_path]
        elif self.lang == "Python":
            file_path = os.path.join(base, "py_app", "assets", "main.py")
            compile_cmd = None
            run_cmd = ["python3", file_path]
        else:
            return {"status": "error", "message": "Unsupported language"}

        with open(file_path, "w") as f:
            f.write(self.code)

        try:
            if compile_cmd:
                subprocess.run(compile_cmd, check=True)
            output = subprocess.check_output(run_cmd, text=True)
            result = {}
            for line in output.splitlines():
                try:
                    obj = json.loads(line.strip())
                    if obj["type"] == "timing":
                        result["duration_ns"] = obj["duration_ns"]
                    elif obj["type"] == "memory":
                        result["memory_kb"] = obj["delta_kb"]
                except:
                    pass
            return {"status": "success", **result}
        except subprocess.CalledProcessError as e:
            return {"status": "error", "message": e.stderr or str(e)}
        except Exception as e:
            return {"status": "error", "message": str(e)}
