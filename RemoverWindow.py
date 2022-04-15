# Window that opens when you pick one of the removal options
from PyQt5.QtCore import QProcess
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QPlainTextEdit


class RemoverWindow(QDialog):

    def __init__(self, selected_kernels: list = []):
        super(QDialog, self).__init__()

        self.setWindowTitle("Progress Window")
        self.setFixedSize(400, 200)

        self.main_layout = QVBoxLayout()

        self.title_label = QLabel("<h2>Removing Kernel(s)</h2>")
        self.status_label = QLabel("Please wait while the action is being performed...")

        bottom_layout = QHBoxLayout()

        self.close_button = QPushButton("Close")
        self.close_button.setEnabled(False)
        self.close_button.clicked.connect(self.close)

        bottom_layout.addStretch()
        bottom_layout.addWidget(self.close_button)

        self.output_text_edit = QPlainTextEdit()
        self.output_text_edit.setReadOnly(True)

        self.main_layout.addWidget(self.title_label)
        self.main_layout.addWidget(self.status_label)
        # self.main_layout.addStretch()
        self.main_layout.addWidget(self.output_text_edit)
        self.main_layout.addLayout(bottom_layout)

        self.setLayout(self.main_layout)
        self.show()

        self.process = QProcess(None)
        self.process.setProcessChannelMode(QProcess.MergedChannels)
        self.process.readyReadStandardOutput.connect(self.read_process_output)
        self.process.finished.connect(self.on_process_finished)

        self.perform_kernel_removal(selected_kernels)

    def on_process_finished(self, exit_code, exit_status):
        if exit_code == 0:
            self.status_label.setText("Removal successfully completed!")
            self.output_text_edit.appendPlainText("Removal successful!")
        elif exit_code == 127:
            self.status_label.setText("Authorization failed. Please try again.")
        else:
            self.status_label.setText("An error has occured.")

        self.close_button.setEnabled(True)

    def perform_kernel_removal(self, selected_kernels: list = []):
        self.process.setProgram("pkexec")
        kernels_str = " ".join(selected_kernels)
        self.process.setArguments(["vkpurge", "rm", f"{kernels_str}" if len(selected_kernels) > 0 else "all"])
        self.process.start()

    def read_process_output(self):
        output = bytearray(self.process.readAllStandardOutput())
        self.output_text_edit.appendPlainText(output.decode("UTF-8").strip())
