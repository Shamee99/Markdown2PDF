import os
import sys

import markdown2
import pdfkit
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLineEdit, QPushButton, QProgressBar,
                             QFileDialog, QMessageBox, QLabel)


# 配置wkhtmltopdf路径
def extract_wkhtmltopdf():
    # 获取程序目录中的wkhtmltopdf安装程序路径
    installer_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'wkhtmltox-0.12.6-1.msvc2015-win64.exe')
    if not os.path.exists(installer_path):
        return False
    
    # 解压wkhtmltopdf.exe到程序目录
    program_dir = os.path.dirname(os.path.abspath(__file__))
    target_path = os.path.join(program_dir, 'wkhtmltopdf.exe')
    
    try:
        # 使用安装程序的静默安装模式提取wkhtmltopdf.exe
        os.system(f'"{installer_path}" /S /D={program_dir}')
        return os.path.exists(target_path)
    except:
        return False

def find_wkhtmltopdf():
    # 首先检查程序目录下的bin文件夹
    program_dir = os.path.dirname(os.path.abspath(__file__))
    bin_path = os.path.join(program_dir, 'bin', 'wkhtmltopdf.exe')
    if os.path.exists(bin_path):
        return bin_path
    
    # 检查程序目录
    program_dir_path = os.path.join(program_dir, 'wkhtmltopdf.exe')
    if os.path.exists(program_dir_path):
        return program_dir_path
    
    # 如果程序目录中不存在，尝试解压
    if extract_wkhtmltopdf():
        return program_dir_path
    
    # 如果解压失败，检查其他可能的安装路径
    possible_paths = [
        'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe',  # 默认64位安装路径
        'C:\\Program Files (x86)\\wkhtmltopdf\\bin\\wkhtmltopdf.exe',  # 默认32位安装路径
    ]
    
    # 检查环境变量
    if 'PATH' in os.environ:
        for path_dir in os.environ['PATH'].split(os.pathsep):
            wk_path = os.path.join(path_dir, 'wkhtmltopdf.exe')
            if os.path.exists(wk_path):
                return wk_path
    
    # 检查可能的安装路径
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return None

WKHTMLTOPDF_PATH = find_wkhtmltopdf()

# 配置pdfkit
config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH) if WKHTMLTOPDF_PATH else None

class ConvertThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, input_dir, output_dir, header_edit, footer_edit):
        super().__init__()
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.header_edit = header_edit
        self.footer_edit = footer_edit

    def run(self):
        try:
            # 检查wkhtmltopdf是否可用
            if not os.path.exists(WKHTMLTOPDF_PATH):
                self.error.emit('未找到wkhtmltopdf，请确保已正确安装wkhtmltopdf工具！')
                return

            md_files = [f for f in os.listdir(self.input_dir) if f.endswith('.md')]
            total_files = len(md_files)
            
            if total_files == 0:
                self.error.emit('所选文件夹中没有找到.md文件！')
                return

            for i, md_file in enumerate(md_files, 1):
                input_path = os.path.abspath(os.path.join(self.input_dir, md_file))
                output_path = os.path.abspath(os.path.join(self.output_dir, f'{os.path.splitext(md_file)[0]}.pdf'))
                
                with open(input_path, 'r', encoding='utf-8') as f:
                    markdown_content = f.read()
                
                # 转换Markdown为HTML
                html_content = markdown2.markdown(markdown_content)
                
                # 添加页眉页脚
                header = self.header_edit.text()
                footer = self.footer_edit.text()
                
                # 创建页眉HTML
                header_html = ""
                if header:
                    header_html = f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <meta charset="utf-8">
                        <style>
                            body {{ margin: 0; padding: 0; }}
                            .header {{ 
                                text-align: left; 
                                font-size: 10px; 
                                color: #333333;
                                padding: 5px 10px;
                                border-bottom: 1px solid #cccccc;
                                background: linear-gradient(to right, #FFA500, #FFE4B5);
                                margin: 0 0 10px 0;
                                width: 100%;
                                box-sizing: border-box;
                                height: 20px;
                                line-height: 20px;
                            }}
                        </style>
                    </head>
                    <body>
                        <div class="header">{header}</div>
                    </body>
                    </html>
                    """
                
                # 创建页脚HTML
                footer_html = ""
                if footer:
                    footer_html = f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <meta charset="utf-8">
                        <style>
                            body {{ margin: 0; padding: 0; }}
                            .footer {{ 
                                text-align: left; 
                                font-size: 10px; 
                                color: #333333;
                                padding: 5px 10px;
                                border-top: 1px solid #cccccc;
                                background: linear-gradient(to right, #FFA500, #FFE4B5);
                                margin: 0;
                                width: 100%;
                                box-sizing: border-box;
                                height: 20px;
                                line-height: 20px;
                            }}
                        </style>
                    </head>
                    <body>
                        <div class="footer">{footer}</div>
                    </body>
                    </html>
                    """
                
                # 创建临时文件保存页眉页脚HTML
                header_path = os.path.join(self.output_dir, f'header_{os.path.splitext(md_file)[0]}.html')
                footer_path = os.path.join(self.output_dir, f'footer_{os.path.splitext(md_file)[0]}.html')
                
                try:
                    with open(header_path, 'w', encoding='utf-8') as f:
                        f.write(header_html)
                    with open(footer_path, 'w', encoding='utf-8') as f:
                        f.write(footer_html)
                    
                    html_template = f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <meta charset="utf-8">
                        <style>
                            body {{ margin: 40px; }}
                        </style>
                    </head>
                    <body>
                        {html_content}
                    </body>
                    </html>
                    """
                    
                    # 配置PDF选项
                    options = {
                        'page-size': 'A4',
                        'margin-top': '25mm',
                        'margin-right': '15mm',
                        'margin-bottom': '25mm',
                        'margin-left': '15mm',
                        'encoding': "UTF-8",
                        'enable-local-file-access': True,
                        'header-spacing': '10',
                        'footer-spacing': '10',
                        'header-html': header_path if header else None,
                        'footer-html': footer_path if footer else None,
                        'footer-right': '第 [page] 页'
                    }
                    
                    # 执行转换
                    pdfkit.from_string(html_template, output_path, options=options, configuration=config)
                finally:
                    # 清理临时文件
                    if os.path.exists(header_path):
                        os.remove(header_path)
                    if os.path.exists(footer_path):
                        os.remove(footer_path)
                
                progress = int((i / total_files) * 100)
                self.progress.emit(progress)
            
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Markdown批量转PDF工具')
        self.setGeometry(300, 300, 600, 150)

        # 主布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # 输入文件夹选择
        input_layout = QHBoxLayout()
        self.input_edit = QLineEdit()
        self.input_edit.setPlaceholderText('选择包含Markdown文件的文件夹')
        input_button = QPushButton('浏览')
        input_button.clicked.connect(self.select_input_folder)
        input_layout.addWidget(self.input_edit)
        input_layout.addWidget(input_button)

        # 页眉页脚设置
        header_layout = QHBoxLayout()
        self.header_edit = QLineEdit()
        self.header_edit.setPlaceholderText('输入页眉文本（可选）')
        header_layout.addWidget(QLabel('页眉：'))
        header_layout.addWidget(self.header_edit)

        footer_layout = QHBoxLayout()
        self.footer_edit = QLineEdit()
        self.footer_edit.setPlaceholderText('输入页脚文本（可选）')
        footer_layout.addWidget(QLabel('页脚：'))
        footer_layout.addWidget(self.footer_edit)

        # 输出文件夹选择
        output_layout = QHBoxLayout()
        self.output_edit = QLineEdit()
        self.output_edit.setPlaceholderText('选择PDF文件输出文件夹')
        output_button = QPushButton('浏览')
        output_button.clicked.connect(self.select_output_folder)
        output_layout.addWidget(self.output_edit)
        output_layout.addWidget(output_button)

        # 转换按钮
        convert_button = QPushButton('开始转换')
        convert_button.clicked.connect(self.start_conversion)

        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setAlignment(Qt.AlignCenter)

        # 添加所有组件到主布局
        layout.addLayout(input_layout)
        layout.addLayout(header_layout)
        layout.addLayout(footer_layout)
        layout.addLayout(output_layout)
        layout.addWidget(convert_button)
        layout.addWidget(self.progress_bar)

    def select_input_folder(self):
        folder = QFileDialog.getExistingDirectory(self, '选择输入文件夹')
        if folder:
            self.input_edit.setText(folder)

    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, '选择输出文件夹')
        if folder:
            self.output_edit.setText(folder)

    def start_conversion(self):
        input_dir = self.input_edit.text()
        output_dir = self.output_edit.text()

        if not input_dir or not output_dir:
            QMessageBox.warning(self, '警告', '请选择输入和输出文件夹！')
            return

        if not os.path.exists(input_dir) or not os.path.exists(output_dir):
            QMessageBox.warning(self, '警告', '输入或输出文件夹不存在！')
            return

        self.progress_bar.setValue(0)
        self.convert_thread = ConvertThread(input_dir, output_dir, self.header_edit, self.footer_edit)
        self.convert_thread.progress.connect(self.update_progress)
        self.convert_thread.finished.connect(self.conversion_finished)
        self.convert_thread.error.connect(self.show_error)
        self.convert_thread.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def conversion_finished(self):
        QMessageBox.information(self, '完成', '转换完成！')
        os.startfile(self.output_edit.text())

    def show_error(self, error_msg):
        QMessageBox.critical(self, '错误', f'转换过程中出现错误：\n{error_msg}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())