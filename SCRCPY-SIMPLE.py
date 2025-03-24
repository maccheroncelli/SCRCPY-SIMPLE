import sys
import os
import subprocess
import datetime
import time
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QComboBox, QLabel, QTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextOption
from PIL import Image
from io import BytesIO

adb_path = 'adb'

translations = {
    'English': {
        'language_name': 'English',
        'start_scrcpy': 'Start SCRCPY',
        'mode_label': 'Mode:',
        'screenshot': 'Screenshot',
        'log_scrcpy_start': 'Started SCRCPY in screenshot mode',
        'log_scrcpy_recording': 'Started screen recording: {}',
        'log_scrcpy_fail': 'Failed to start SCRCPY: {}',
        'log_screenshot_saved': 'Screenshot saved: {}',
        'log_screenshot_fail': 'Screenshot failed: {}',
        'screenshots': 'Screenshots',
        'screen_recording': 'Screen recording'
    },
    'Vietnamese': {
        'language_name': 'Tiếng Việt',
        'start_scrcpy': 'Khởi động SCRCPY',
        'mode_label': 'Chế độ:',
        'screenshot': 'Chụp màn hình',
        'log_scrcpy_start': 'Đã khởi động SCRCPY ở chế độ chụp màn hình',
        'log_scrcpy_recording': 'Bắt đầu ghi màn hình: {}',
        'log_scrcpy_fail': 'Không thể khởi động SCRCPY: {}',
        'log_screenshot_saved': 'Ảnh chụp màn hình đã được lưu: {}',
        'log_screenshot_fail': 'Không thể chụp màn hình: {}',
        'screenshots': 'Chụp màn hình',
        'screen_recording': 'Ghi màn hình'
    },  
    'Thai': {
        'language_name': 'ไทย',
        'start_scrcpy': 'เริ่ม SCRCPY',
        'mode_label': 'โหมด:',
        'screenshot': 'จับภาพ',
        'log_scrcpy_start': 'เริ่ม SCRCPY ในโหมดภาพหน้าจอ',
        'log_scrcpy_recording': 'เริ่มการบันทึกหน้าจอ: {}',
        'log_scrcpy_fail': 'ไม่สามารถเริ่ม SCRCPY: {}',
        'log_screenshot_saved': 'บันทึกภาพหน้าจอแล้ว: {}',
        'log_screenshot_fail': 'การจับภาพหน้าจอล้มเหลว: {}',
        'screenshots': 'ภาพหน้าจอ',
        'screen_recording': 'บันทึกหน้าจอ'
    },
    'Khmer': {
        'language_name': 'ភាសាខ្មែរ',
        'start_scrcpy': 'ចាប់ផ្តើម SCRCPY',
        'mode_label': 'របៀប:',
        'screenshot': 'ថតរូបអេក្រង់',
        'log_scrcpy_start': 'បានចាប់ផ្តើម SCRCPY ក្នុងរបៀបថតអេក្រង់',
        'log_scrcpy_recording': 'ចាប់ផ្តើមការថតអេក្រង់: {}',
        'log_scrcpy_fail': 'បរាជ័យក្នុងការចាប់ផ្តើម SCRCPY: {}',
        'log_screenshot_saved': 'បានរក្សាទុករូបថតអេក្រង់: {}',
        'log_screenshot_fail': 'បរាជ័យក្នុងការថតរូបអេក្រង់: {}',
        'screenshots': 'ថតរូបអេក្រង់',
        'screen_recording': 'ថតអេក្រង់'
    },
    'Lao': {
        'language_name': 'ພາສາລາວ',
        'start_scrcpy': 'ເລີ່ມ SCRCPY',
        'mode_label': 'ໂໝດ:',
        'screenshot': 'ຈັບພາບ',
        'log_scrcpy_start': 'ເລີ່ມ SCRCPY ໃນໂໝດຈັບພາບ',
        'log_scrcpy_recording': 'ເລີ່ມບັນທຶກຫນ້າຈໍ: {}',
        'log_scrcpy_fail': 'ບໍ່ສາມາດເລີ່ມ SCRCPY: {}',
        'log_screenshot_saved': 'ບັນທຶກຮູບພາບແລ້ວ: {}',
        'log_screenshot_fail': 'ຈັບພາບຜິດພາດ: {}',
        'screenshots': 'ຈັບພາບ',
        'screen_recording': 'ບັນທຶກຫນ້າຈໍ'
    },
    'Sinhala': {
        'language_name': 'සිංහල',
        'start_scrcpy': 'SCRCPY ආරම්භ කරන්න',
        'mode_label': 'මාදිලිය:',
        'screenshot': 'තිර රූපය',
        'log_scrcpy_start': 'SCRCPY ආරම්භ විය තිර රූප මාදිලියෙන්',
        'log_scrcpy_recording': 'තිරය වාර්තා කිරීම ආරම්භ කරන ලදී: {}',
        'log_scrcpy_fail': 'SCRCPY ආරම්භයට අසාර්ථකයි: {}',
        'log_screenshot_saved': 'තිර රූපය සුරැකිණි: {}',
        'log_screenshot_fail': 'තිර රූපය අසාර්ථකයි: {}',
        'screenshots': 'තිර රූප',
        'screen_recording': 'තිර රූප ඇතුලත් කිරීම'
    },
    'Malay': {
        'language_name': 'Bahasa Melayu',
        'start_scrcpy': 'Mula SCRCPY',
        'mode_label': 'Mod:',
        'screenshot': 'Tangkap Skrin',
        'log_scrcpy_start': 'SCRCPY dimulakan dalam mod tangkap skrin',
        'log_scrcpy_recording': 'Rakaman skrin dimulakan: {}',
        'log_scrcpy_fail': 'Gagal memulakan SCRCPY: {}',
        'log_screenshot_saved': 'Tangkapan skrin disimpan: {}',
        'log_screenshot_fail': 'Gagal menangkap skrin: {}',
        'screenshots': 'Tangkapan Skrin',
        'screen_recording': 'Rakaman Skrin'
    },
    'Filipino': {
        'language_name': 'Filipino',
        'start_scrcpy': 'Simulan ang SCRCPY',
        'mode_label': 'Paraan:',
        'screenshot': 'Kuhanan ng Screenshot',
        'log_scrcpy_start': 'Sinimulan ang SCRCPY sa mode na screenshot',
        'log_scrcpy_recording': 'Sinimulan ang pag-record ng screen: {}',
        'log_scrcpy_fail': 'Nabigong simulan ang SCRCPY: {}',
        'log_screenshot_saved': 'Na-save ang screenshot: {}',
        'log_screenshot_fail': 'Nabigong kumuha ng screenshot: {}',
        'screenshots': 'Screenshot',
        'screen_recording': 'Pag-record ng Screen'
    },
    'Arabic': {
        'language_name': 'العربية',
        'start_scrcpy': 'ابدأ SCRCPY',
        'mode_label': 'الوضع:',
        'screenshot': 'لقطة شاشة',
        'log_scrcpy_start': 'تم بدء SCRCPY في وضع لقطة الشاشة',
        'log_scrcpy_recording': 'بدأ تسجيل الشاشة: {}',
        'log_scrcpy_fail': 'فشل في بدء SCRCPY: {}',
        'log_screenshot_saved': 'تم حفظ لقطة الشاشة: {}',
        'log_screenshot_fail': 'فشل في التقاط لقطة الشاشة: {}',
        'screenshots': 'لقطة شاشة',
        'screen_recording': 'تسجيل الشاشة'
    }
}

