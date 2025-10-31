import streamlit as st
import matplotlib.pyplot as plt
from orchestrator import Orchestrator
import time
import os
import pandas as pd

st.set_page_config(page_title="AlgoForge - Benchmark Tool", layout="centered")
st.title("AlgoForge - Benchmark System")

if "history" not in st.session_state:
    st.session_state.history = []

defaults = {
    "C++": """#include <MemoryProfiler.hpp>
#include <Timer.hpp>
int main(){
Timer t("C++ Task", true);
MemoryProfiler m("C++ Task", true);
// Your code
return 0;
}
""",
    "C": """#include <MemoryProfiler.h>
#include <Timer.h>
int main(){
Timer t = Timer_create("C Task", 1);
MemoryProfiler m = MemoryProfiler_create("C Task", 1);
// Your code
Timer_destroy(&t);
MemoryProfiler_destroy(&m);
return 0;
}
""",
    "Python": """from Timer import Timer
from MemoryProfiler import MemoryProfiler
with Timer("Python Task", emit_json=True), MemoryProfiler("Python Task", emit_json=True):
    pass
"""
}


# Few Pre-Defined algorithms uploaded from our Project curriculum to test compilations/integrity and more
ALGOS = {
    "C++": {
        "Kadane": "cpp_core/algos/kadane.cpp",
        "Kruskal": "cpp_core/algos/kruskal.cpp",
        "Max Sum Array (D&C)": "cpp_core/algos/max_sum_array.cpp"
    }
}

lang = st.selectbox("Language", ["C++", "C", "Python"])
use_predefined = st.checkbox("Use Predefined Algorithm")


# in ALGOS the algorithm paths must be under a langauge so its USer' Friendly
if use_predefined and lang in ALGOS:
    algo_name = st.selectbox("Select Algorithm", list(ALGOS[lang].keys()))
    algo_path = ALGOS[lang][algo_name]
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    full_path = os.path.join(base, algo_path)
    try:
        with open(full_path, "r") as f:
            code = f.read()
        st.info(f"Loaded: {algo_name}")
    except:
        code = defaults[lang]
        st.warning("Could not load algorithm, using default.")
else:
    uploaded = st.file_uploader("Upload Code", type=["cpp", "c", "py"])
    code = uploaded.read().decode("utf-8") if uploaded else defaults[lang]

code_area = st.text_area("Editor", code, height=300)

"""
After this line its all formatting for Data taken afte running Code
and Graph formatting
"""
col1, col2 = st.columns([1, 1])
with col1:
    run = st.button("Run Benchmark")
with col2:
    clear = st.button("Clear History")

if clear:
    st.session_state.history = []
    st.rerun()

if run:
    with st.spinner("Running..."):
        # This is where the real call is for Running the code
        orc = Orchestrator(lang, code_area)
        result = orc.run()
        time.sleep(0.3)

        if result.get("status") != "success":
            st.error(result.get("message", "Error"))
            if result.get("stderr"):
                st.subheader("Error Output")
                st.code(result["stderr"], language="bash")
        else:
            metrics = result.get("metrics", [])
            if isinstance(metrics, dict):
                metrics = [metrics]
            elif not isinstance(metrics, list):
                metrics = []

            stdout = result.get("stdout", "")
            stderr = result.get("stderr", "")

            if metrics:
                st.success(f"Found {len(metrics)} measurement(s)")

                cols = st.columns(max(1, len(metrics)))
                for i, metric in enumerate(metrics):
                    with cols[i % len(cols)]:
                        work = metric.get("work", f"Task {i+1}")
                        t = metric.get("duration_ns", 0) / 1e6
                        m = metric.get("memory_kb", 0)
                        st.subheader(work)
                        st.write(f"Time: {t:.3f} ms")
                        st.write(f"Memory: {m} KB")

                st.session_state.history.append({
                    "timestamp": time.strftime("%H:%M:%S"),
                    "lang": lang,
                    "metrics": metrics
                })

                chart_data = []
                for m in metrics:
                    chart_data.append({
                        "Task": m.get("work", "Task"),
                        "Time_ms": m.get("duration_ns", 0) / 1e6,
                        "Memory_KB": m.get("memory_kb", 0)
                    })
                df = pd.DataFrame(chart_data)

                col1, col2 = st.columns(2)
                with col1:
                    st.write("Execution Time")
                    fig1 = plt.figure(figsize=(5, 3))
                    plt.bar(df["Task"], df["Time_ms"], color="#1f77b4")
                    plt.ylabel("Time (ms)")
                    plt.grid(axis="y", alpha=0.3)
                    st.pyplot(fig1, clear_figure=True)
                with col2:
                    st.write("Memory Usage")
                    fig2 = plt.figure(figsize=(5, 3))
                    plt.bar(df["Task"], df["Memory_KB"], color="#ff7f0e")
                    plt.ylabel("Memory (KB)")
                    plt.grid(axis="y", alpha=0.3)
                    st.pyplot(fig2, clear_figure=True)
            else:
                st.warning("No metrics found in output.")

            if stdout.strip():
                st.subheader("Standard Output")
                st.code(stdout, language="text")
            if stderr.strip():
                st.subheader("Standard Error")
                st.code(stderr, language="bash")

