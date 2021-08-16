# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/main_frame.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(1404, 1090)
        Frame.setMinimumSize(QtCore.QSize(1400, 1080))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(12)
        Frame.setFont(font)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(Frame)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.frame = QtWidgets.QFrame(Frame)
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(16)
        self.frame.setFont(font)
        self.frame.setFrameShape(QtWidgets.QFrame.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.launch_button = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.launch_button.sizePolicy().hasHeightForWidth())
        self.launch_button.setSizePolicy(sizePolicy)
        self.launch_button.setMinimumSize(QtCore.QSize(75, 75))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("gui\\../icons/launch.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.launch_button.setIcon(icon)
        self.launch_button.setIconSize(QtCore.QSize(50, 50))
        self.launch_button.setObjectName("launch_button")
        self.horizontalLayout.addWidget(self.launch_button)
        self.status_label = QtWidgets.QLabel(self.frame)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.status_label.setPalette(palette)
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)
        self.status_label.setObjectName("status_label")
        self.horizontalLayout.addWidget(self.status_label)
        self.status_info_label = QtWidgets.QLabel(self.frame)
        self.status_info_label.setAlignment(QtCore.Qt.AlignCenter)
        self.status_info_label.setObjectName("status_info_label")
        self.horizontalLayout.addWidget(self.status_info_label)
        self.timer_label = QtWidgets.QLabel(self.frame)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.timer_label.setPalette(palette)
        self.timer_label.setText("")
        self.timer_label.setAlignment(QtCore.Qt.AlignCenter)
        self.timer_label.setObjectName("timer_label")
        self.horizontalLayout.addWidget(self.timer_label)
        self.start_button = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.start_button.sizePolicy().hasHeightForWidth())
        self.start_button.setSizePolicy(sizePolicy)
        self.start_button.setMinimumSize(QtCore.QSize(75, 75))
        self.start_button.setIconSize(QtCore.QSize(50, 50))
        self.start_button.setObjectName("start_button")
        self.horizontalLayout.addWidget(self.start_button)
        self.verticalLayout_7.addWidget(self.frame)
        self.frame_17 = QtWidgets.QFrame(Frame)
        self.frame_17.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_17.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_17.setObjectName("frame_17")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.frame_17)
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_10.setSpacing(0)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.frame_8 = QtWidgets.QFrame(self.frame_17)
        self.frame_8.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_8.setObjectName("frame_8")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.frame_8)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.frame_3 = QtWidgets.QFrame(self.frame_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy)
        self.frame_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame_7 = QtWidgets.QFrame(self.frame_3)
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.frame_7)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setSpacing(18)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.frame_11 = QtWidgets.QFrame(self.frame_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_11.sizePolicy().hasHeightForWidth())
        self.frame_11.setSizePolicy(sizePolicy)
        self.frame_11.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_11.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_11.setObjectName("frame_11")
        self.formLayout_2 = QtWidgets.QFormLayout(self.frame_11)
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_8 = QtWidgets.QLabel(self.frame_11)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.label = QtWidgets.QLabel(self.frame_11)
        self.label.setObjectName("label")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label)
        self.team_label = QtWidgets.QLabel(self.frame_11)
        self.team_label.setText("")
        self.team_label.setObjectName("team_label")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.team_label)
        self.label_14 = QtWidgets.QLabel(self.frame_11)
        self.label_14.setObjectName("label_14")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_14)
        self.loop_count_label = QtWidgets.QLabel(self.frame_11)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.loop_count_label.setPalette(palette)
        self.loop_count_label.setText("")
        self.loop_count_label.setObjectName("loop_count_label")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.loop_count_label)
        self.label_15 = QtWidgets.QLabel(self.frame_11)
        self.label_15.setObjectName("label_15")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_15)
        self.error_count_label = QtWidgets.QLabel(self.frame_11)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.error_count_label.setPalette(palette)
        self.error_count_label.setText("")
        self.error_count_label.setObjectName("error_count_label")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.error_count_label)
        self.label_16 = QtWidgets.QLabel(self.frame_11)
        self.label_16.setObjectName("label_16")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_16)
        self.frame_9 = QtWidgets.QFrame(self.frame_11)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 170, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.frame_9.setPalette(palette)
        self.frame_9.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_9.setObjectName("frame_9")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_9)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.gold_current_label = QtWidgets.QLabel(self.frame_9)
        self.gold_current_label.setText("")
        self.gold_current_label.setObjectName("gold_current_label")
        self.horizontalLayout_3.addWidget(self.gold_current_label)
        self.gold_gained_label = QtWidgets.QLabel(self.frame_9)
        self.gold_gained_label.setText("")
        self.gold_gained_label.setObjectName("gold_gained_label")
        self.horizontalLayout_3.addWidget(self.gold_gained_label)
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.frame_9)
        self.label_17 = QtWidgets.QLabel(self.frame_11)
        self.label_17.setObjectName("label_17")
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_17)
        self.frame_13 = QtWidgets.QFrame(self.frame_11)
        self.frame_13.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_13.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_13.setObjectName("frame_13")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.frame_13)
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_8.setSpacing(6)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.world_wins_label = QtWidgets.QLabel(self.frame_13)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.world_wins_label.setPalette(palette)
        self.world_wins_label.setText("")
        self.world_wins_label.setObjectName("world_wins_label")
        self.horizontalLayout_8.addWidget(self.world_wins_label)
        self.world_losses_label = QtWidgets.QLabel(self.frame_13)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.world_losses_label.setPalette(palette)
        self.world_losses_label.setText("")
        self.world_losses_label.setObjectName("world_losses_label")
        self.horizontalLayout_8.addWidget(self.world_losses_label)
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.frame_13)
        self.label_20 = QtWidgets.QLabel(self.frame_11)
        self.label_20.setObjectName("label_20")
        self.formLayout_2.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_20)
        self.frame_14 = QtWidgets.QFrame(self.frame_11)
        self.frame_14.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_14.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_14.setObjectName("frame_14")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.frame_14)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setSpacing(6)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.arena_wins_label = QtWidgets.QLabel(self.frame_14)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.arena_wins_label.setPalette(palette)
        self.arena_wins_label.setText("")
        self.arena_wins_label.setObjectName("arena_wins_label")
        self.horizontalLayout_7.addWidget(self.arena_wins_label)
        self.arena_losses_label = QtWidgets.QLabel(self.frame_14)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.arena_losses_label.setPalette(palette)
        self.arena_losses_label.setText("")
        self.arena_losses_label.setObjectName("arena_losses_label")
        self.horizontalLayout_7.addWidget(self.arena_losses_label)
        self.formLayout_2.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.frame_14)
        self.label_13 = QtWidgets.QLabel(self.frame_11)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.formLayout_2.setWidget(7, QtWidgets.QFormLayout.SpanningRole, self.label_13)
        self.items_gained_table = QtWidgets.QTableWidget(self.frame_11)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.items_gained_table.sizePolicy().hasHeightForWidth())
        self.items_gained_table.setSizePolicy(sizePolicy)
        self.items_gained_table.setMaximumSize(QtCore.QSize(16777215, 153))
        self.items_gained_table.setObjectName("items_gained_table")
        self.items_gained_table.setColumnCount(2)
        self.items_gained_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.items_gained_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.items_gained_table.setHorizontalHeaderItem(1, item)
        self.formLayout_2.setWidget(8, QtWidgets.QFormLayout.SpanningRole, self.items_gained_table)
        self.horizontalLayout_6.addWidget(self.frame_11)
        self.horizontalLayout_2.addWidget(self.frame_7)
        self.line_4 = QtWidgets.QFrame(self.frame_3)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setObjectName("line_4")
        self.horizontalLayout_2.addWidget(self.line_4)
        self.frame_5 = QtWidgets.QFrame(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_5.sizePolicy().hasHeightForWidth())
        self.frame_5.setSizePolicy(sizePolicy)
        self.frame_5.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_5)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_5 = QtWidgets.QLabel(self.frame_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_4.addWidget(self.label_5)
        self.scrollArea = QtWidgets.QScrollArea(self.frame_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setMinimumSize(QtCore.QSize(300, 357))
        self.scrollArea.setMaximumSize(QtCore.QSize(16777215, 357))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.widget = QtWidgets.QWidget()
        self.widget.setGeometry(QtCore.QRect(0, 0, 298, 355))
        self.widget.setObjectName("widget")
        self.ninja_info_area = QtWidgets.QVBoxLayout(self.widget)
        self.ninja_info_area.setObjectName("ninja_info_area")
        self.scrollArea.setWidget(self.widget)
        self.verticalLayout_4.addWidget(self.scrollArea)
        self.horizontalLayout_2.addWidget(self.frame_5)
        self.line = QtWidgets.QFrame(self.frame_3)
        self.line.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setObjectName("line")
        self.horizontalLayout_2.addWidget(self.line)
        self.frame_6 = QtWidgets.QFrame(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_6.sizePolicy().hasHeightForWidth())
        self.frame_6.setSizePolicy(sizePolicy)
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.formLayout = QtWidgets.QFormLayout(self.frame_6)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label_3 = QtWidgets.QLabel(self.frame_6)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.label_3)
        self.label_11 = QtWidgets.QLabel(self.frame_6)
        self.label_11.setObjectName("label_11")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_11)
        self.frame_10 = QtWidgets.QFrame(self.frame_6)
        self.frame_10.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_10.setObjectName("frame_10")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.frame_10)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.sleep_lower_number = QtWidgets.QSpinBox(self.frame_10)
        self.sleep_lower_number.setMaximum(10000)
        self.sleep_lower_number.setObjectName("sleep_lower_number")
        self.horizontalLayout_5.addWidget(self.sleep_lower_number)
        self.label_26 = QtWidgets.QLabel(self.frame_10)
        self.label_26.setAlignment(QtCore.Qt.AlignCenter)
        self.label_26.setObjectName("label_26")
        self.horizontalLayout_5.addWidget(self.label_26)
        self.sleep_upper_number = QtWidgets.QSpinBox(self.frame_10)
        self.sleep_upper_number.setMaximum(10000)
        self.sleep_upper_number.setObjectName("sleep_upper_number")
        self.horizontalLayout_5.addWidget(self.sleep_upper_number)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.frame_10)
        self.line_2 = QtWidgets.QFrame(self.frame_6)
        self.line_2.setMinimumSize(QtCore.QSize(0, 0))
        self.line_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setObjectName("line_2")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self.line_2)
        self.label_9 = QtWidgets.QLabel(self.frame_6)
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_9)
        self.label_7 = QtWidgets.QLabel(self.frame_6)
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.world_behavior_combobox = QtWidgets.QComboBox(self.frame_6)
        self.world_behavior_combobox.setObjectName("world_behavior_combobox")
        self.world_behavior_combobox.addItem("")
        self.world_behavior_combobox.addItem("")
        self.world_behavior_combobox.addItem("")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.world_behavior_combobox)
        self.label_10 = QtWidgets.QLabel(self.frame_6)
        self.label_10.setObjectName("label_10")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_10)
        self.line_3 = QtWidgets.QFrame(self.frame_6)
        self.line_3.setMinimumSize(QtCore.QSize(0, 0))
        self.line_3.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setObjectName("line_3")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.SpanningRole, self.line_3)
        self.label_12 = QtWidgets.QLabel(self.frame_6)
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.LabelRole, self.label_12)
        self.label_18 = QtWidgets.QLabel(self.frame_6)
        self.label_18.setObjectName("label_18")
        self.formLayout.setWidget(10, QtWidgets.QFormLayout.LabelRole, self.label_18)
        self.arena_energy_cap_number = QtWidgets.QSpinBox(self.frame_6)
        self.arena_energy_cap_number.setObjectName("arena_energy_cap_number")
        self.formLayout.setWidget(10, QtWidgets.QFormLayout.FieldRole, self.arena_energy_cap_number)
        self.label_19 = QtWidgets.QLabel(self.frame_6)
        self.label_19.setObjectName("label_19")
        self.formLayout.setWidget(11, QtWidgets.QFormLayout.LabelRole, self.label_19)
        self.arena_rematches_only_checkbox = QtWidgets.QCheckBox(self.frame_6)
        self.arena_rematches_only_checkbox.setObjectName("arena_rematches_only_checkbox")
        self.formLayout.setWidget(11, QtWidgets.QFormLayout.FieldRole, self.arena_rematches_only_checkbox)
        self.label_21 = QtWidgets.QLabel(self.frame_6)
        self.label_21.setObjectName("label_21")
        self.formLayout.setWidget(12, QtWidgets.QFormLayout.LabelRole, self.label_21)
        self.arena_wins_only_checkbox = QtWidgets.QCheckBox(self.frame_6)
        self.arena_wins_only_checkbox.setObjectName("arena_wins_only_checkbox")
        self.formLayout.setWidget(12, QtWidgets.QFormLayout.FieldRole, self.arena_wins_only_checkbox)
        self.submit_settings_button = QtWidgets.QPushButton(self.frame_6)
        self.submit_settings_button.setObjectName("submit_settings_button")
        self.formLayout.setWidget(15, QtWidgets.QFormLayout.SpanningRole, self.submit_settings_button)
        self.line_8 = QtWidgets.QFrame(self.frame_6)
        self.line_8.setMinimumSize(QtCore.QSize(0, 0))
        self.line_8.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_8.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_8.setObjectName("line_8")
        self.formLayout.setWidget(13, QtWidgets.QFormLayout.SpanningRole, self.line_8)
        self.world_mission_text = QtWidgets.QLineEdit(self.frame_6)
        self.world_mission_text.setObjectName("world_mission_text")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.world_mission_text)
        self.reset_settings_button = QtWidgets.QPushButton(self.frame_6)
        self.reset_settings_button.setObjectName("reset_settings_button")
        self.formLayout.setWidget(14, QtWidgets.QFormLayout.SpanningRole, self.reset_settings_button)
        self.horizontalLayout_2.addWidget(self.frame_6)
        self.verticalLayout_6.addWidget(self.frame_3)
        self.line_5 = QtWidgets.QFrame(self.frame_8)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setObjectName("line_5")
        self.verticalLayout_6.addWidget(self.line_5)
        self.frame_2 = QtWidgets.QFrame(self.frame_8)
        self.frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)
        self.frame_15 = QtWidgets.QFrame(self.frame_2)
        self.frame_15.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_15.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_15.setObjectName("frame_15")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.frame_15)
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_9.setSpacing(18)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.item_recipe_tree = QtWidgets.QTreeWidget(self.frame_15)
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(12)
        self.item_recipe_tree.setFont(font)
        self.item_recipe_tree.setObjectName("item_recipe_tree")
        self.horizontalLayout_9.addWidget(self.item_recipe_tree)
        self.item_location_table = QtWidgets.QTableWidget(self.frame_15)
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(12)
        self.item_location_table.setFont(font)
        self.item_location_table.setObjectName("item_location_table")
        self.item_location_table.setColumnCount(4)
        self.item_location_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.item_location_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.item_location_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.item_location_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.item_location_table.setHorizontalHeaderItem(3, item)
        self.horizontalLayout_9.addWidget(self.item_location_table)
        self.verticalLayout_3.addWidget(self.frame_15)
        self.verticalLayout_6.addWidget(self.frame_2)
        self.line_6 = QtWidgets.QFrame(self.frame_8)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setObjectName("line_6")
        self.verticalLayout_6.addWidget(self.line_6)
        self.frame_4 = QtWidgets.QFrame(self.frame_8)
        self.frame_4.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_4 = QtWidgets.QLabel(self.frame_4)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_5.addWidget(self.label_4)
        self.notes_textbox = QtWidgets.QTextBrowser(self.frame_4)
        self.notes_textbox.setReadOnly(False)
        self.notes_textbox.setObjectName("notes_textbox")
        self.verticalLayout_5.addWidget(self.notes_textbox)
        self.verticalLayout_6.addWidget(self.frame_4)
        self.horizontalLayout_10.addWidget(self.frame_8)
        self.line_7 = QtWidgets.QFrame(self.frame_17)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Plain)
        self.line_7.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_7.setObjectName("line_7")
        self.horizontalLayout_10.addWidget(self.line_7)
        self.frame_12 = QtWidgets.QFrame(self.frame_17)
        self.frame_12.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_12.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_12.setObjectName("frame_12")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_12)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_22 = QtWidgets.QLabel(self.frame_12)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_22.setFont(font)
        self.label_22.setObjectName("label_22")
        self.verticalLayout.addWidget(self.label_22)
        self.logs_textbox = QtWidgets.QTextBrowser(self.frame_12)
        font = QtGui.QFont()
        font.setFamily("Courier New")
        self.logs_textbox.setFont(font)
        self.logs_textbox.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.logs_textbox.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.logs_textbox.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.logs_textbox.setObjectName("logs_textbox")
        self.verticalLayout.addWidget(self.logs_textbox)
        self.horizontalLayout_10.addWidget(self.frame_12)
        self.verticalLayout_7.addWidget(self.frame_17)

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "Frame"))
        self.status_label.setText(_translate("Frame", "OK"))
        self.status_info_label.setText(_translate("Frame", "waiting to start"))
        self.label_8.setText(_translate("Frame", "Summary"))
        self.label.setText(_translate("Frame", "Team"))
        self.label_14.setText(_translate("Frame", "Loop #"))
        self.label_15.setText(_translate("Frame", "Error Count"))
        self.label_16.setText(_translate("Frame", "Gold"))
        self.label_17.setText(_translate("Frame", "World"))
        self.label_20.setText(_translate("Frame", "Arena"))
        self.label_13.setText(_translate("Frame", "Items Obtained"))
        item = self.items_gained_table.horizontalHeaderItem(0)
        item.setText(_translate("Frame", "qty"))
        item = self.items_gained_table.horizontalHeaderItem(1)
        item.setText(_translate("Frame", "item"))
        self.label_5.setText(_translate("Frame", "Ninja Info"))
        self.label_3.setText(_translate("Frame", "Settings"))
        self.label_11.setText(_translate("Frame", "Sleep Duration"))
        self.label_26.setText(_translate("Frame", "to"))
        self.label_9.setText(_translate("Frame", "World"))
        self.label_7.setText(_translate("Frame", "Behavior"))
        self.world_behavior_combobox.setItemText(0, _translate("Frame", "Manual"))
        self.world_behavior_combobox.setItemText(1, _translate("Frame", "Item Hunter"))
        self.world_behavior_combobox.setItemText(2, _translate("Frame", "World Progression"))
        self.label_10.setText(_translate("Frame", "Mission"))
        self.label_12.setText(_translate("Frame", "Arena"))
        self.label_18.setText(_translate("Frame", "Energy Cap"))
        self.label_19.setText(_translate("Frame", "Rematches Only?"))
        self.arena_rematches_only_checkbox.setText(_translate("Frame", "yes"))
        self.label_21.setText(_translate("Frame", "Prioritize Wins?"))
        self.arena_wins_only_checkbox.setText(_translate("Frame", "yes"))
        self.submit_settings_button.setText(_translate("Frame", "Submit"))
        self.reset_settings_button.setText(_translate("Frame", "Reset"))
        self.label_2.setText(_translate("Frame", "Item Helper"))
        self.item_recipe_tree.headerItem().setText(0, _translate("Frame", "Item"))
        self.item_recipe_tree.headerItem().setText(1, _translate("Frame", "Recipe"))
        self.item_recipe_tree.headerItem().setText(2, _translate("Frame", "Need"))
        self.item_recipe_tree.headerItem().setText(3, _translate("Frame", "Have"))
        item = self.item_location_table.horizontalHeaderItem(0)
        item.setText(_translate("Frame", "Item"))
        item = self.item_location_table.horizontalHeaderItem(1)
        item.setText(_translate("Frame", "Chance"))
        item = self.item_location_table.horizontalHeaderItem(2)
        item.setText(_translate("Frame", "Difficulty"))
        item = self.item_location_table.horizontalHeaderItem(3)
        item.setText(_translate("Frame", "Location"))
        self.label_4.setText(_translate("Frame", "Notes"))
        self.label_22.setText(_translate("Frame", "Logs"))
