# coding:utf-8
from PyQt5.QtWidgets import QWidget, QFormLayout
from PyQt5.QtGui import QValidator
from qfluentwidgets import Dialog, LineEdit, BodyLabel, SpinBox


class InputDialogView(Dialog):

    def __init__(self, title: str, parent=None):
        super().__init__(title=title, content='', parent=parent)
        self.windowTitleLabel.setVisible(True)
        self.contentLabel.hide()
        self.titleLabel.hide()
        self.textLayout.setContentsMargins(12, 12, 12, 12)
        self.textLayout.setSpacing(5)
        self.yesButton.setText(self.tr('确定'))
        self.cancelButton.setText(self.tr('取消'))

        self.view = QWidget()
        self.view.setObjectName("view")
        self.formLayout = QFormLayout(self)
        self.formLayout.setContentsMargins(24, 24, 24, 24)
        self.formLayout.setSpacing(15)
        self.vBoxLayout.insertLayout(2, self.formLayout)
        self.setFixedWidth(270)

    def addLineEdit(self, name: str, placeholderText: str, key: str, value: str = None,
                    validate: QValidator = None, readOnly: bool = False):
        lineEdit = LineEdit(self.view)
        lineEdit.setText(value)
        lineEdit.setPlaceholderText(placeholderText)
        lineEdit.setObjectName(key)
        lineEdit.setValidator(validate)
        lineEdit.setToolTip(placeholderText)
        lineEdit.setReadOnly(readOnly)

        label = BodyLabel(self.view)
        label.setText(name)

        row = self.formLayout.rowCount()
        self.formLayout.setWidget(row, QFormLayout.LabelRole, label)
        self.formLayout.setWidget(row, QFormLayout.FieldRole, lineEdit)

    def addSpinBox(self, name: str, placeholderText: str, key: str, value: int = None):
        spinBox = SpinBox(self.view)
        spinBox.setRange(1, 1000)
        if value:
            spinBox.setValue(value)
        spinBox.setToolTip(placeholderText)
        spinBox.setObjectName(key)

        label = BodyLabel(self.view)
        label.setText(name)

        row = self.formLayout.rowCount()
        self.formLayout.setWidget(row, QFormLayout.LabelRole, label)
        self.formLayout.setWidget(row, QFormLayout.FieldRole, spinBox)

    def getData(self) -> dict:
        result = {}

        lineEdits = self.findChildren(LineEdit)
        for line in lineEdits:
            key = line.objectName()
            value = line.text()
            result[key] = value

        spinBoxs = self.findChildren(SpinBox)
        for spin in spinBoxs:
            key = spin.objectName()
            value = spin.value()
            result[key] = value

        return result


