# coding:utf-8
from PyQt5.QtCore import Qt, pyqtSignal, QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QWidget, QStackedLayout, QFileDialog
from qfluentwidgets import (StrongBodyLabel, CommandBar, Pivot, FluentIcon, Action, Dialog, StateToolTip)

from components.dialog.input_dialog import InputDialogView
from components.widget.from_widget import FromScrollAreaWidget
from components.widget.design_widget import DesignWidget
from components.validator.int_validator import IntValidator
from components.custom.preview_view import PreviewCardView
from common.file_util import copyImage

from server.service.paper_service import findItemAll
from server.service.template_base_service import save, findById


class SaveDialog(InputDialogView):

    def __init__(self, title: str, values: dict = None, parent=None):
        super().__init__(title, parent)
        self.addLineEdit(name=self.tr('模板编码:'),
                         placeholderText=self.tr('请输入模板编码,不输入则自动生成,请保证唯一性'),
                         key='templateCode',
                         value=values['templateCode'] if values and values['templateCode'] else None,
                         readOnly=True if values and values['templateCode'] else False)
        self.addLineEdit(name=self.tr('模板名称:'),
                         placeholderText=self.tr('请输入模板名称'),
                         key='name',
                         value=values['name'] if values and values['name'] else None,
                         validate=QRegExpValidator(QRegExp(".{1,10}"), self))
        self.addLineEdit(name=self.tr('备注:'),
                         placeholderText=self.tr('请输入备注,可不填'),
                         key='remark',
                         value=values['remark'] if values and values['remark'] else None,
                         validate=QRegExpValidator(QRegExp(".{1,50}"), self))


"""
模板设计View
"""

printerItemData = [{"纵向打印": {"direction_type": 0}}, {"横向打印": {"direction_type": 1}}]


class TemplateBroadsideWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.broadsidePivot = Pivot(self)
        self.simpleForm = FromScrollAreaWidget(parent=self)
        self.detailForm = FromScrollAreaWidget(promptText="请选中右侧的控件", parent=self)
        # 侧边栏
        self.broadsideVBoxLayout = QVBoxLayout(self)
        # 侧边切换
        self.stackedLayout = QStackedLayout(self)
        self.__initWidget()

        self.setFixedWidth(225)

    def __initWidget(self):
        # broadsidePivot
        self.broadsidePivot.addItem("basic_settings", "基本设置",
                                    onClick=lambda: self.stackedLayout.setCurrentIndex(0), icon=FluentIcon.SETTING)
        self.broadsidePivot.addItem("advanced_properties", "高级属性",
                                    onClick=lambda: self.stackedLayout.setCurrentIndex(1), icon=FluentIcon.MIX_VOLUMES)
        self.broadsidePivot.setItemFontSize(12)
        self.broadsidePivot.setCurrentItem("basic_settings")

        self.broadsideVBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.broadsideVBoxLayout.setSpacing(12)
        self.broadsideVBoxLayout.addWidget(self.broadsidePivot)
        self.broadsideVBoxLayout.addLayout(self.stackedLayout)
        # simpleForm
        self.stackedLayout.setContentsMargins(0, 0, 0, 0)
        self.stackedLayout.setSpacing(12)
        self.stackedLayout.addWidget(self.simpleForm)
        self.stackedLayout.addWidget(self.detailForm)


