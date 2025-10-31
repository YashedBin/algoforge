import os
import subprocess
import json

class Orchestrator:
    def __init__(self, lang, code):
        self.lang = lang
        self.code = code

    def run(self):
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        cpp_root = os.path.join(base, "cpp_core")
        src_dir = os.path.join(cpp_root, "src")
        bin_dir = os.path.join(cpp_root, "bin")
        headers_dir = os.path.join(cpp_root, "headers")

        os.makedirs(src_dir, exist_ok=True)
        os.makedirs(bin_dir, exist_ok=True)

        env = os.environ.copy()

        if self.lang == "C++":
            file_path = os.path.join(src_dir, "main.cpp")
            exe_path = os.path.join(bin_dir, "main")
            compile_cmd = ["g++", file_path, "-I", headers_dir, "-o", exe_path, "-std=c++11"]
            run_cmd = [exe_path]

        elif self.lang == "C":
            file_path = os.path.join(src_dir, "main.c")
            exe_path = os.path.join(bin_dir, "main")
            compile_cmd = ["gcc", file_path, "-I", headers_dir, "-o", exe_path, "-std=c11"]
            run_cmd = [exe_path]

        elif self.lang == "Python":
            file_path = os.path.join(base, "py_app", "assets", "main.py")
            compile_cmd = None
            run_cmd = ["python3", file_path]
            py_core = os.path.join(base, "py_app", "core")
            env["PYTHONPATH"] = py_core + ":" + env.get("PYTHONPATH", "")

        else:
            return {"status": "error", "message": "Unsupported language"}

        with open(file_path, "w") as f:
            f.write(self.code)

        try:
            if compile_cmd:
                compile_result = subprocess.run(
                    compile_cmd,
                    capture_output=True,
                    text=True,
                    env=env
                )
                if compile_result.returncode != 0:
                    return {
                        "status": "error",
                        "message": "Compilation failed",
                        "stderr": compile_result.stderr,
                        "stdout": compile_result.stdout
                    }

            run_result = subprocess.run(
                run_cmd,
                capture_output=True,
                text=True,
                env=env
            )

            if run_result.returncode != 0:
                return {
                    "status": "error",
                    "message": "Runtime error",
                    "stderr": run_result.stderr,
                    "stdout": run_result.stdout
                }

            output = run_result.stdout or ""
            stderr = run_result.stderr or ""

            metrics_dict = {}
            stdout_lines = []

            for line in output.splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    stdout_lines.append(line)
                    continue

                if not isinstance(obj, dict):
                    stdout_lines.append(str(obj))
                    continue

                if "type" not in obj:
                    stdout_lines.append(line)
                    continue

                work = obj.get("work", "Unknown")
                if work not in metrics_dict:
                    metrics_dict[work] = {
                        "work": work,
                        "duration_ns": 0,
                        "memory_kb": 0,
                        "start_kb": 0,
                        "end_kb": 0
                    }

                t = obj.get("type")
                if t in ("timing", "timer"):
                    if "duration_ns" in obj:
                        metrics_dict[work]["duration_ns"] = obj.get("duration_ns", 0)
                    elif "duration_ms" in obj:
                        metrics_dict[work]["duration_ns"] = int(float(obj["duration_ms"]) * 1e6)
                elif t == "memory":
                    metrics_dict[work]["memory_kb"] = obj.get("delta_kb", obj.get("memory_kb", 0))
                    metrics_dict[work]["start_kb"] = obj.get("start_kb", 0)
                    metrics_dict[work]["end_kb"] = obj.get("end_kb", 0)

            metrics = list(metrics_dict.values())

            return {
                "status": "success",
                "metrics": metrics,
                "stdout": "\n".join(stdout_lines),
                "stderr": stderr
            }

        except subprocess.CalledProcessError as e:
            return {
                "status": "error",
                "message": str(e),
                "stderr": getattr(e, "stderr", ""),
                "stdout": getattr(e, "stdout", "")
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
