# Installation Guide

## Step 1. Clone the Repository
```
git clone https://github.com/Yashx13/sentiment_analyzer.git
cd sentiment_analyzer
```

---

## Step 2. Install Python Requirements
### Make sure Python 3.10+ is installed
```
pip install -r requirements.txt
# Versions are not fixed; the latest compatible packages will be installed.
```
---

## Step 3. Check Compilers
### Required language toolchains
```
g++ --version
gcc --version
python --version     # or python3 --version
```
### Install missing compilers (Linux / WSL)
```
sudo apt install g++ gcc python3 -y
```
---

## Step 4. Run the Python App

### Windows / Default Environment
```
cd py_app/core
streamlit run app.py
# or
python -m streamlit run app.py
```

### Linux / WSL
```
cd py_app/core
python3 -m streamlit run app.py --server.headless true
```
### Access the app at:
`https://localhost:8501`

### Optional: Run on a custom port
```
python3 -m streamlit run app.py --server.port 8502
```
---

## Step 5. Run Behavior
### - Code wouldn't be bothered if you compile binary but don't
### - Python does it for you
### - Streamlit frontend triggers backend logic automatically

---

## Step 6. Troubleshooting

#### Hard refresh Streamlit cache
####   Focus the app window → press Ctrl + Shift + R

### Fix permission errors (Linux)
```
chmod +x <script>
```

### Change default port if in use
```
python3 -m streamlit run app.py --server.port <port_number>
```
---

+  Supported languages:
###   - C++
###   - Python


---

## Notes
### - Works without version-pinned dependencies
### - Tested on Windows, Linux, and WSL
### - All execution flows through the Orchestrator system
### - Use Streamlit for launching, not direct binaries