class TemplateCardView(QWidget):
    returnActionChanged = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.view = QFrame(self)
        self.titleLibraryLabel = StrongBodyLabel(self.tr('模板设计'), self.view)
        self.titleCommandBar = CommandBar(self.view)
        self.broadsideWidget = TemplateBroadsideWidget(self.view)
        self.contentWidget = DesignWidget(self.view)

        # 整个布局
        self.contentVBoxLayout = QVBoxLayout(self)
        # 设计栏
        self.designHBoxLayout = QHBoxLayout(self)

        # 模板参数
        self.templateId = None
        self.templateCode = None
        self.templateName = None
        self.templateRemark = None

        self.__initLayout()
        self.initWidget()
        self.setFixedSize(1300, 750)

    def __initLayout(self):
        self.contentVBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.contentVBoxLayout.setSpacing(6)
        self.contentVBoxLayout.addWidget(self.titleLibraryLabel)
        self.contentVBoxLayout.addWidget(self.titleCommandBar)
        self.contentVBoxLayout.addLayout(self.designHBoxLayout)

        self.designHBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.designHBoxLayout.setSpacing(10)
        self.designHBoxLayout.addWidget(self.broadsideWidget)
        self.designHBoxLayout.addWidget(self.contentWidget)

        # titleCommandBar
        self.titleCommandBar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        returnAction = Action(FluentIcon.RETURN, self.tr('返回'))
        returnAction.triggered.connect(self.__onReturnActionChanged)
        saveAction = Action(FluentIcon.SAVE, self.tr('保存'))
        saveAction.triggered.connect(self.__onSaveActionChanged)
        deleteAction = Action(FluentIcon.DELETE, self.tr('删除'))
        deleteAction.triggered.connect(self.__onDeleteActionChanged)
        backgroundAction = Action(FluentIcon.PHOTO, self.tr('背景'))
        backgroundAction.triggered.connect(self.__onBackgroundActionChanged)
        self.titleCommandBar.addActions([
            returnAction,
            saveAction,
            deleteAction,
            backgroundAction,
        ])
        self.titleCommandBar.addSeparator()
        viewAction = Action(FluentIcon.VIEW, self.tr('预览'), checkable=True)
        viewAction.triggered.connect(self.__onViewActionChanged)
        refreshAction = Action(FluentIcon.SYNC, self.tr('刷新'))
        refreshAction.triggered.connect(self.__onRefreshActionChanged)
        self.titleCommandBar.addActions([
            viewAction,
            refreshAction
        ])

    def __onReturnActionChanged(self):
        w = Dialog(self.tr('返回'), self.tr('确定返回吗?设计的内容将不会被自动保存!'), self)
        w.setTitleBarVisible(False)
        if w.exec():
            self.broadsideWidget.detailForm.delViewLater()
            self.broadsideWidget.detailForm.addPromptText('请选中右侧的控件')
            self.contentWidget.contentWidget.resetWidget()
            self.templateId = None
            self.templateCode = None
            self.templateName = None
            self.templateRemark = None
            self.returnActionChanged.emit()

    def __onSaveActionChanged(self):
        values = {'name': self.templateName, 'remark': self.templateRemark, 'templateCode': self.templateCode}
        w = SaveDialog(title=self.tr('保存'), values=values, parent=self)
        if w.exec():
            stateTooltip = StateToolTip('正在保存模板', '客官请耐心等待哦~~', self)
            stateTooltip.move(1020, 70)
            stateTooltip.show()
            data = w.getData()
            templateData = self.contentWidget.getContentWidgetData()
            templateData['paperInfo']['id'] = self.templateId
            self.templateCode = data['templateCode']
            templateData['paperInfo']['code'] = self.templateCode
            self.templateName = data['name']
            self.templateNameWidget.setText(self.templateName)
            templateData['paperInfo']['name'] = self.templateName
            self.templateRemark = data['remark']
            templateData['paperInfo']['remark'] = self.templateRemark
            save(templateData, self)
            stateTooltip.setContent('模板训练完成啦 😆')
            stateTooltip.setState(True)
            stateTooltip.deleteLater()

    def __onDeleteActionChanged(self):
        w = Dialog(self.tr('删除'), self.tr('确定删除吗?将删除当前选中的控件!'), self)
        w.setTitleBarVisible(False)
        if w.exec():
            self.contentWidget.delCurrentSelectedWidget()

    def __onBackgroundActionChanged(self):
        openFile = QFileDialog.getOpenFileName(self, '选中背景图片', './',
                                               'background png(*.png);;background jpg(*.jpg)',
                                               'background png(*.png);;background jpg(*.jpg)')
        if openFile and openFile[0]:
            self.contentWidget.setContentWidgetBackgroundImage(copyImage(openFile[0]))

    def __onViewActionChanged(self):
        preview = PreviewCardView(self)
        preview.copyContentWidget(self.contentWidget.contentWidget)
        preview.exec_()

    def __onRefreshActionChanged(self):
        dbTemplate = None
        if self.templateId:
            dbTemplate = findById(self.templateId)
        self.initSimpleSetting(dbTemplate)

    def initWidget(self, id: int = None):
        dbTemplate = None
        if id:
            dbTemplate = findById(id)
            self.templateId = dbTemplate['id']
            self.templateCode = dbTemplate['code']
            self.templateName = dbTemplate['name']
            self.templateRemark = dbTemplate['remark']
        # 初始化纸张模型
        self.contentWidget.initContentWidget(self.broadsideWidget.detailForm, dbTemplate)

        self.initSimpleSetting(dbTemplate)

    def initSimpleSetting(self, dbTemplate: dict = None):
        # 基本设置
        self.broadsideWidget.simpleForm.delViewLater()
        self.broadsideWidget.simpleForm.addLabelCard(self.tr('纸张设置'))
        # 模板名称
        self.templateNameWidget = self.broadsideWidget.simpleForm.addLineCard(
            self.tr('模板名称:'),
            self.tr('请输入模板名称'),
            False,
            value=self.templateName,
            callback=self.__onTemplateNameWidgetFinished
        )
        # 纸张
        paperItemList = findItemAll()
        paperKey = list(paperItemList[0].keys())[0]
        paperItem = paperItemList[0].get(paperKey)
        self.paperNameWidget = self.broadsideWidget.simpleForm.addComboBoxCard(
            self.tr('纸张:'),
            paperItemList,
            currentText=dbTemplate['paper_name'] if dbTemplate else paperKey,
            callback=self.__onPaperNameWidgetChanged
        )
        # 打印方向
        self.directionWidget = self.broadsideWidget.simpleForm.addComboBoxCard(
            self.tr('打印方向:'),
            printerItemData,
            currentText=dbTemplate['direction'] if dbTemplate else '纵向打印',
            callback=self.__onDirectionWidgetChanged
        )
        # 纸张宽度
        self.paperWidthWidget = self.broadsideWidget.simpleForm.addLineCard(
            self.tr('纸张宽度:'),
            self.tr('请输入纸张宽度'),
            True,
            dbTemplate['paper_width'] if dbTemplate else paperItem['release_width']
        )
        # 纸张高度
        self.paperHeightWidget = self.broadsideWidget.simpleForm.addLineCard(
            self.tr('纸张高度:'),
            self.tr('请输入纸张高度'),
            True,
            dbTemplate['paper_height'] if dbTemplate else paperItem['release_height']
        )
        # 左边距
        self.leftMarginWidget = self.broadsideWidget.simpleForm.addLineCard(
            self.tr('左边距:'),
            self.tr('请输入左边距'),
            False,
            dbTemplate['left_margin'] if dbTemplate else '30',
            validator=IntValidator(),
            callback=self.__onLeftMarginWidgetFinished
        )
        # 右边距
        self.rightMarginWidget = self.broadsideWidget.simpleForm.addLineCard(
            self.tr('右边距:'),
            self.tr('请输入右边距'),
            False,
            dbTemplate['right_margin'] if dbTemplate else '30',
            validator=IntValidator(),
            callback=self.__onRightMarginWidgetFinished
        )
        # 上边距
        self.topMarginWidget = self.broadsideWidget.simpleForm.addLineCard(
            self.tr('上边距:'),
            self.tr('请输入上边距'),
            False,
            dbTemplate['top_margin'] if dbTemplate else '30',
            validator=IntValidator(),
            callback=self.__onTopMarginWidgetFinished
        )
        # 下边距
        self.bottomMarginWidget = self.broadsideWidget.simpleForm.addLineCard(
            self.tr('下边距:'),
            self.tr('请输入下边距'),
            False,
            dbTemplate['bottom_margin'] if dbTemplate else '30',
            validator=IntValidator(),
            callback=self.__onBottomMarginWidgetFinished
        )
        self.broadsideWidget.simpleForm.addPushButton(
            self.tr('移除背景:'),
            self.tr('确认'),
            self.tr('尝试移除右侧的背景图片'),
            self.__onRemoveBackgroundImageChanged
        )
        self.broadsideWidget.simpleForm.addLabelCard(self.tr('纸张控件'))
        # 图片按钮
        self.broadsideWidget.simpleForm.addPushButton(
            self.tr('图片:'),
            self.tr('添加'),
            self.tr('在右侧添加图片组件'),
            self.__onAddImageLabelChanged
        )
        # 单行文本按钮
        self.broadsideWidget.simpleForm.addPushButton(
            self.tr('单行文本:'),
            self.tr('添加'),
            self.tr('在右侧添加单行文本组件'),
            self.__onAddEditLabelChanged
        )
        # 表格按钮
        self.broadsideWidget.simpleForm.addPushButton(
            self.tr('表格:'),
            self.tr('添加'),
            self.tr('在右侧添加表格组件,注:一个模板中只能有一张表格'),
            self.__onAddTableChanged
        )

    def __onTemplateNameWidgetFinished(self):
        text = self.templateNameWidget.text()
        self.templateName = text

    def __onPaperNameWidgetChanged(self):
        self.__onDirectionWidgetChanged()

    def __onDirectionWidgetChanged(self):
        paperName = self.paperNameWidget.currentText()
        directionType = self.directionWidget.currentData()['direction_type']
        direction = self.directionWidget.currentText()
        paperData = self.paperNameWidget.currentData()
        if directionType == 0:
            widgetWidth = paperData['release_width']
            widgetHeight = paperData['release_height']
        else:
            widgetWidth = paperData['lateral_width']
            widgetHeight = paperData['lateral_height']

        self.paperWidthWidget.setText(str(widgetWidth))
        self.paperHeightWidget.setText(str(widgetHeight))
        self.contentWidget.resetContentWidget(width=widgetWidth, height=widgetHeight, direction=direction, paperName=paperName)

    def __onLeftMarginWidgetFinished(self):
        text = self.leftMarginWidget.text()
        self.contentWidget.setContentWidgetMargin(left=int(text))

    def __onRightMarginWidgetFinished(self):
        text = self.rightMarginWidget.text()
        self.contentWidget.setContentWidgetMargin(right=int(text))

    def __onTopMarginWidgetFinished(self):
        text = self.topMarginWidget.text()
        self.contentWidget.setContentWidgetMargin(top=int(text))

    def __onBottomMarginWidgetFinished(self):
        text = self.bottomMarginWidget.text()
        self.contentWidget.setContentWidgetMargin(bottom=int(text))

    def __onRemoveBackgroundImageChanged(self):
        self.contentWidget.removeContentWidgetBackgroundImage()

    def __onAddEditLabelChanged(self):
        self.contentWidget.addSimpleEditLabel(self.broadsideWidget.detailForm)

    def __onAddImageLabelChanged(self):
        self.contentWidget.addSimpleImage(self.broadsideWidget.detailForm)

    def __onAddTableChanged(self):
        self.contentWidget.addSimpleTable(self.broadsideWidget.detailForm)
