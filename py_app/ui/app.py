"""
AlgoForge - Algorithm Benchmark & Visualization System
Professional PyQt6 Interface
"""

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit, QTabWidget, QFileDialog, 
    QFrame, QSplitter, QComboBox, QStatusBar, QGroupBox, QMessageBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QTextCharFormat, QColor, QSyntaxHighlighter
import sys
import json

# ============ THEME CONSTANTS ============
class Theme:
    # Dark Theme
    DARK_BG = "#0D1117"
    DARK_BG_SECONDARY = "#161B22"
    DARK_BG_TERTIARY = "#21262D"
    DARK_TEXT = "#C9D1D9"
    DARK_TEXT_SECONDARY = "#8B949E"
    DARK_ACCENT = "#58A6FF"
    DARK_SUCCESS = "#3FB950"
    DARK_BORDER = "#30363D"
    
    # Light Theme
    LIGHT_BG = "#FFFFFF"
    LIGHT_BG_SECONDARY = "#F6F8FA"
    LIGHT_BG_TERTIARY = "#EFF1F3"
    LIGHT_TEXT = "#24292F"
    LIGHT_TEXT_SECONDARY = "#57606A"
    LIGHT_ACCENT = "#0969DA"
    LIGHT_SUCCESS = "#1A7F37"
    LIGHT_BORDER = "#D0D7DE"


# ============ SYNTAX HIGHLIGHTER ============
class CppHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.keywords = [
            'int', 'float', 'double', 'char', 'void', 'bool',
            'if', 'else', 'while', 'for', 'return', 'include',
            'class', 'struct', 'namespace', 'using', 'const'
        ]
        
    def highlightBlock(self, text):
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#FF79C6"))
        keyword_format.setFontWeight(QFont.Weight.Bold)
        
        for word in self.keywords:
            index = 0
            while index >= 0:
                index = text.find(word, index)
                if index >= 0:
                    self.setFormat(index, len(word), keyword_format)
                    index += len(word)


# ============ WORKER THREAD ============
class BenchmarkWorker(QThread):
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, code, language):
        super().__init__()
        self.code = code
        self.language = language
    
    def run(self):
        try:
            # TODO: Actual compilation and benchmarking
            # For now, mock response
            result = {
                "status": "success",
                "time_ns": 1234567,
                "memory_kb": 512,
                "complexity": "O(n log n)"
            }
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


