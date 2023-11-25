# coding:utf-8
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QValidator
from PyQt5.QtWidgets import QFrame, QFormLayout, QVBoxLayout, QWidget
from qfluentwidgets import (ScrollArea, BodyLabel, LineEdit, ComboBox, Slider,
                            SwitchButton, PrimaryPushButton, StrongBodyLabel, SpinBox)
from components.button.color_button import ColorButton
from components.combobox.font_combobox import FontComboBox


class FromWidget(QWidget):

    def __init__(self, promptText: str = None, parent=None):
        super().__init__(parent)
        self.view = QFrame()
        self.view.setObjectName('view')
        # 选项栏
        self.contentVBoxLayout = QVBoxLayout(self)
        self.simpleFormLayout = QFormLayout(self)
        self.simpleFormLayout.setSpacing(5)

        self.contentVBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.contentVBoxLayout.setSpacing(0)
        self.contentVBoxLayout.addLayout(self.simpleFormLayout)

        # 提示文本
        self.promptLabel = None
        self.addPromptText(promptText)

        # 设置主题
        self.setObjectName('fromWidget')

    def addPromptText(self, promptText: str = None):
        """ 添加提示文本 """
        if promptText and not self.promptLabel:
            self.promptLabel = BodyLabel(self.view)
            self.promptLabel.setText(promptText)
            self.contentVBoxLayout.addWidget(self.promptLabel, 0, Qt.AlignTop | Qt.AlignCenter)

    def delAll(self):
        """ 删除所有 """
        self.delPromptText()
        self.delViewLater()

    def delPromptText(self):
        """
        删除提示文本
        :return:
        """
        if self.promptLabel:
            self.contentVBoxLayout.removeWidget(self.promptLabel)
            self.promptLabel.deleteLater()
            self.promptLabel = None

    def delViewLater(self):
        """
        删除simpleFormLayout子控件
        :return:
        """
        for i in reversed(range(self.simpleFormLayout.count())):
            item = self.simpleFormLayout.itemAt(i)
            if item.widget() is not None:
                item.widget().deleteLater()
            self.simpleFormLayout.removeItem(item)
        self.update()

    def addLabelCard(self, name: str) -> StrongBodyLabel:
        """
        添加一行标签
        :param name:
        :return:
        """
        label = StrongBodyLabel(self.view)
        label.setText(name)

        labelView = BodyLabel(self.view)
        row = self.simpleFormLayout.rowCount()
        self.simpleFormLayout.setWidget(row, QFormLayout.LabelRole, label)
        self.simpleFormLayout.setWidget(row, QFormLayout.FieldRole, labelView)

        return label

    def addLineCard(self, name: str, placeholderText: str, readOnly: bool, value: any = None, validator: QValidator = None, callback=None) -> LineEdit:
        """
        添加输入控件
        :param name: 名称
        :param placeholderText: 提示符
        :param readOnly: 是否可编辑
        :param value: 是否默认值
        :param validator: 验证器
        :param callback: 回调函数
        :return:
        """
        label = BodyLabel(self.view)
        label.setText(name)

        lineEdit = LineEdit(self.view)
        lineEdit.setReadOnly(readOnly)
        lineEdit.setPlaceholderText(placeholderText)

        if value:
            lineEdit.setText(str(value))

        if validator:
            lineEdit.setValidator(validator)

        if callback:
            lineEdit.editingFinished.connect(callback)

        row = self.simpleFormLayout.rowCount()
        self.simpleFormLayout.setWidget(row, QFormLayout.LabelRole, label)
        self.simpleFormLayout.setWidget(row, QFormLayout.FieldRole, lineEdit)

        return lineEdit

    def addComboBoxCard(self, name: str, itemList: list, currentIndex: int = None, currentText: str = None,  callback=None) -> ComboBox:
        """
        添加多选控件
        :param name: 名称
        :param itemList: 内容 结构:[{"纵向打印": {"direction_type": 0}},{"横向打印": {"direction_type": 1}}]
        :param currentIndex: 默认选中
        :param currentText: 默认选中
        :param callback: 回调函数
        :return:
        """
        label = BodyLabel(self.view)
        label.setText(name)

        comboBox = ComboBox(self.view)
        for item in itemList:
            for key, value in item.items():
                comboBox.addItem(key, userData=value)

        if currentIndex:
            comboBox.setCurrentIndex(currentIndex)

        if currentText:
            comboBox.setCurrentText(currentText)

        if callback:
            comboBox.currentIndexChanged.connect(callback)

        row = self.simpleFormLayout.rowCount()
        self.simpleFormLayout.setWidget(row, QFormLayout.LabelRole, label)
        self.simpleFormLayout.setWidget(row, QFormLayout.FieldRole, comboBox)

        return comboBox

    def addSliderCard(self, name: str, min: int, max: int, value: int, callback=None) -> Slider:
        """
        添加滑动控件
        :param name: 名称
        :param min: 最小
        :param max: 最大
        :param value: 当前
        :param callback: 回调函数
        :return:
        """
        label = BodyLabel(self.view)
        label.setText(name)

        slider = Slider(Qt.Horizontal, self.view)
        slider.setMinimum(min)
        slider.setMaximum(max)
        slider.setValue(value)
        if callback:
            slider.sliderReleased.connect(callback)

        row = self.simpleFormLayout.rowCount()
        self.simpleFormLayout.setWidget(row, QFormLayout.LabelRole, label)
        self.simpleFormLayout.setWidget(row, QFormLayout.FieldRole, slider)

        return slider

    def addSwitchButtonCard(self, name: str, checked: bool, callback=None) -> SwitchButton:
        """
        添加开关控件
        :param name:
        :param checked:
        :param callback:
        :return:
        """
        label = BodyLabel(self.view)
        label.setText(name)

        switchButton = SwitchButton(self.view)
        switchButton.hBox.setAlignment(Qt.AlignHCenter)
        switchButton.setChecked(checked)
        if callback:
            switchButton.checkedChanged.connect(callback)

        row = self.simpleFormLayout.rowCount()
        self.simpleFormLayout.setWidget(row, QFormLayout.LabelRole, label)
        self.simpleFormLayout.setWidget(row, QFormLayout.FieldRole, switchButton)

        return switchButton

    def addColorButtonCard(self, name: str, colorHex: str, callback=None) -> ColorButton:
        """
        添加颜色控件
        :param name:
        :param colorHex:
        :param callback:
        :return:
        """
        label = BodyLabel(self.view)
        label.setText(name)

        colorButton = ColorButton(QColor(colorHex), '', self.view, enableAlpha=True)
        if callback:
            colorButton.colorChanged.connect(callback)

        row = self.simpleFormLayout.rowCount()
        self.simpleFormLayout.setWidget(row, QFormLayout.LabelRole, label)
        self.simpleFormLayout.setWidget(row, QFormLayout.FieldRole, colorButton)

        return colorButton

    def addPushButton(self, name: str, textName: str, toolTip: str = None, callback=None) -> PrimaryPushButton:
        """
        添加按钮控件
        :param toolTip:
        :param name:
        :param textName:
        :param callback:
        :return:
        """
        label = BodyLabel(self.view)
        label.setText(name)

        button = PrimaryPushButton(self.view)
        button.setText(textName)
        if toolTip:
            button.setToolTip(toolTip)
        if callback:
            button.clicked.connect(callback)

        row = self.simpleFormLayout.rowCount()
        self.simpleFormLayout.setWidget(row, QFormLayout.LabelRole, label)
        self.simpleFormLayout.setWidget(row, QFormLayout.FieldRole, button)

        return button

    def addFontComboBox(self, name: str, family: str, callback=None) -> FontComboBox:
        """
        添加字体选项
        :param name:
        :param family:
        :param callback:
        :return:
        """
        label = BodyLabel(self.view)
        label.setText(name)

        combobox = FontComboBox(self.view)
        if family not in combobox.all_fonts:
            combobox.addItem(family)
        combobox.setCurrentText(family)

        if callback:
            combobox.currentTextChanged.connect(callback)

        row = self.simpleFormLayout.rowCount()
        self.simpleFormLayout.setWidget(row, QFormLayout.LabelRole, label)
        self.simpleFormLayout.setWidget(row, QFormLayout.FieldRole, combobox)

        return combobox

    def addSpinBox(self, name: str, value: int, callback=None) -> SpinBox:
        """
        带调解按钮的SpinBox
        :param name:
        :param value:
        :param callback:
        :return:
        """
        label = BodyLabel(self.view)
        label.setText(name)

        spinbox = SpinBox(self.view)
        spinbox.setRange(30, 9999)
        spinbox.setSingleStep(1)
        spinbox.setValue(value)
        if callback:
            spinbox.textChanged.connect(callback)

        row = self.simpleFormLayout.rowCount()
        self.simpleFormLayout.setWidget(row, QFormLayout.LabelRole, label)
        self.simpleFormLayout.setWidget(row, QFormLayout.FieldRole, spinbox)
        return spinbox


