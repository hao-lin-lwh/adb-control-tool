import sys
import os
import subprocess
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class AutomationAssistantV2(QWidget):
    def __init__(self):
        super().__init__()
        self.device_serial = None
        self.delay_enabled = False
        self.setWindowTitle("自动化助手 V2")
        self.resize(800, 600)  # 窗口更大
        self.init_ui()
        self.refresh_devices()  # 启动时自动检测设备
        
    def init_ui(self):
        # 主布局
        main_layout = QVBoxLayout()
        
        # === 1. 顶部状态栏（动态检测设备）===
        status_layout = QHBoxLayout()
        self.status_label = QLabel("正在检测设备...")
        self.status_label.setStyleSheet("""
            QLabel {
                background-color: #f0f0f0;
                padding: 5px;
                border: 1px solid #ccc;
                font-weight: bold;
            }
        """)
        
        self.device_combo = QComboBox()
        self.device_combo.setMinimumWidth(200)
        self.device_combo.currentTextChanged.connect(self.on_device_selected)
        
        refresh_btn = QPushButton("刷新")
        refresh_btn.clicked.connect(self.refresh_devices)
        
        status_layout.addWidget(QLabel("设备状态:"))
        status_layout.addWidget(self.status_label, 1)
        status_layout.addWidget(QLabel("选择设备:"))
        status_layout.addWidget(self.device_combo)
        status_layout.addWidget(refresh_btn)
        
        # === 2. 中间区域 ===
        middle_layout = QHBoxLayout()
        
        # 左侧：脚本编辑区
        left_panel = QVBoxLayout()
        left_panel.addWidget(QLabel("脚本编辑器 (双击命令可编辑):"))
        
        self.script_editor = QTextEdit()
        self.script_editor.setFont(QFont("Consolas", 10))
        self.script_editor.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: 1px solid #3c3c3c;
            }
        """)
        
        # 工具栏
        tool_layout = QHBoxLayout()
        save_btn = QPushButton("保存脚本")
        save_btn.clicked.connect(self.save_script)
        load_btn = QPushButton("加载脚本")
        load_btn.clicked.connect(self.load_script)
        run_btn = QPushButton("▶ 执行脚本")
        run_btn.clicked.connect(self.run_script)
        run_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; }")
        
        tool_layout.addWidget(save_btn)
        tool_layout.addWidget(load_btn)
        tool_layout.addStretch()
        tool_layout.addWidget(run_btn)
        
        left_panel.addLayout(tool_layout)
        left_panel.addWidget(self.script_editor)
        
        # 右侧：控制面板
        right_panel = QVBoxLayout()
        right_panel.addWidget(QLabel("快捷命令:"))
        
        # 按键模拟组
        key_group = QGroupBox("按键模拟")
        key_layout = QGridLayout()
        
        keys = [
            ("电源键", "26"), ("音量+", "24"), ("音量-", "25"),
            ("Home键", "3"), ("返回键", "4"), ("菜单键", "82"),
            ("确认键", "66"), ("删除键", "67")
        ]
        
        for i, (name, code) in enumerate(keys):
            btn = QPushButton(name)
            btn.clicked.connect(lambda checked, c=code: self.insert_command(f"keyevent {c}", name))
            key_layout.addWidget(btn, i//3, i%3)
        
        key_group.setLayout(key_layout)
        
        # 触摸模拟组
        touch_group = QGroupBox("触摸模拟")
        touch_layout = QGridLayout()
        
        touch_actions = [
            ("点击(100,200)", "tap 100 200"),
            ("长按(100,200)", "swipe 100 200 100 200 1000"),
            ("上滑", "swipe 300 800 300 300"),
            ("下滑", "swipe 300 300 300 800"),
            ("左滑", "swipe 500 500 100 500"),
            ("右滑", "swipe 100 500 500 500"),
        ]
        
        for i, (name, cmd) in enumerate(touch_actions):
            btn = QPushButton(name)
            btn.clicked.connect(lambda checked, c=cmd, n=name: self.insert_command(c, n))
            touch_layout.addWidget(btn, i//2, i%2)
        
        touch_group.setLayout(touch_layout)
        
        # 系统控制组
        system_group = QGroupBox("系统控制")
        system_layout = QVBoxLayout()
        
        system_actions = [
            ("截屏", "screencap /sdcard/screen.png"),
            ("录屏(开始)", "screenrecord /sdcard/record.mp4"),
            ("重启", "reboot"),
            ("关机", "reboot -p"),
            ("进入Fastboot", "reboot bootloader"),
        ]
        
        for name, cmd in system_actions:
            btn = QPushButton(name)
            btn.clicked.connect(lambda checked, c=cmd, n=name: self.insert_command(c, n))
            system_layout.addWidget(btn)
        
        system_group.setLayout(system_layout)
        
        # 应用控制组
        app_group = QGroupBox("应用控制")
        app_layout = QVBoxLayout()
        
        app_actions = [
            ("启动浏览器", "am start -a android.intent.action.VIEW -d https://www.baidu.com"),
            ("启动设置", "am start -a android.settings.SETTINGS"),
            ("列出应用", "pm list packages"),
            ("清除缓存", "pm clear com.example.app"),
        ]
        
        for name, cmd in app_actions:
            btn = QPushButton(name)
            btn.clicked.connect(lambda checked, c=cmd, n=name: self.insert_command(c, n))
            app_layout.addWidget(btn)
        
        app_group.setLayout(app_layout)
        
        # 延时选项
        delay_layout = QHBoxLayout()
        self.delay_checkbox = QCheckBox("所有命令自动插入1秒延时")
        self.delay_checkbox.stateChanged.connect(self.toggle_delay)
        delay_layout.addWidget(self.delay_checkbox)
        delay_layout.addStretch()
        
        # 组装右侧面板
        right_panel.addWidget(key_group)
        right_panel.addWidget(touch_group)
        right_panel.addWidget(system_group)
        right_panel.addWidget(app_group)
        right_panel.addLayout(delay_layout)
        right_panel.addStretch()
        
        # 添加到中间布局
        middle_layout.addLayout(left_panel, 2)  # 左侧占2份
        middle_layout.addLayout(right_panel, 1)  # 右侧占1份
        
        # 添加到主布局
        main_layout.addLayout(status_layout)
        main_layout.addLayout(middle_layout)
        
        self.setLayout(main_layout)
    
    def refresh_devices(self):
        """刷新设备列表"""
        self.status_label.setText("正在检测设备...")
        self.device_combo.clear()
        
        try:
            result = subprocess.run(['adb', 'devices'], capture_output=True, text=True, timeout=5)
            devices = []
            for line in result.stdout.strip().split('\n')[1:]:
                if line.strip() and '\tdevice' in line:
                    serial = line.split('\t')[0]
                    devices.append(serial)
            
            if devices:
                self.device_combo.addItems(devices)
                self.status_label.setText(f"已连接 {len(devices)} 台设备")
                self.status_label.setStyleSheet("""
                    QLabel {
                        background-color: #d4edda;
                        color: #155724;
                        padding: 5px;
                        border: 1px solid #c3e6cb;
                        font-weight: bold;
                    }
                """)
            else:
                self.status_label.setText("未检测到设备")
                self.status_label.setStyleSheet("""
                    QLabel {
                        background-color: #f8d7da;
                        color: #721c24;
                        padding: 5px;
                        border: 1px solid #f5c6cb;
                        font-weight: bold;
                    }
                """)
        except Exception as e:
            self.status_label.setText(f"ADB错误: {str(e)}")
            self.status_label.setStyleSheet("""
                QLabel {
                    background-color: #fff3cd;
                    color: #856404;
                    padding: 5px;
                    border: 1px solid #ffeaa7;
                    font-weight: bold;
                }
            """)
    
    def on_device_selected(self, serial):
        """选择设备"""
        self.device_serial = serial
        self.status_label.setText(f"已选择设备: {serial}")
    
    def insert_command(self, command, description):
        """插入命令到编辑器"""
        if not self.device_serial:
            QMessageBox.warning(self, "警告", "请先选择设备！")
            return
        
        full_command = f"adb -s {self.device_serial} shell {command}"
        
        # 添加延时
        if self.delay_enabled:
            full_command += "\nadb -s {self.device_serial} shell sleep 1"
        
        # 添加注释
        comment = f"\n# {description}\n{full_command}\n"
        
        self.script_editor.insertPlainText(comment)
    
    def toggle_delay(self, state):
        """切换延时"""
        self.delay_enabled = (state == Qt.Checked)
    
    def save_script(self):
        """保存脚本"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "保存脚本", "", "脚本文件 (*.txt);;所有文件 (*.*)"
        )
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self.script_editor.toPlainText())
            QMessageBox.information(self, "成功", "脚本保存成功！")
    
    def load_script(self):
        """加载脚本"""
        filename, _ = QFileDialog.getOpenFileName(
            self, "加载脚本", "", "脚本文件 (*.txt);;所有文件 (*.*)"
        )
        if filename:
            with open(filename, 'r', encoding='utf-8') as f:
                self.script_editor.setText(f.read())
    
    def run_script(self):
        """执行脚本"""
        if not self.device_serial:
            QMessageBox.warning(self, "警告", "请先选择设备！")
            return
        
        script = self.script_editor.toPlainText()
        if not script.strip():
            QMessageBox.warning(self, "警告", "脚本为空！")
            return
        
        # 执行每一行命令
        commands = script.split('\n')
        success_count = 0
        error_count = 0
        
        for line in commands:
            line = line.strip()
            if line and not line.startswith('#'):
                try:
                    # 替换占位符
                    if '{device}' in line:
                        line = line.replace('{device}', self.device_serial)
                    
                    # 执行命令
                    result = subprocess.run(
                        line, shell=True, capture_output=True, text=True, timeout=10
                    )
                    
                    if result.returncode == 0:
                        success_count += 1
                    else:
                        error_count += 1
                        
                except Exception as e:
                    error_count += 1
                    print(f"执行失败: {line}, 错误: {e}")
        
        QMessageBox.information(
            self, "执行完成", 
            f"执行完成！\n成功: {success_count} 条\n失败: {error_count} 条"
        )

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AutomationAssistantV2()
    window.show()
    sys.exit(app.exec_())
