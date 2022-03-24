# Main Window for vkpurge-pyqt
# Shows the list of kernels can be purged
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QListWidget, QListWidgetItem, \
    QAbstractItemView
from PyQt5.QtCore import QProcess
from RemoverWindow import RemoverWindow

button_stylesheet = "padding: 6px;"


class MainWindow(QDialog):

    def __init__(self):
        super(QDialog, self).__init__()

        self.main_layout = QVBoxLayout()
        self.setWindowTitle("Purge Old Kernels - vkpurge GUI Wrapper")

        self.kernels = []
        self.selected_kernels = []

        title_label = QLabel("<h2>Purge Previous Kernel Versions</h2>")
        explanation_label = QLabel("Please pick the versions you want to remove, "
                                   "or click 'Remove All' button below")

        self.kernels_list_view = QListWidget()
        self.kernels_list_view.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.kernels_list_view.itemSelectionChanged.connect(self.on_list_view_clicked)

        bottom_buttons_layout = QHBoxLayout()

        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.do_refresh_list)

        self.remove_selected_button = QPushButton("Remove Selected")
        self.remove_selected_button.setEnabled(False)
        self.remove_selected_button.clicked.connect(self.do_remove_selected)

        self.remove_all_button = QPushButton("Remove All")
        self.remove_all_button.clicked.connect(self.do_remove_all)

        self.refresh_button.setStyleSheet(button_stylesheet)
        self.remove_selected_button.setStyleSheet(button_stylesheet)
        self.remove_all_button.setStyleSheet(button_stylesheet)

        self.status_label = QLabel("")

        bottom_buttons_layout.addWidget(self.refresh_button)
        bottom_buttons_layout.addWidget(self.status_label)
        bottom_buttons_layout.addStretch()
        bottom_buttons_layout.addWidget(self.remove_selected_button)
        bottom_buttons_layout.addWidget(self.remove_all_button)

        self.main_layout.addWidget(title_label)
        self.main_layout.addWidget(explanation_label)
        self.main_layout.addWidget(self.kernels_list_view)
        self.main_layout.addLayout(bottom_buttons_layout)

        self.list_process = QProcess(None)
        self.list_process.readyReadStandardOutput.connect(self.read_process_output)
        self.list_process.finished.connect(self.on_process_finished)
        self.list_process.setProgram("vkpurge")
        self.list_process.setArguments(["list"])

        self.do_refresh_list()

        self.setLayout(self.main_layout)
        self.show()

    def on_process_finished(self, exit_code, exit_status):
        self.selected_kernels.clear()
        self.kernels_list_view.clear()
        font = QFont()
        font.setPointSize(16)
        for kernel in self.kernels:
            item = QListWidgetItem(kernel)
            item.setFont(font)
            self.kernels_list_view.addItem(item)

        self.remove_all_button.setEnabled(len(self.kernels) > 0)
        self.status_label.setText("No old kernels found" if len(self.kernels) == 0 else "")
        self.refresh_button.setEnabled(True)

    def read_process_output(self):
        output = bytearray(self.list_process.readAllStandardOutput())
        self.kernels = output.decode("UTF-8").strip().split(" ")

    def do_refresh_list(self):
        self.refresh_button.setEnabled(False)
        self.remove_selected_button.setEnabled(False)
        self.remove_all_button.setEnabled(False)
        self.kernels.clear()
        self.status_label.setText("")
        self.list_process.start()

    def do_remove_all(self):
        remover = RemoverWindow()
        remover.exec_()
        self.do_refresh_list()

    def do_remove_selected(self):
        remover = RemoverWindow(self.selected_kernels)
        remover.exec_()
        self.do_refresh_list()

    def on_list_view_clicked(self):
        self.selected_kernels = [item.text().strip() for item in self.kernels_list_view.selectedItems()]
        self.remove_selected_button.setEnabled(len(self.selected_kernels) > 0)