class SimpleSCRCPY(QWidget):
    def __init__(self):
        super().__init__()
        self.output_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'AndroidScreenOutput')
        os.makedirs(self.output_folder, exist_ok=True)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('SCRCPY Simple')
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        layout = QVBoxLayout(self)

        self.languageCombo = QComboBox()
        for lang_key, lang_data in translations.items():
            self.languageCombo.addItem(lang_data['language_name'], lang_key)
        self.languageCombo.currentIndexChanged.connect(self.updateLanguage)
        layout.addWidget(self.languageCombo)

        self.modeLabel = QLabel()
        layout.addWidget(self.modeLabel)

        self.modeCombo = QComboBox()
        layout.addWidget(self.modeCombo)

        self.startBtn = QPushButton()
        self.startBtn.clicked.connect(self.startSCRCPY)
        layout.addWidget(self.startBtn)

        self.screenshotBtn = QPushButton()
        self.screenshotBtn.clicked.connect(self.takeScreenshot)
        layout.addWidget(self.screenshotBtn)

        self.logArea = QTextEdit()
        self.logArea.setReadOnly(True)
        self.logArea.setWordWrapMode(QTextOption.NoWrap)
        layout.addWidget(self.logArea)

        self.resize(600, 300)
        self.updateLanguage()

    def updateLanguage(self):
        self.lang = self.languageCombo.currentData()
        t = translations[self.lang]
        self.startBtn.setText(t['start_scrcpy'])
        self.modeLabel.setText(t['mode_label'])
        self.screenshotBtn.setText(t['screenshot'])

        # Update modeCombo options with translated values
        current_key = self.modeCombo.currentData() or 'screenshots'
        self.modeCombo.clear()
        self.modeCombo.addItem(t['screenshots'], 'screenshots')
        self.modeCombo.addItem(t['screen_recording'], 'screen_recording')
        index = self.modeCombo.findData(current_key)
        if index >= 0:
            self.modeCombo.setCurrentIndex(index)
        

    def log(self, message_key, *args):
        t = translations[self.lang]
        message = t[message_key].format(*args)
        timestamp = datetime.datetime.now().strftime("%y/%m/%d %H:%M | ")
        self.logArea.append(timestamp + message)

    def startSCRCPY(self):
        import threading
        mode_key = self.modeCombo.currentData()
        self.startBtn.setEnabled(False)
        self.modeCombo.setEnabled(False)
        try:
            if mode_key == 'screen_recording':
                filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + '.mp4'
                path = os.path.join(self.output_folder, filename)
                self.process = subprocess.Popen(['scrcpy', '--record', path, '--audio-codec=aac'])
                self.log('log_scrcpy_recording', filename)
            elif mode_key == 'screenshots':
                self.process = subprocess.Popen(['scrcpy'])
                self.log('log_scrcpy_start')

            def monitor():
                while self.process.poll() is None:
                    time.sleep(0.5)  # Check every 500ms if the process is still running
                self.startBtn.setEnabled(True)
                self.modeCombo.setEnabled(True)
            monitor_thread = threading.Thread(target=monitor, daemon=True)
            monitor_thread.start()
        except Exception as e:
            self.log('log_scrcpy_fail', str(e))

    def takeScreenshot(self):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        try:
            data = subprocess.check_output([adb_path, 'exec-out', 'screencap', '-p'])
            image = Image.open(BytesIO(data))
            filename = f"{timestamp}.png"
            image.save(os.path.join(self.output_folder, filename))
            self.log('log_screenshot_saved', filename)
        except Exception as e:
            self.log('log_screenshot_fail', str(e))

if __name__ == '__main__':
    from PyQt5.QtGui import QFont
    app = QApplication(sys.argv)
    app.setFont(QFont("Noto Sans", 10))
    window = SimpleSCRCPY()
    window.show()
    sys.exit(app.exec_())
