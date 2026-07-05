import sys
import pandas as pd

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QFileDialog,
    QTextEdit,
    QVBoxLayout,
    QMessageBox
)

from matplotlib import pyplot as plt


class SocialMediaAnalyzer(QWidget):

    def __init__(self):
        super().__init__()

        self.df = None

        self.setWindowTitle("Social Media Best Time Poster")
        self.setGeometry(300, 150, 700, 500)

        layout = QVBoxLayout()

        title = QLabel("📱 Social Media Best Time Poster")
        title.setStyleSheet("font-size:22px;font-weight:bold;")
        layout.addWidget(title)

        self.load_btn = QPushButton("Load CSV")
        self.load_btn.clicked.connect(self.load_csv)
        layout.addWidget(self.load_btn)

        self.analyze_btn = QPushButton("Analyze Best Time")
        self.analyze_btn.clicked.connect(self.analyze)
        layout.addWidget(self.analyze_btn)

        self.chart_btn = QPushButton("Show Chart")
        self.chart_btn.clicked.connect(self.show_chart)
        layout.addWidget(self.chart_btn)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        self.setLayout(layout)

    def load_csv(self):

        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV File",
            "",
            "CSV Files (*.csv)"
        )

        if file_name:
            self.df = pd.read_csv(file_name)

            self.output.clear()
            self.output.append("✅ CSV Loaded Successfully\n")
            self.output.append(str(self.df.head()))

    def analyze(self):

        if self.df is None:
            QMessageBox.warning(self, "Error", "Please load CSV first.")
            return

        avg = self.df.groupby("Time")["Likes"].mean()

        best_time = avg.idxmax()
        likes = avg.max()

        self.output.append("\n=========================")
        self.output.append(f"Best Posting Time : {best_time}")
        self.output.append(f"Average Likes : {likes:.2f}")

    def show_chart(self):

        if self.df is None:
            QMessageBox.warning(self, "Error", "Please load CSV first.")
            return

        avg = self.df.groupby("Time")["Likes"].mean()

        avg.plot(kind="bar")

        plt.title("Average Likes by Time")
        plt.xlabel("Time")
        plt.ylabel("Likes")
        plt.show()


app = QApplication(sys.argv)

window = SocialMediaAnalyzer()
window.show()

sys.exit(app.exec())