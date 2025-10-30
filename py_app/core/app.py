# app.py
import streamlit as st
import matplotlib.pyplot as plt
from orchestrator import Orchestrator
import time

st.set_page_config(page_title="AlgoForge - Benchmark Tool", layout="centered")
st.title("⚙️ AlgoForge - Simple Benchmark System")

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
    "C": """#include <MemoryProfiler.hpp>
#include <Timer.hpp>
int main(){
    Timer t("C Task", true);
    MemoryProfiler m("C Task", true);
    // Your code
    return 0;
}
""",
    "Python": """from Timer import Timer
from MemoryProfiler import MemoryProfiler
with Timer("Python Task", emit_json=True), MemoryProfiler("Python Task", emit_json=True):
    pass
"""
}

lang = st.selectbox("Language", ["C++", "C", "Python"])
uploaded = st.file_uploader("Upload Code", type=["cpp", "c", "py"])
code = uploaded.read().decode("utf-8") if uploaded else defaults[lang]

code_area = st.text_area("Editor", code, height=300)
run = st.button("▶ Run Benchmark")

if run:
    with st.spinner("Running..."):
        orc = Orchestrator(lang, code_area)
        result = orc.run()
        time.sleep(0.3)

        if result["status"] != "success":
            st.error(result.get("message", "Error"))
        else:
            t = result.get("duration_ns", 0) / 1e6
            m = result.get("memory_kb", 0)
            st.success(f"✅ Done! Time: {t:.3f} ms | Memory: {m} KB")

            fig, ax = plt.subplots(figsize=(4, 2.5))
            ax.bar(["Time (ms)", "Memory (KB)"], [t, m], color=["#1f77b4", "#ff7f0e"])
            ax.grid(axis="y", linestyle="--", alpha=0.4)
            st.pyplot(fig)

