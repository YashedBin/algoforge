# AlgoForge — Code Benchmarking System

AlgoForge is a hybrid **C++ + Python** benchmarking framework designed for measuring, visualizing, and analyzing algorithm performance in real time.

> It will help students and programmers evaluate there code's runtime efficiency, memory usage, and computational complexity across multiple algorithms or data structures.

---

## 📘 Background

Benchmarking refers to the process of **measuring code performance** — how fast and efficiently an algorithm runs under given constraints.

AlgoForge provides:
- **Precise timing and memory profiling**
- **Automated C++ execution through Python** Will be more languages soon
- **Modular system** — easily plug in new algorithms for testing

Common metrics used in benchmarking include:
- **Execution Time (ms)** — measures how long code runs
- **Memory Consumption (KB/MB)** — tracks runtime space usage


---

> ### Sorry for the Boilerplates Designed for multi languages 💀
`Survive the se...`

---

## 📂 Project Structure

```
├── README.md
├── cpp_core
│   ├── algos
│   ├── assets          # UI Assests if any
│   ├── bin
│   │   └── main        # Binaries
│   ├── headers
│   │   ├── MemoryProfiler.hpp
│   │   └── Timer.hpp
│   └── src
│       ├── main.c
│       └── main.cpp
├── devlog.md
├── install.md            # Installation guide
├── py_app
│   ├── assets
│   │   └── main.py       # for python
│   └── core
│       ├── MemoryProfiler.py
│       ├── Timer.py
│       ├── app.py
│       └── orchestrator.py
└── requirements.txt
```
---
### JSON Formats will be uplaoded soon
---

## ⚙️ Installation & Setup

Detailed setup instructions are in [`install.md`](./install.md)

> Includes environment configuration, compiler setup, and Streamlit launch commands.

---

## 🧠 Tech Stack

| Component | Purpose |
|------------|----------|
| **C++17** | Core algorithmic logic, timer & memory profilers |
| **Python 3.10+** | Runtime orchestration and frontend layer |
| **Streamlit** | UI for visualization and control |
| **Matplotlib / Pandas** | Optional plotting and data handling |

---

## 🧩 Future Scope

Planned features and improvements:
- Enhanced **sandboxing** for user-provided code
- Dedicated **visualization engine** for performance graphs
- **Runtime analytics** for multi-threaded benchmarks
- Extended **language support** (C, Java, Rust)
- Expanded **algorithm library**
- Exportable **benchmark reports**

---


---