# ============ MAIN WINDOW ============
class AlgoForgeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.is_dark = True
        self.current_language = "C++"
        self.init_ui()
        self.apply_theme()
        
    def init_ui(self):
        self.setWindowTitle("AlgoForge - Algorithm Benchmark System")
        self.setGeometry(100, 100, 1400, 900)
        
        # Central Widget
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # ========== HEADER ==========
        header = self.create_header()
        layout.addWidget(header)
        
        # ========== TABS ==========
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_benchmark_tab(), "Benchmark")
        self.tabs.addTab(self.create_visualizer_tab(), "Visualizer")
        self.tabs.addTab(self.create_history_tab(), "History")
        layout.addWidget(self.tabs)
        
        # ========== STATUS BAR ==========
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
    def create_header(self):
        header = QWidget()
        layout = QHBoxLayout(header)
        layout.setContentsMargins(20, 15, 20, 15)
        
        # Title
        title = QLabel("ALGOFORGE")
        title_font = QFont("Consolas", 24, QFont.Weight.Bold)
        title.setFont(title_font)
        layout.addWidget(title)
        
        layout.addStretch()
        
        # Theme Toggle
        self.theme_btn = QPushButton("🌙 Dark")
        self.theme_btn.setFixedSize(100, 35)
        self.theme_btn.clicked.connect(self.toggle_theme)
        layout.addWidget(self.theme_btn)
        
        # Separator
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFixedHeight(2)
        
        wrapper = QWidget()
        wrapper_layout = QVBoxLayout(wrapper)
        wrapper_layout.setContentsMargins(0, 0, 0, 0)
        wrapper_layout.setSpacing(0)
        wrapper_layout.addWidget(header)
        wrapper_layout.addWidget(line)
        
        return wrapper
        
    def create_benchmark_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # ========== TOP CONTROLS ==========
        controls = QHBoxLayout()
        
        # Language Selector
        lang_label = QLabel("Language:")
        controls.addWidget(lang_label)
        
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["C++", "Python", "Java", "C"])
        self.lang_combo.currentTextChanged.connect(self.on_language_changed)
        self.lang_combo.setFixedWidth(120)
        controls.addWidget(self.lang_combo)
        
        controls.addStretch()
        
        # Upload Button
        upload_btn = QPushButton("📁 Upload File")
        upload_btn.clicked.connect(self.upload_code)
        upload_btn.setFixedHeight(35)
        controls.addWidget(upload_btn)
        
        # Run Button
        self.run_btn = QPushButton("▶ Run Benchmark")
        self.run_btn.clicked.connect(self.run_benchmark)
        self.run_btn.setFixedHeight(35)
        controls.addWidget(self.run_btn)
        
        layout.addLayout(controls)
        
        # ========== SPLITTER FOR CODE/OUTPUT ==========
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # LEFT: Code Editor
        code_group = QGroupBox("Code Editor")
        code_layout = QVBoxLayout()
        
        self.code_editor = QTextEdit()
        self.code_editor.setPlaceholderText(
            "// Paste your algorithm here\n"
            "// Include visualizer calls:\n"
            "//   viz.compare(i, j);\n"
            "//   viz.swap(i, j);\n"
        )
        self.code_editor.setFont(QFont("Consolas", 11))
        self.highlighter = CppHighlighter(self.code_editor.document())
        code_layout.addWidget(self.code_editor)
        
        code_group.setLayout(code_layout)
        splitter.addWidget(code_group)
        
        # RIGHT: Output/Results
        output_group = QGroupBox("Output & Results")
        output_layout = QVBoxLayout()
        
        # Output Text
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setFont(QFont("Consolas", 10))
        self.output_text.setPlaceholderText("Compilation output and errors will appear here...")
        output_layout.addWidget(self.output_text)
        
        # Results Summary
        results_frame = QFrame()
        results_layout = QHBoxLayout(results_frame)
        
        self.time_label = QLabel("Time: --")
        self.memory_label = QLabel("Memory: --")
        self.complexity_label = QLabel("Complexity: --")
        
        results_layout.addWidget(self.time_label)
        results_layout.addWidget(self.memory_label)
        results_layout.addWidget(self.complexity_label)
        results_layout.addStretch()
        
        output_layout.addWidget(results_frame)
        
        output_group.setLayout(output_layout)
        splitter.addWidget(output_group)
        
        splitter.setStretchFactor(0, 6)
        splitter.setStretchFactor(1, 4)
        
        layout.addWidget(splitter)
        
        # ========== GRAPH AREA ==========
        graph_group = QGroupBox("Performance Graph")
        graph_layout = QVBoxLayout()
        
        self.graph_placeholder = QLabel("📊 Graph will appear after benchmark runs")
        self.graph_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.graph_placeholder.setFixedHeight(200)
        graph_layout.addWidget(self.graph_placeholder)
        
        graph_group.setLayout(graph_layout)
        layout.addWidget(graph_group)
        
        return tab
        
    def create_visualizer_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Controls
        controls = QHBoxLayout()
        
        self.play_btn = QPushButton("▶ Play")
        self.play_btn.setFixedSize(80, 35)
        controls.addWidget(self.play_btn)
        
        self.pause_btn = QPushButton("⏸ Pause")
        self.pause_btn.setFixedSize(80, 35)
        controls.addWidget(self.pause_btn)
        
        self.step_btn = QPushButton("⏭ Step")
        self.step_btn.setFixedSize(80, 35)
        controls.addWidget(self.step_btn)
        
        controls.addStretch()
        
        speed_label = QLabel("Speed:")
        controls.addWidget(speed_label)
        
        self.speed_combo = QComboBox()
        self.speed_combo.addItems(["0.25x", "0.5x", "1x", "2x", "4x"])
        self.speed_combo.setCurrentText("1x")
        self.speed_combo.setFixedWidth(80)
        controls.addWidget(self.speed_combo)
        
        layout.addLayout(controls)
        
        # Visualization Area
        viz_area = QLabel("🎨 Algorithm Visualization\n\nRun a benchmark first to visualize")
        viz_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        viz_area.setFont(QFont("Consolas", 16))
        layout.addWidget(viz_area, 1)
        
        return tab
        
    def create_history_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(15, 15, 15, 15)
        
        history_label = QLabel("📜 Benchmark History\n\nPast runs will appear here")
        history_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        history_label.setFont(QFont("Consolas", 14))
        layout.addWidget(history_label)
        
        return tab
        
    def upload_code(self):
        extensions = {
            "C++": "C++ Files (*.cpp *.cc *.cxx);;All Files (*)",
            "Python": "Python Files (*.py);;All Files (*)",
            "Java": "Java Files (*.java);;All Files (*)",
            "C": "C Files (*.c);;All Files (*)"
        }
        
        ext_filter = extensions.get(self.current_language, "All Files (*)")
        filename, _ = QFileDialog.getOpenFileName(
            self, "Open Code File", "", ext_filter
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    code = f.read()
                self.code_editor.setText(code)
                self.status_bar.showMessage(f"Loaded: {filename}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load file:\n{str(e)}")
                
    def run_benchmark(self):
        code = self.code_editor.toPlainText()
        if not code.strip():
            QMessageBox.warning(self, "No Code", "Please enter code to benchmark")
            return
            
        self.run_btn.setEnabled(False)
        self.output_text.clear()
        self.output_text.append("🔨 Compiling...\n")
        self.status_bar.showMessage("Running benchmark...")
        
        # Start worker thread
        self.worker = BenchmarkWorker(code, self.current_language)
        self.worker.finished.connect(self.on_benchmark_finished)
        self.worker.error.connect(self.on_benchmark_error)
        self.worker.start()
        
    def on_benchmark_finished(self, result):
        self.run_btn.setEnabled(True)
        self.output_text.append("✅ Benchmark completed!\n")
        self.output_text.append(json.dumps(result, indent=2))
        
        # Update labels
        self.time_label.setText(f"Time: {result['time_ns']/1e6:.2f} ms")
        self.memory_label.setText(f"Memory: {result['memory_kb']} KB")
        self.complexity_label.setText(f"Complexity: {result['complexity']}")
        
        self.status_bar.showMessage("Benchmark completed successfully")
        
    def on_benchmark_error(self, error_msg):
        self.run_btn.setEnabled(True)
        self.output_text.append(f"❌ Error:\n{error_msg}")
        self.status_bar.showMessage("Benchmark failed")
        
    def on_language_changed(self, language):
        self.current_language = language
        self.status_bar.showMessage(f"Language: {language}")
        
    def toggle_theme(self):
        self.is_dark = not self.is_dark
        self.apply_theme()
        
    def apply_theme(self):
        if self.is_dark:
            self.theme_btn.setText("☀️ Light")
            self.setStyleSheet(f"""
                QMainWindow, QWidget {{
                    background-color: {Theme.DARK_BG};
                    color: {Theme.DARK_TEXT};
                    font-family: 'Consolas', 'Courier New', monospace;
                }}
                QLabel {{
                    color: {Theme.DARK_TEXT};
                }}
                QPushButton {{
                    background-color: {Theme.DARK_BG_TERTIARY};
                    color: {Theme.DARK_TEXT};
                    border: 1px solid {Theme.DARK_BORDER};
                    border-radius: 4px;
                    padding: 8px 16px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: {Theme.DARK_ACCENT};
                    color: {Theme.DARK_BG};
                }}
                QPushButton:pressed {{
                    background-color: {Theme.DARK_SUCCESS};
                }}
                QTextEdit {{
                    background-color: {Theme.DARK_BG_SECONDARY};
                    color: {Theme.DARK_TEXT};
                    border: 1px solid {Theme.DARK_BORDER};
                    border-radius: 4px;
                    padding: 8px;
                }}
                QComboBox {{
                    background-color: {Theme.DARK_BG_TERTIARY};
                    color: {Theme.DARK_TEXT};
                    border: 1px solid {Theme.DARK_BORDER};
                    border-radius: 4px;
                    padding: 5px;
                }}
                QGroupBox {{
                    border: 1px solid {Theme.DARK_BORDER};
                    border-radius: 4px;
                    margin-top: 10px;
                    font-weight: bold;
                    padding-top: 10px;
                }}
                QGroupBox::title {{
                    color: {Theme.DARK_ACCENT};
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px;
                }}
                QTabWidget::pane {{
                    border: 1px solid {Theme.DARK_BORDER};
                    background-color: {Theme.DARK_BG};
                }}
                QTabBar::tab {{
                    background-color: {Theme.DARK_BG_SECONDARY};
                    color: {Theme.DARK_TEXT_SECONDARY};
                    padding: 10px 20px;
                    border: 1px solid {Theme.DARK_BORDER};
                    border-bottom: none;
                    border-top-left-radius: 4px;
                    border-top-right-radius: 4px;
                }}
                QTabBar::tab:selected {{
                    background-color: {Theme.DARK_BG};
                    color: {Theme.DARK_ACCENT};
                    border-bottom: 2px solid {Theme.DARK_ACCENT};
                }}
                QStatusBar {{
                    background-color: {Theme.DARK_BG_SECONDARY};
                    color: {Theme.DARK_TEXT_SECONDARY};
                    border-top: 1px solid {Theme.DARK_BORDER};
                }}
                QFrame[frameShape="4"] {{
                    background-color: {Theme.DARK_BORDER};
                }}
            """)
        else:
            self.theme_btn.setText("🌙 Dark")
            self.setStyleSheet(f"""
                QMainWindow, QWidget {{
                    background-color: {Theme.LIGHT_BG};
                    color: {Theme.LIGHT_TEXT};
                    font-family: 'Consolas', 'Courier New', monospace;
                }}
                QLabel {{
                    color: {Theme.LIGHT_TEXT};
                }}
                QPushButton {{
                    background-color: {Theme.LIGHT_BG_TERTIARY};
                    color: {Theme.LIGHT_TEXT};
                    border: 1px solid {Theme.LIGHT_BORDER};
                    border-radius: 4px;
                    padding: 8px 16px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: {Theme.LIGHT_ACCENT};
                    color: white;
                }}
                QPushButton:pressed {{
                    background-color: {Theme.LIGHT_SUCCESS};
                }}
                QTextEdit {{
                    background-color: {Theme.LIGHT_BG_SECONDARY};
                    color: {Theme.LIGHT_TEXT};
                    border: 1px solid {Theme.LIGHT_BORDER};
                    border-radius: 4px;
                    padding: 8px;
                }}
                QComboBox {{
                    background-color: {Theme.LIGHT_BG_TERTIARY};
                    color: {Theme.LIGHT_TEXT};
                    border: 1px solid {Theme.LIGHT_BORDER};
                    border-radius: 4px;
                    padding: 5px;
                }}
                QGroupBox {{
                    border: 1px solid {Theme.LIGHT_BORDER};
                    border-radius: 4px;
                    margin-top: 10px;
                    font-weight: bold;
                    padding-top: 10px;
                }}
                QGroupBox::title {{
                    color: {Theme.LIGHT_ACCENT};
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px;
                }}
                QTabWidget::pane {{
                    border: 1px solid {Theme.LIGHT_BORDER};
                    background-color: {Theme.LIGHT_BG};
                }}
                QTabBar::tab {{
                    background-color: {Theme.LIGHT_BG_SECONDARY};
                    color: {Theme.LIGHT_TEXT_SECONDARY};
                    padding: 10px 20px;
                    border: 1px solid {Theme.LIGHT_BORDER};
                    border-bottom: none;
                    border-top-left-radius: 4px;
                    border-top-right-radius: 4px;
                }}
                QTabBar::tab:selected {{
                    background-color: {Theme.LIGHT_BG};
                    color: {Theme.LIGHT_ACCENT};
                    border-bottom: 2px solid {Theme.LIGHT_ACCENT};
                }}
                QStatusBar {{
                    background-color: {Theme.LIGHT_BG_SECONDARY};
                    color: {Theme.LIGHT_TEXT_SECONDARY};
                    border-top: 1px solid {Theme.LIGHT_BORDER};
                }}
                QFrame[frameShape="4"] {{
                    background-color: {Theme.LIGHT_BORDER};
                }}
            """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AlgoForgeWindow()
    window.show()
    sys.exit(app.exec())
    