class FromScrollAreaWidget(ScrollArea):

    def __init__(self, promptText: str = None, parent=None):
        super().__init__(parent)
        self.formWidget = FromWidget(promptText, parent)
        self.formWidget.resize(210, 800)
        self.setWidget(self.formWidget)
        self.setStyleSheet('background-color: transparent;')

    def addPromptText(self, promptText: str = None):
        self.formWidget.addPromptText(promptText)

    def delAll(self):
        self.formWidget.delAll()

    def delPromptText(self):
        self.formWidget.delPromptText()

    def delViewLater(self):
        self.formWidget.delViewLater()

    def addLabelCard(self, name: str) -> StrongBodyLabel:
        return self.formWidget.addLabelCard(name)

    def addLineCard(self, name: str, placeholderText: str, readOnly: bool, value: any = None, validator: QValidator = None, callback=None) -> LineEdit:
        return self.formWidget.addLineCard(name, placeholderText, readOnly, value, validator, callback)

    def addComboBoxCard(self, name: str, itemList: list, currentIndex: int = None, currentText: str = None,  callback=None) -> ComboBox:
        return self.formWidget.addComboBoxCard(name, itemList, currentIndex, currentText, callback)

    def addSliderCard(self, name: str, min: int, max: int, value: int, callback=None) -> Slider:
        return self.formWidget.addSliderCard(name, min, max, value, callback)

    def addSwitchButtonCard(self, name: str, checked: bool, callback=None) -> SwitchButton:
        return self.formWidget.addSwitchButtonCard(name, checked, callback)

    def addColorButtonCard(self, name: str, colorHex: str, callback=None) -> ColorButton:
        return self.formWidget.addColorButtonCard(name, colorHex, callback)

    def addPushButton(self, name: str, textName: str, toolTip: str = None, callback=None) -> PrimaryPushButton:
        return self.formWidget.addPushButton(name, textName, toolTip, callback)

    def addFontComboBox(self, name: str, family: str, callback=None) -> FontComboBox:
        return self.formWidget.addFontComboBox(name, family, callback)

    def addSpinBox(self, name: str, value: int, callback=None) -> SpinBox:
        return self.formWidget.addSpinBox(name, value, callback)
