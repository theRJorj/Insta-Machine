from PyQt5 import QtCore, QtGui, QtWidgets
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sqlite3
import requests
import time
import re
import pickle
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import os
import shutil
import random
import ast
import cv2
import pytesseract
import threading
from subprocess import CREATE_NO_WINDOW
from selenium.webdriver.chrome.service import Service as ChromeService

# SQLite database connection setup

conn = sqlite3.connect("machine.db", check_same_thread=False)
mycursor = conn.cursor()

# Check if neseccary folders exist

if not os.path.exists(r"Screenshots"):
    os.makedirs(r"Screenshots")
if not os.path.exists(r"Insta image"):
    os.makedirs(r"Insta image")
if not os.path.exists(r"logins/cookies"):
    os.makedirs(r"logins/cookies")
if not os.path.exists(r"links_lists/links_progress"):
    os.makedirs(r"links_lists/links_progress")

# Image to binary converter


def image_to_binary(filename):
    with open(filename, "rb") as file:
        imgdata = file.read()
    return imgdata


# Report bot sub-catagories

r1 = [
    "Nudity or pornography",
    "Sexual exploitation or solicitation",
    "Sharing private images",
    "Involves a child",
]
r2 = [
    "Violent threat",
    "Animal abuse",
    "Death or severe injury",
    "Dangerous organizations or individuals",
]
r3 = [
    "Fake health documents",
    "Drugs, alcohol or tobacco",
    "Firearms",
    "Weight loss products or cosmetic procedures",
    "Animals",
]
r4 = ["Me", "Someone I know", "Someone else"]
r5 = ["Health", "Politics", "Social issue", "Somthing else"]


# Qt user interface


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("InstaMachine")
        MainWindow.setEnabled(True)
        MainWindow.resize(809, 684)
        MainWindow.setMinimumSize(QtCore.QSize(0, 684))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(210, 210, 210))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(32, 35, 42))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(210, 210, 210))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(210, 210, 210))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(32, 35, 42))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(32, 35, 42))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(210, 210, 210, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(210, 210, 210))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(32, 35, 42))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(210, 210, 210))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(210, 210, 210))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(32, 35, 42))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(32, 35, 42))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(210, 210, 210, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(210, 210, 210))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(32, 35, 42))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(210, 210, 210))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(210, 210, 210))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(32, 35, 42))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(32, 35, 42))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(210, 210, 210, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.PlaceholderText, brush)
        MainWindow.setPalette(palette)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        MainWindow.setFont(font)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("background-color: rgb(32, 35, 42);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.centralwidget.setFont(font)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setStyleSheet(
            "QScrollBar:horizontal {\n"
            "    border: none;\n"
            "    background: rgb(52, 59, 72);\n"
            "    height: 14px;\n"
            "    margin: 0px 21px 0 21px;\n"
            "    border-radius: 0px;\n"
            "}\n"
            "QScrollBar::handle:horizontal {\n"
            "    background-color: rgb(159, 112, 151);\n"
            "    min-width: 25px;\n"
            "    border-radius: 4px\n"
            "}\n"
            "QScrollBar::add-line:horizontal {\n"
            "    border: none;\n"
            "    background: rgb(55, 63, 77);\n"
            "    width: 20px;\n"
            "    border-top-right-radius: 4px;\n"
            "    border-bottom-right-radius: 4px;\n"
            "    subcontrol-position: right;\n"
            "    subcontrol-origin: margin;\n"
            "}\n"
            "QScrollBar::sub-line:horizontal {\n"
            "    border: none;\n"
            "    background: rgb(55, 63, 77);\n"
            "    width: 20px;\n"
            "    border-top-left-radius: 4px;\n"
            "    border-bottom-left-radius: 4px;\n"
            "    subcontrol-position: left;\n"
            "    subcontrol-origin: margin;\n"
            "}\n"
            "QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal\n"
            "{\n"
            "     background: none;\n"
            "}\n"
            "QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal\n"
            "{\n"
            "     background: none;\n"
            "}\n"
            " QScrollBar:vertical {\n"
            "    border: none;\n"
            "    background: rgb(52, 59, 72);\n"
            "    width: 14px;\n"
            "    margin: 21px 0 21px 0;\n"
            "    border-radius: 0px;\n"
            " }\n"
            " QScrollBar::handle:vertical {    \n"
            "    background-color: rgb(159, 112, 151);\n"
            "    min-height: 25px;\n"
            "    border-radius: 4px\n"
            " }\n"
            " QScrollBar::add-line:vertical {\n"
            "     border: none;\n"
            "    background: rgb(55, 63, 77);\n"
            "     height: 20px;\n"
            "    border-bottom-left-radius: 4px;\n"
            "    border-bottom-right-radius: 4px;\n"
            "     subcontrol-position: bottom;\n"
            "     subcontrol-origin: margin;\n"
            " }\n"
            " QScrollBar::sub-line:vertical {\n"
            "    border: none;\n"
            "    background: rgb(55, 63, 77);\n"
            "     height: 20px;\n"
            "    border-top-left-radius: 4px;\n"
            "    border-top-right-radius: 4px;\n"
            "     subcontrol-position: top;\n"
            "     subcontrol-origin: margin;\n"
            " }\n"
            " QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
            "     background: none;\n"
            " }\n"
            "\n"
            " QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
            "     background: none;\n"
            " }\n"
            "QTabBar::tab {\n"
            "    color: rgb(107, 107, 107);\n"
            "    background-color: rgb(32, 35, 42);\n"
            "  padding: 5px;\n"
            "} \n"
            "QTabBar::tab:selected { \n"
            "    color: rgb(227, 223, 247);\n"
            "    background-color: rgb(41, 45, 56);\n"
            "}\n"
            "QTabWidget::pane {\n"
            "  top:-1px; \n"
            "  background: rgb(245, 245, 245);; \n"
            "} \n"
            "QCheckBox:indicator:unchecked\n"
            "{\n"
            "border : 2px solid rgb(152, 83, 120);\n"
            "}\n"
            "QCheckBox:indicator:checked\n"
            "{\n"
            "border : 2px solid rgb(152, 83, 120);\n"
            "    background-color: rgb(197, 44, 120);\n"
            "}\n"
            "QTableCornerButton::section { background-color:rgb(27, 29, 35); }"
        )
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(244, 244, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(44, 44, 54))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(249, 249, 249))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(121, 121, 121))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(162, 162, 162))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(244, 244, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(244, 244, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(44, 44, 54))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(44, 44, 54))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(249, 249, 249))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(244, 244, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(244, 244, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(44, 44, 54))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(249, 249, 249))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(121, 121, 121))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(162, 162, 162))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(244, 244, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(244, 244, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(44, 44, 54))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(44, 44, 54))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(249, 249, 249))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(244, 244, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(244, 244, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(44, 44, 54))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(249, 249, 249))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(121, 121, 121))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(162, 162, 162))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(244, 244, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(244, 244, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(44, 44, 54))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(44, 44, 54))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(243, 243, 243))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(244, 244, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.PlaceholderText, brush)
        self.tableWidget.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        self.tableWidget.setFont(font)
        self.tableWidget.setAutoFillBackground(False)
        self.tableWidget.setStyleSheet(
            "QTableWidget {\n"
            "    color: rgb(244, 244, 255);    \n"
            "    background-color: rgb(44, 44, 54);\n"
            "    padding: 10px;\n"
            "    border-radius: 5px;\n"
            "    gridline-color: rgb(86, 84, 100);\n"
            "    border-bottom: 1px solid rgb(44, 49, 60);\n"
            "}\n"
            "QTableWidget::item{\n"
            "    color: rgb(244, 244, 255);\n"
            "    border-color: rgb(44, 49, 60);\n"
            "    padding-left: 5px;\n"
            "    padding-right: 5px;\n"
            "    gridline-color: rgb(44, 49, 60);\n"
            "}\n"
            "QTableWidget::item:selected{\n"
            "    background-color: rgb(85, 170, 255);\n"
            "}\n"
            "QScrollBar:horizontal {\n"
            "    border: none;\n"
            "    background: rgb(52, 59, 72);\n"
            "    height: 14px;\n"
            "    margin: 0px 21px 0 21px;\n"
            "    border-radius: 0px;\n"
            "}\n"
            " QScrollBar:vertical {\n"
            "    border: none;\n"
            "    background: rgb(52, 59, 72);\n"
            "    width: 14px;\n"
            "    margin: 21px 0 21px 0;\n"
            "    border-radius: 0px;\n"
            " }\n"
            "QHeaderView::section{\n"
            "    color: rgb(244, 244, 255);\n"
            "    Background-color: rgb(39, 44, 54);\n"
            "    max-width: 30px;\n"
            "    border: 1px solid rgb(44, 49, 60);\n"
            "    border-style: none;\n"
            "    border-bottom: 1px solid rgb(44, 49, 60);\n"
            "    border-right: 1px solid rgb(44, 49, 60);\n"
            "}\n"
            "QTableWidget::horizontalHeader {    \n"
            "    background-color: rgb(81, 255, 0);\n"
            "}\n"
            "QHeaderView::section:horizontal\n"
            "{\n"
            "    border: 1px solid rgb(32, 34, 42);\n"
            "    background-color: rgb(27, 29, 35);\n"
            "    padding: 3px;\n"
            "\n"
            "}\n"
            "QHeaderView::section:vertical\n"
            "{\n"
            "    border: 1px solid rgb(44, 49, 60);\n"
            "}\n"
            "QTableCornerButton::section { background-color:rgb(27, 29, 35); }"
        )
        self.tableWidget.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.tableWidget.setGridStyle(QtCore.Qt.SolidLine)
        self.tableWidget.setRowCount(3)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(9)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 0, item)
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(200)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(False)
        self.tableWidget.verticalHeader().setVisible(True)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setDefaultSectionSize(200)
        self.gridLayout_3.addWidget(self.tableWidget, 0, 1, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 2, 3, 1)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setMinimumSize(QtCore.QSize(288, 625))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(244, 244, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(41, 45, 56))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(245, 245, 245))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(118, 118, 118))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(157, 157, 157))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(244, 244, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(244, 244, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(41, 45, 56))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(41, 45, 56))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(245, 245, 245))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(244, 244, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(244, 244, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(41, 45, 56))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(245, 245, 245))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(118, 118, 118))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(157, 157, 157))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(244, 244, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(244, 244, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(41, 45, 56))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(41, 45, 56))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(245, 245, 245))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(244, 244, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(244, 244, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(41, 45, 56))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(245, 245, 245))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(118, 118, 118))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(157, 157, 157))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(244, 244, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(244, 244, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(41, 45, 56))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(41, 45, 56))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(236, 236, 236))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(244, 244, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.PlaceholderText, brush)
        self.tabWidget.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setBold(False)
        font.setWeight(50)
        self.tabWidget.setFont(font)
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setStyleSheet(
            "color: rgb(244, 244, 255);\n"
            "background-color: rgb(41, 45, 56);\n"
            "border-radius: 5px;\n"
            ""
        )
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setElideMode(QtCore.Qt.ElideNone)
        self.tabWidget.setUsesScrollButtons(True)
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(False)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setStyleSheet("")
        self.tab_5.setObjectName("tab_5")
        self.gridLayout = QtWidgets.QGridLayout(self.tab_5)
        self.gridLayout.setObjectName("gridLayout")
        self.ocr = QtWidgets.QCheckBox(self.tab_5)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ocr.sizePolicy().hasHeightForWidth())
        self.ocr.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        self.ocr.setFont(font)
        self.ocr.setAutoFillBackground(False)
        self.ocr.setStyleSheet("")
        self.ocr.setObjectName("ocr")
        self.gridLayout.addWidget(self.ocr, 21, 0, 1, 1)
        self.reason2 = QtWidgets.QComboBox(self.tab_5)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.reason2.sizePolicy().hasHeightForWidth())
        self.reason2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        self.reason2.setFont(font)
        self.reason2.setStyleSheet(
            "QComboBox{\n"
            "    background-color: rgb(27, 29, 35);\n"
            "    border-radius: 5px;\n"
            "    border: 2px solid rgb(91, 101, 124);\n"
            "    padding: 5px;\n"
            "    padding-left: 10px;\n"
            "}\n"
            "QComboBox:hover{\n"
            "    border: 2px solid rgb(64, 71, 88);\n"
            "}\n"
            "QComboBox QAbstractItemView {\n"
            "    color: rgb(85, 170, 255);    \n"
            "    background-color: rgb(27, 29, 35);\n"
            "    padding: 10px;\n"
            "    selection-background-color: rgb(39, 44, 54);\n"
            "}"
        )
        self.reason2.setObjectName("reason2")
        self.gridLayout.addWidget(self.reason2, 31, 1, 1, 3)
        self.comment = QtWidgets.QCheckBox(self.tab_5)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comment.sizePolicy().hasHeightForWidth())
        self.comment.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setBold(False)
        font.setWeight(50)
        self.comment.setFont(font)
        self.comment.setAutoFillBackground(False)
        self.comment.setStyleSheet("")
        self.comment.setObjectName("comment")
        self.gridLayout.addWidget(self.comment, 33, 0, 1, 1)
        self.report = QtWidgets.QCheckBox(self.tab_5)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.report.sizePolicy().hasHeightForWidth())
        self.report.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setBold(False)
        font.setWeight(50)
        self.report.setFont(font)
        self.report.setAutoFillBackground(False)
        self.report.setStyleSheet("")
        self.report.setObjectName("report")
        self.gridLayout.addWidget(self.report, 30, 0, 1, 1)
        self.likesmin = QtWidgets.QCheckBox(self.tab_5)
        self.likesmin.setObjectName("likesmin")
        self.gridLayout.addWidget(self.likesmin, 23, 0, 1, 1)
        self.followcombo = QtWidgets.QComboBox(self.tab_5)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.followcombo.sizePolicy().hasHeightForWidth())
        self.followcombo.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        self.followcombo.setFont(font)
        self.followcombo.setStyleSheet(
            "QComboBox{\n"
            "    background-color: rgb(27, 29, 35);\n"
            "    border-radius: 5px;\n"
            "    border: 2px solid rgb(91, 101, 124);\n"
            "    padding: 5px;\n"
            "    padding-left: 10px;\n"
            "}\n"
            "QComboBox:hover{\n"
            "    border: 2px solid rgb(64, 71, 88);\n"
            "}\n"
            "QComboBox QAbstractItemView {\n"
            "    color: rgb(85, 170, 255);    \n"
            "    background-color: rgb(27, 29, 35);\n"
            "    padding: 10px;\n"
            "    selection-background-color: rgb(39, 44, 54);\n"
            "}"
        )
        self.followcombo.setObjectName("followcombo")
        self.followcombo.addItem("")
        self.followcombo.addItem("")
        self.followcombo.addItem("")
        self.gridLayout.addWidget(self.followcombo, 29, 1, 1, 1)

        self.set_like = QtWidgets.QLabel(self.tab_5)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.set_like.sizePolicy().hasHeightForWidth())
        self.set_like.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setBold(False)
        font.setWeight(50)
        self.set_like.setFont(font)
        self.set_like.setAutoFillBackground(False)
        self.set_like.setStyleSheet("")
        self.set_like.setObjectName("set_like")
        self.gridLayout.addWidget(self.set_like, 28, 0, 1, 1)
        self.overwrite = QtWidgets.QCheckBox(self.tab_5)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.overwrite.sizePolicy().hasHeightForWidth())
        self.overwrite.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        self.overwrite.setFont(font)
        self.overwrite.setAutoFillBackground(False)
        self.overwrite.setStyleSheet("")
        self.overwrite.setObjectName("overwrite")
        self.gridLayout.addWidget(self.overwrite, 3, 1, 1, 1)
        self.likecombo = QtWidgets.QComboBox(self.tab_5)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.likecombo.sizePolicy().hasHeightForWidth())
        self.likecombo.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        self.likecombo.setFont(font)
        self.likecombo.setStyleSheet(
            "QComboBox{\n"
            "    background-color: rgb(27, 29, 35);\n"
            "    border-radius: 5px;\n"
            "    border: 2px solid rgb(91, 101, 124);\n"
            "    padding: 5px;\n"
            "    padding-left: 10px;\n"
            "}\n"
            "QComboBox:hover{\n"
            "    border: 2px solid rgb(64, 71, 88);\n"
            "}\n"
            "QComboBox QAbstractItemView {\n"
            "    color: rgb(85, 170, 255);    \n"
            "    background-color: rgb(27, 29, 35);\n"
            "    padding: 10px;\n"
            "    selection-background-color: rgb(39, 44, 54);\n"
            "}"
        )
        self.likecombo.setObjectName("likecombo")
        self.likecombo.addItem("")
        self.likecombo.addItem("")
        self.likecombo.addItem("")
        self.gridLayout.addWidget(self.likecombo, 28, 1, 1, 1)
        self.datelimit = QtWidgets.QCheckBox(self.tab_5)
        self.datelimit.setObjectName("datelimit")
        self.gridLayout.addWidget(self.datelimit, 24, 0, 1, 1)
        self.findinput = QtWidgets.QLineEdit(self.tab_5)
        self.findinput.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.findinput.sizePolicy().hasHeightForWidth())
        self.findinput.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        self.findinput.setFont(font)
        self.findinput.setStyleSheet(
            "QLineEdit {\n"
            "    background-color: rgb(27, 29, 35);\n"
            "    border-radius: 5px;\n"
            "    border: 2px solid rgb(91, 101, 124);\n"
            "    padding-left: 10px;\n"
            "}\n"
            "QLineEdit:hover {\n"
            "    border: 2px solid rgb(64, 71, 88);\n"
            "}\n"
            "QLineEdit:focus {\n"
            "    border: 2px solid rgb(91, 101, 124);\n"
            "}\n"
            "QLineEdit:disabled {\n"
            "    border-color: rgb(58, 63, 75);\n"
            "}\n"
            ""
        )
        self.findinput.setObjectName("findinput")
        self.gridLayout.addWidget(self.findinput, 22, 1, 1, 3)
        self.datelimit_input = QtWidgets.QDateEdit(self.tab_5)
        self.datelimit_input.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.datelimit_input.sizePolicy().hasHeightForWidth()
        )
        self.datelimit_input.setSizePolicy(sizePolicy)
        self.datelimit_input.setStyleSheet(
            "QDateEdit{\n"
            "    background-color: rgb(27, 29, 35);\n"
            "    border-radius: 5px;\n"
            "    border: 2px solid rgb(91, 101, 124);\n"
            "    padding: 5px;\n"
            "    padding-left: 10px;\n"
            "}\n"
            "QDateEdit:hover{\n"
            "    border: 2px solid rgb(64, 71, 88);\n"
            "}\n"
            "QDateEdit QAbstractItemView {\n"
            "    color: rgb(85, 170, 255);    \n"
            "    background-color: rgb(27, 29, 35);\n"
            "    padding: 10px;\n"
            "    selection-background-color: rgb(39, 44, 54);\n"
            "}\n"
            "QDateEdit:disabled {\n"
            "    color: rgb(70, 70, 70);\n"
            "    border-color: rgb(58, 63, 75);\n"
            "}\n"
            ""
        )
        self.datelimit_input.setObjectName("datelimit_input")
        self.gridLayout.addWidget(self.datelimit_input, 24, 1, 1, 1)
        self.aiselect = QtWidgets.QPushButton(
            self.tab_5, clicked=lambda: self.image_dialog()
        )
        self.aiselect.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.aiselect.sizePolicy().hasHeightForWidth())
        self.aiselect.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        self.aiselect.setFont(font)
        self.aiselect.setStyleSheet(
            "QPushButton {\n"
            "    color: rgb(27, 29, 35);\n"
            "    border: 2px solid  rgb(141, 127, 157);\n"
            "    background-color: rgb(157, 156, 179);\n"
            "    border-radius: 6px;    \n"
            "\n"
            "}\n"
            "QPushButton:hover {\n"
            "    background-color: rgb(188, 174, 206);\n"
            "    border: 2px solid rgb(61, 70, 86);\n"
            "}\n"
            "QPushButton:pressed {    \n"
            "    background-color: rgb(35, 40, 49);\n"
            "    border: 2px solid rgb(43, 50, 61);\n"
            "}\n"
            "QPushButton:disabled {\n"
            "    color: rgb(117, 117, 117);\n"
            "    background-color: rgb(51, 52, 68);\n"
            "    border: 2px solid  rgb(94, 90, 99)\n"
            "}\n"
            ""
        )
        self.aiselect.setObjectName("aiselect")
        self.gridLayout.addWidget(self.aiselect, 20, 1, 1, 1)
        self.randomcm = QtWidgets.QCheckBox(
            self.tab_5, clicked=lambda: self.check_select()
        )
        self.randomcm.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.randomcm.sizePolicy().hasHeightForWidth())
        self.randomcm.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        self.randomcm.setFont(font)
        self.randomcm.setAutoFillBackground(False)
        self.randomcm.setStyleSheet("")
        self.randomcm.setObjectName("randomcm")
        self.gridLayout.addWidget(self.randomcm, 33, 1, 1, 1)
        self.aicombo = QtWidgets.QComboBox(self.tab_5)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.aicombo.sizePolicy().hasHeightForWidth())
        self.aicombo.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        self.aicombo.setFont(font)
        self.aicombo.setStyleSheet(
            "QComboBox{\n"
            "    background-color: rgb(27, 29, 35);\n"
            "    border-radius: 5px;\n"
            "    border: 2px solid rgb(91, 101, 124);\n"
            "    padding: 5px;\n"
            "    padding-left: 10px;\n"
            "}\n"
            "QComboBox:hover{\n"
            "    border: 2px solid rgb(64, 71, 88);\n"
            "}\n"
            "QComboBox QAbstractItemView {\n"
            "    color: rgb(85, 170, 255);    \n"
            "    background-color: rgb(27, 29, 35);\n"
            "    padding: 10px;\n"
            "    selection-background-color: rgb(39, 44, 54);\n"
            "}"
        )
        self.aicombo.setObjectName("aicombo")
        self.aicombo.addItem("")
        self.aicombo.addItem("")
        self.gridLayout.addWidget(self.aicombo, 20, 2, 1, 2)
        self.find = QtWidgets.QCheckBox(self.tab_5)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.find.sizePolicy().hasHeightForWidth())
        self.find.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setBold(False)
        font.setWeight(50)
        self.find.setFont(font)
        self.find.setAutoFillBackground(False)
        self.find.setStyleSheet("")
        self.find.setObjectName("find")
        self.gridLayout.addWidget(self.find, 22, 0, 1, 1)
        self.resume = QtWidgets.QCheckBox(self.tab_5)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.resume.sizePolicy().hasHeightForWidth())
        self.resume.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setBold(False)
        font.setWeight(50)
        self.resume.setFont(font)
        self.resume.setAutoFillBackground(False)
        self.resume.setStyleSheet("")
        self.resume.setTristate(False)
        self.resume.setObjectName("resume")
        self.gridLayout.addWidget(self.resume, 3, 0, 1, 1)
        self.scroll_number = QtWidgets.QSpinBox(self.tab_5)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.scroll_number.sizePolicy().hasHeightForWidth()
        )
        self.scroll_number.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        self.scroll_number.setFont(font)
        self.scroll_number.setStyleSheet(
            "QSpinBox{\n"
            "    background-color: rgb(27, 29, 35);\n"
            "    border-radius: 5px;\n"
            "    border: 2px solid rgb(91, 101, 124);\n"
            "    padding: 5px;\n"
            "    padding-left: 10px;\n"
            "}\n"
            "QSpinBox:hover{\n"
            "    border: 2px solid rgb(64, 71, 88);\n"
            "}\n"
            "QSpinBox QAbstractItemView {\n"
            "    color: rgb(85, 170, 255);    \n"
            "    background-color: rgb(27, 29, 35);\n"
            "    padding: 10px;\n"
            "    selection-background-color: rgb(39, 44, 54);\n"
            "}"
        )
        self.scroll_number.setWrapping(False)
        self.scroll_number.setFrame(True)
        self.scroll_number.setMinimum(1)
        self.scroll_number.setMaximum(1000)
        self.scroll_number.setObjectName("scroll_number")
        self.gridLayout.addWidget(self.scroll_number, 3, 3, 1, 1)
        self.set_follow = QtWidgets.QLabel(self.tab_5)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.set_follow.sizePolicy().hasHeightForWidth())
        self.set_follow.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setBold(False)
        font.setWeight(50)
        self.set_follow.setFont(font)
        self.set_follow.setAutoFillBackground(False)
        self.set_follow.setStyleSheet("")
        self.set_follow.setObjectName("set_follow")
        self.gridLayout.addWidget(self.set_follow, 29, 0, 1, 1)
        self.ai = QtWidgets.QCheckBox(self.tab_5)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ai.sizePolicy().hasHeightForWidth())
        self.ai.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setBold(False)
        font.setWeight(50)
        self.ai.setFont(font)
        self.ai.setAutoFillBackground(False)
        self.ai.setStyleSheet("")
        self.ai.setObjectName("ai")
        self.gridLayout.addWidget(self.ai, 20, 0, 1, 1)
        self.screenshot = QtWidgets.QCheckBox(self.tab_5)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.screenshot.sizePolicy().hasHeightForWidth())
        self.screenshot.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setBold(False)
        font.setWeight(50)
        self.screenshot.setFont(font)
        self.screenshot.setAutoFillBackground(False)
        self.screenshot.setStyleSheet("")
        self.screenshot.setObjectName("screenshot")
        self.gridLayout.addWidget(self.screenshot, 32, 0, 1, 1)
        self.ocrlang = QtWidgets.QComboBox(self.tab_5)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ocrlang.sizePolicy().hasHeightForWidth())
        self.ocrlang.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        self.ocrlang.setFont(font)
        self.ocrlang.setStyleSheet(
            "QComboBox{\n"
            "    background-color: rgb(27, 29, 35);\n"
            "    border-radius: 5px;\n"
            "    border: 2px solid rgb(91, 101, 124);\n"
            "    padding: 5px;\n"
            "    padding-left: 10px;\n"
            "}\n"
            "QComboBox:hover{\n"
            "    border: 2px solid rgb(64, 71, 88);\n"
            "}\n"
            "QComboBox QAbstractItemView {\n"
            "    color: rgb(85, 170, 255);    \n"
            "    background-color: rgb(27, 29, 35);\n"
            "    padding: 10px;\n"
            "    selection-background-color: rgb(39, 44, 54);\n"
            "}"
        )
        self.ocrlang.setObjectName("ocrlang")
        self.ocrlang.addItem("")
        self.ocrlang.addItem("")
        self.gridLayout.addWidget(self.ocrlang, 21, 2, 1, 2)
        self.price = QtWidgets.QCheckBox(self.tab_5)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.price.sizePolicy().hasHeightForWidth())
        self.price.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setBold(False)
        font.setWeight(50)
        self.price.setFont(font)
        self.price.setAutoFillBackground(False)
        self.price.setStyleSheet("")
        self.price.setObjectName("price")
        self.gridLayout.addWidget(self.price, 24, 2, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(self.tab_5)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.radiotag = QtWidgets.QRadioButton(self.groupBox)
        self.radiotag.setGeometry(QtCore.QRect(0, 0, 37, 16))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.radiotag.sizePolicy().hasHeightForWidth())
        self.radiotag.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        self.radiotag.setFont(font)
        self.radiotag.setObjectName("radiotag")
        self.radiolocation = QtWidgets.QRadioButton(self.groupBox)
        self.radiolocation.setGeometry(QtCore.QRect(70, 0, 71, 16))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.radiolocation.sizePolicy().hasHeightForWidth()
        )
        self.radiolocation.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        self.radiolocation.setFont(font)
        self.radiolocation.setObjectName("radiolocation")
        self.radioperson = QtWidgets.QRadioButton(self.groupBox)
        self.radioperson.setGeometry(QtCore.QRect(150, 0, 61, 16))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.radioperson.sizePolicy().hasHeightForWidth())
        self.radioperson.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        self.radioperson.setFont(font)
        self.radioperson.setObjectName("radioperson")
        self.radioButton_4 = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_4.setGeometry(QtCore.QRect(230, 0, 81, 16))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.radioButton_4.sizePolicy().hasHeightForWidth()
        )
        self.radioButton_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        self.radioButton_4.setFont(font)
        self.radioButton_4.setObjectName("radioButton_4")

        self.gridLayout.addWidget(self.groupBox, 2, 0, 1, 4)
        self.go = QtWidgets.QPushButton(
            self.tab_5, clicked=lambda: threading.Thread(target=self.letsgo).start()
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.go.sizePolicy().hasHeightForWidth())
        self.go.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.go.setFont(font)
        self.go.setStyleSheet(
            "QPushButton {\n"
            "    color: rgb(247, 244, 255);\n"
            "    border: 2px solid rgb(141, 127, 157);\n"
            "    border-radius: 4px;    \n"
            "    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.994, y2:1, stop:0 rgba(86, 82, 189, 255), stop:1 rgba(207, 40, 114, 255));\n"
            "}\n"
            "QPushButton:hover {\n"
            "    background-color: rgb(166, 54, 140);\n"
            "    border: 2px solid rgb(61, 70, 86);\n"
            "}\n"
            "QPushButton:pressed {    \n"
            "    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(115, 110, 255, 255), stop:1 rgba(179, 55, 246, 255));\n"
            "    border: 2px solid rgb(43, 50, 61);\n"
            "}"
        )
        self.go.setObjectName("go")
        self.gridLayout.addWidget(self.go, 1, 0, 1, 1)
        self.reason = QtWidgets.QComboBox(self.tab_5)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.reason.sizePolicy().hasHeightForWidth())
        self.reason.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        self.reason.setFont(font)
        self.reason.setStyleSheet(
            "QComboBox{\n"
            "    background-color: rgb(27, 29, 35);\n"
            "    border-radius: 5px;\n"
            "    border: 2px solid rgb(91, 101, 124);\n"
            "    padding: 5px;\n"
            "    padding-left: 10px;\n"
            "}\n"
            "QComboBox:hover{\n"
            "    border: 2px solid rgb(64, 71, 88);\n"
            "}\n"
            "QComboBox QAbstractItemView {\n"
            "    color: rgb(85, 170, 255);    \n"
            "    background-color: rgb(27, 29, 35);\n"
            "    padding: 10px;\n"
            "    selection-background-color: rgb(39, 44, 54);\n"
            "}"
        )
        self.reason.setObjectName("reason")
        self.reason.addItem("")
        self.reason.addItem("")
        self.reason.addItem("")
        self.reason.addItem("")
        self.reason.addItem("")
        self.reason.addItem("")
        self.reason.addItem("")
        self.reason.addItem("")
        self.reason.addItem("")
        self.reason.addItem("")
        self.reason.addItem("")
        self.reason.addItem("")
        self.reason.addItem("")
        self.gridLayout.addWidget(self.reason, 30, 1, 1, 3)
        self.ocr_input = QtWidgets.QLineEdit(self.tab_5)
        self.ocr_input.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ocr_input.sizePolicy().hasHeightForWidth())
        self.ocr_input.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        self.ocr_input.setFont(font)
        self.ocr_input.setStyleSheet(
            "QLineEdit {\n"
            "    background-color: rgb(27, 29, 35);\n"
            "    border-radius: 5px;\n"
            "    border: 2px solid rgb(91, 101, 124);\n"
            "    padding-left: 10px;\n"
            "}\n"
            "QLineEdit:hover {\n"
            "    border: 2px solid rgb(64, 71, 88);\n"
            "}\n"
            "QLineEdit:focus {\n"
            "    border: 2px solid rgb(91, 101, 124);\n"
            "}\n"
            "QLineEdit:disabled {\n"
            "    border-color: rgb(58, 63, 75);\n"
            "}\n"
            ""
        )
        self.ocr_input.setObjectName("ocr_input")
        self.gridLayout.addWidget(self.ocr_input, 21, 1, 1, 1)
        self.scroll_limit = QtWidgets.QLabel(self.tab_5)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scroll_limit.sizePolicy().hasHeightForWidth())
        self.scroll_limit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setBold(False)
        font.setWeight(50)
        self.scroll_limit.setFont(font)
        self.scroll_limit.setAutoFillBackground(False)
        self.scroll_limit.setStyleSheet("")
        self.scroll_limit.setObjectName("scroll_limit")
        self.gridLayout.addWidget(self.scroll_limit, 3, 2, 1, 1)
        self.selecttext = QtWidgets.QPushButton(
            self.tab_5, clicked=lambda: self.text_dialog()
        )
        self.selecttext.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.selecttext.sizePolicy().hasHeightForWidth())
        self.selecttext.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        self.selecttext.setFont(font)
        self.selecttext.setStyleSheet(
            "QPushButton {\n"
            "    color: rgb(27, 29, 35);\n"
            "    border: 2px solid  rgb(141, 127, 157);\n"
            "    background-color: rgb(157, 156, 179);\n"
            "    border-radius: 6px;    \n"
            "\n"
            "}\n"
            "QPushButton:hover {\n"
            "    background-color: rgb(188, 174, 206);\n"
            "    border: 2px solid rgb(61, 70, 86);\n"
            "}\n"
            "QPushButton:pressed {    \n"
            "    background-color: rgb(35, 40, 49);\n"
            "    border: 2px solid rgb(43, 50, 61);\n"
            "}\n"
            "QPushButton:disabled {\n"
            "    color: rgb(117, 117, 117);\n"
            "    background-color: rgb(51, 52, 68);\n"
            "    border: 2px solid  rgb(94, 90, 99)\n"
            "}\n"
            ""
        )
        self.selecttext.setObjectName("selecttext")
        self.gridLayout.addWidget(self.selecttext, 33, 2, 1, 2)
        self.likesmin_input = QtWidgets.QSpinBox(self.tab_5)
        self.likesmin_input.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.likesmin_input.sizePolicy().hasHeightForWidth()
        )
        self.likesmin_input.setSizePolicy(sizePolicy)
        self.likesmin_input.setStyleSheet(
            "QSpinBox{\n"
            "    background-color: rgb(27, 29, 35);\n"
            "    border-radius: 5px;\n"
            "    border: 2px solid rgb(91, 101, 124);\n"
            "    padding: 5px;\n"
            "    padding-left: 10px;\n"
            "}\n"
            "QSpinBox:hover{\n"
            "    border: 2px solid rgb(64, 71, 88);\n"
            "}\n"
            "QSpinBox QAbstractItemView {\n"
            "    color: rgb(85, 170, 255);    \n"
            "    background-color: rgb(27, 29, 35);\n"
            "    padding: 10px;\n"
            "    selection-background-color: rgb(39, 44, 54);\n"
            "}\n"
            "QSpinBox:disabled {\n"
            "    color: rgb(70, 70, 70);\n"
            "    border-color: rgb(58, 63, 75);\n"
            "}\n"
            ""
        )
        self.likesmin_input.setObjectName("likesmin_input")
        self.gridLayout.addWidget(self.likesmin_input, 23, 1, 1, 1)
        self.bulkimage = QtWidgets.QCheckBox(self.tab_5)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bulkimage.sizePolicy().hasHeightForWidth())
        self.bulkimage.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setBold(False)
        font.setWeight(50)
        self.bulkimage.setFont(font)
        self.bulkimage.setAutoFillBackground(False)
        self.bulkimage.setStyleSheet("")
        self.bulkimage.setObjectName("bulkimage")
        self.gridLayout.addWidget(self.bulkimage, 32, 1, 1, 3)
        self.label_2 = QtWidgets.QLabel(self.tab_5)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setUnderline(True)
        font.setFamily("Segoe UI Black")
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(189, 133, 180);")
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 19, 0, 1, 4)
        self.label = QtWidgets.QLabel(self.tab_5)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Black")
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(189, 133, 180); ")
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 27, 0, 1, 4)
        self.search = QtWidgets.QLineEdit(self.tab_5)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.search.sizePolicy().hasHeightForWidth())
        self.search.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        self.search.setFont(font)
        self.search.setStyleSheet(
            "QLineEdit {\n"
            "    background-color: rgb(27, 29, 35);\n"
            "    border-radius: 5px;\n"
            "    border: 2px solid  rgb(141, 127, 157);\n"
            "    padding-left: 10px;\n"
            "}\n"
            "QLineEdit:hover {\n"
            "    border: 2px solid  rgb(180, 162, 200);\n"
            "}\n"
            "QLineEdit:focus {\n"
            "    border: 2px solid rgb(224, 215, 245);;\n"
            "}"
        )
        self.search.setObjectName("search")
        self.gridLayout.addWidget(self.search, 1, 1, 1, 3)
        self.phone = QtWidgets.QCheckBox(self.tab_5)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.phone.sizePolicy().hasHeightForWidth())
        self.phone.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setBold(False)
        font.setWeight(50)
        self.phone.setFont(font)
        self.phone.setAutoFillBackground(False)
        self.phone.setStyleSheet("")
        self.phone.setObjectName("phone")
        self.gridLayout.addWidget(self.phone, 23, 2, 1, 2)
        self.commentbox = QtWidgets.QTextEdit(self.tab_5)
        self.commentbox.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Ignored
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.commentbox.sizePolicy().hasHeightForWidth())
        self.commentbox.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        self.commentbox.setFont(font)
        self.commentbox.setStyleSheet(
            "QTextEdit {\n"
            "    background-color: rgb(27, 29, 35);\n"
            "    border-radius: 5px;\n"
            "    border: 2px solid rgb(91, 101, 124);\n"
            "    padding: 10px;\n"
            "}\n"
            "QTextEdit:hover {\n"
            "    border: 2px solid rgb(64, 71, 88);\n"
            "}\n"
            "QTextEdit:focus {\n"
            "    border: 2px solid rgb(91, 101, 124);\n"
            "}\n"
            "QTextEdit:disabled {\n"
            "    border-color: rgb(58, 63, 75);\n"
            "}\n"
            ""
        )
        self.commentbox.setObjectName("commentbox")
        self.gridLayout.addWidget(self.commentbox, 34, 0, 2, 4)
        self.tabWidget.addTab(self.tab_5, "")
        self.tab_6 = QtWidgets.QWidget()
        self.tab_6.setObjectName("tab_6")
        self.switchspin = QtWidgets.QSpinBox(self.tab_6)
        self.switchspin.setEnabled(False)
        self.switchspin.setGeometry(QtCore.QRect(82, 470, 81, 31))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.switchspin.sizePolicy().hasHeightForWidth())
        self.switchspin.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        self.switchspin.setFont(font)
        self.switchspin.setStyleSheet(
            "QSpinBox{\n"
            "    background-color: rgb(27, 29, 35);\n"
            "    border-radius: 5px;\n"
            "    border: 2px solid rgb(91, 101, 124);\n"
            "    padding: 5px;\n"
            "    padding-left: 10px;\n"
            "}\n"
            "QSpinBox:hover{\n"
            "    border: 2px solid rgb(64, 71, 88);\n"
            "}\n"
            "QSpinBox QAbstractItemView {\n"
            "    color: rgb(85, 170, 255);    \n"
            "    background-color: rgb(27, 29, 35);\n"
            "    padding: 10px;\n"
            "    selection-background-color: rgb(39, 44, 54);\n"
            "}\n"
            "QSpinBox:disabled {\n"
            "    color: rgb(70, 70, 70);\n"
            "    border-color: rgb(58, 63, 75);\n"
            "}\n"
            ""
        )
        self.switchspin.setMinimum(1)
        self.switchspin.setMaximum(1000)
        self.switchspin.setObjectName("switchspin")
        self.remember = QtWidgets.QCheckBox(self.tab_6)
        self.remember.setGeometry(QtCore.QRect(10, 90, 81, 31))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.remember.sizePolicy().hasHeightForWidth())
        self.remember.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        self.remember.setFont(font)
        self.remember.setTristate(False)
        self.remember.setObjectName("remember")
        self.switchevery = QtWidgets.QLabel(self.tab_6)
        self.switchevery.setGeometry(QtCore.QRect(10, 470, 61, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        self.switchevery.setFont(font)
        self.switchevery.setObjectName("switchevery")
        self.importlist = QtWidgets.QPushButton(
            self.tab_6, clicked=lambda: self.import_list()
        )
        self.importlist.setGeometry(QtCore.QRect(10, 400, 81, 31))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.importlist.sizePolicy().hasHeightForWidth())
        self.importlist.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setBold(False)
        font.setWeight(50)
        self.importlist.setFont(font)
        self.importlist.setStyleSheet(
            "QPushButton {\n"
            "    color: rgb(27, 29, 35);\n"
            "    border: 2px solid  rgb(141, 127, 157);\n"
            "    background-color: rgb(157, 156, 179);\n"
            "    border-radius: 6px;    \n"
            "\n"
            "}\n"
            "QPushButton:hover {\n"
            "    background-color: rgb(188, 174, 206);\n"
            "    border: 2px solid rgb(61, 70, 86);\n"
            "}\n"
            "QPushButton:pressed {    \n"
            "    background-color: rgb(35, 40, 49);\n"
            "    border: 2px solid rgb(43, 50, 61);\n"
            "}\n"
            "QPushButton:disabled {\n"
            "    color: rgb(117, 117, 117);\n"
            "    background-color: rgb(51, 52, 68);\n"
            "}"
        )
        self.importlist.setObjectName("importlist")
        self.pass_input = QtWidgets.QLineEdit(self.tab_6)
        self.pass_input.setGeometry(QtCore.QRect(70, 50, 241, 31))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pass_input.sizePolicy().hasHeightForWidth())
        self.pass_input.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        self.pass_input.setFont(font)
        self.pass_input.setStyleSheet(
            "QLineEdit {\n"
            "    background-color: rgb(27, 29, 35);\n"
            "    border-radius: 5px;\n"
            "    border: 2px solid rgb(91, 101, 124);\n"
            "    padding-left: 10px;\n"
            "}\n"
            "QLineEdit:hover {\n"
            "    border: 2px solid rgb(64, 71, 88);\n"
            "}\n"
            "QLineEdit:focus {\n"
            "    border: 2px solid rgb(91, 101, 124);\n"
            "}\n"
            "QLineEdit:disabled {\n"
            "    border-color: rgb(58, 63, 75);\n"
            "}\n"
            ""
        )
        self.pass_input.setObjectName("pass_input")
        self.min = QtWidgets.QLabel(self.tab_6)
        self.min.setGeometry(QtCore.QRect(170, 470, 21, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        self.min.setFont(font)
        self.min.setObjectName("min")
        self.user_input = QtWidgets.QLineEdit(self.tab_6)
        self.user_input.setGeometry(QtCore.QRect(70, 10, 241, 31))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.user_input.sizePolicy().hasHeightForWidth())
        self.user_input.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        self.user_input.setFont(font)
        self.user_input.setStyleSheet(
            "QLineEdit {\n"
            "    background-color: rgb(27, 29, 35);\n"
            "    border-radius: 5px;\n"
            "    border: 2px solid rgb(91, 101, 124);\n"
            "    padding-left: 10px;\n"
            "}\n"
            "QLineEdit:hover {\n"
            "    border: 2px solid rgb(64, 71, 88);\n"
            "}\n"
            "QLineEdit:focus {\n"
            "    border: 2px solid rgb(91, 101, 124);\n"
            "}\n"
            "QLineEdit:disabled {\n"
            "    border-color: rgb(58, 63, 75);\n"
            "}\n"
            ""
        )
        self.user_input.setObjectName("user_input")
        self.add_account = QtWidgets.QPushButton(
            self.tab_6, clicked=lambda: self.list_add_acc()
        )
        self.add_account.setGeometry(QtCore.QRect(230, 90, 81, 31))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.add_account.sizePolicy().hasHeightForWidth())
        self.add_account.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        self.add_account.setFont(font)
        self.add_account.setStyleSheet(
            "QPushButton {\n"
            "    color: rgb(27, 29, 35);\n"
            "    border: 2px solid  rgb(141, 127, 157);\n"
            "    background-color: rgb(157, 156, 179);\n"
            "    border-radius: 6px;    \n"
            "\n"
            "}\n"
            "QPushButton:hover {\n"
            "    background-color: rgb(188, 174, 206);\n"
            "    border: 2px solid rgb(61, 70, 86);\n"
            "}\n"
            "QPushButton:pressed {    \n"
            "    background-color: rgb(35, 40, 49);\n"
            "    border: 2px solid rgb(43, 50, 61);\n"
            "}\n"
            "QPushButton:disabled {\n"
            "    color: rgb(117, 117, 117);\n"
            "    background-color: rgb(51, 52, 68);\n"
            "}"
        )
        self.add_account.setObjectName("add_account")
        self.remove_acc = QtWidgets.QPushButton(
            self.tab_6, clicked=lambda: self.removeacc()
        )
        self.remove_acc.setGeometry(QtCore.QRect(120, 400, 81, 31))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.remove_acc.sizePolicy().hasHeightForWidth())
        self.remove_acc.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        self.remove_acc.setFont(font)
        self.remove_acc.setStyleSheet(
            "QPushButton {\n"
            "    color: rgb(27, 29, 35);\n"
            "    border: 2px solid  rgb(141, 127, 157);\n"
            "    background-color: rgb(157, 156, 179);\n"
            "    border-radius: 6px;    \n"
            "\n"
            "}\n"
            "QPushButton:hover {\n"
            "    background-color: rgb(188, 174, 206);\n"
            "    border: 2px solid rgb(61, 70, 86);\n"
            "}\n"
            "QPushButton:pressed {    \n"
            "    background-color: rgb(35, 40, 49);\n"
            "    border: 2px solid rgb(43, 50, 61);\n"
            "}\n"
            "QPushButton:disabled {\n"
            "    color: rgb(117, 117, 117);\n"
            "    background-color: rgb(51, 52, 68);\n"
            "}"
        )
        self.remove_acc.setObjectName("remove_acc")
        self.addswitch = QtWidgets.QCheckBox(self.tab_6)
        self.addswitch.setGeometry(QtCore.QRect(10, 440, 81, 31))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addswitch.sizePolicy().hasHeightForWidth())
        self.addswitch.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        self.addswitch.setFont(font)
        self.addswitch.setObjectName("addswitch")
        self.password = QtWidgets.QLabel(self.tab_6)
        self.password.setGeometry(QtCore.QRect(10, 50, 48, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        self.password.setFont(font)
        self.password.setObjectName("password")
        self.select_acc = QtWidgets.QPushButton(
            self.tab_6, clicked=lambda: self.acc_select()
        )
        self.select_acc.setGeometry(QtCore.QRect(230, 400, 81, 31))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.select_acc.sizePolicy().hasHeightForWidth())
        self.select_acc.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        self.select_acc.setFont(font)
        self.select_acc.setStyleSheet(
            "QPushButton {\n"
            "    color: rgb(27, 29, 35);\n"
            "    border: 2px solid  rgb(141, 127, 157);\n"
            "    background-color: rgb(157, 156, 179);\n"
            "    border-radius: 6px;    \n"
            "\n"
            "}\n"
            "QPushButton:hover {\n"
            "    background-color: rgb(188, 174, 206);\n"
            "    border: 2px solid rgb(61, 70, 86);\n"
            "}\n"
            "QPushButton:pressed {    \n"
            "    background-color: rgb(35, 40, 49);\n"
            "    border: 2px solid rgb(43, 50, 61);\n"
            "}\n"
            "QPushButton:disabled {\n"
            "    color: rgb(117, 117, 117);\n"
            "    background-color: rgb(51, 52, 68);\n"
            "}"
        )
        self.select_acc.setObjectName("select_acc")
        self.acc_list = QtWidgets.QListWidget(self.tab_6)
        self.acc_list.setGeometry(QtCore.QRect(10, 130, 301, 261))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.acc_list.sizePolicy().hasHeightForWidth())
        self.acc_list.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        self.acc_list.setFont(font)
        self.acc_list.setStyleSheet(
            "QListWidget{\n"
            "    background-color: rgb(27, 29, 35);\n"
            "    border-radius: 5px;\n"
            "    border: 2px solid rgb(91, 101, 124);\n"
            "    padding: 5px;\n"
            "    padding-left: 10px;\n"
            "}\n"
            "QListWidget:hover{\n"
            "    border: 2px solid rgb(64, 71, 88);\n"
            "}\n"
            "QListWidget QAbstractItemView {\n"
            "    color: rgb(85, 170, 255);    \n"
            "    background-color: rgb(27, 29, 35);\n"
            "    padding: 10px;\n"
            "    selection-background-color: rgb(39, 44, 54);\n"
            "}"
        )
        self.acc_list.setObjectName("acc_list")
        self.usernam = QtWidgets.QLabel(self.tab_6)
        self.usernam.setGeometry(QtCore.QRect(10, 15, 51, 21))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        self.usernam.setFont(font)
        self.usernam.setObjectName("usernam")
        self.singlelink = QtWidgets.QCheckBox(self.tab_6)
        self.singlelink.setGeometry(QtCore.QRect(10, 500, 131, 31))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.singlelink.sizePolicy().hasHeightForWidth())
        self.singlelink.setSizePolicy(sizePolicy)
        self.singlelink.setObjectName("singlelink")
        self.tabWidget.addTab(self.tab_6, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.drop_data_table = QtWidgets.QPushButton(self.tab)
        self.drop_data_table.setGeometry(QtCore.QRect(10, 590, 81, 31))
        self.drop_data_table.setStyleSheet(
            "QPushButton {\n"
            "    color: rgb(27, 29, 35);\n"
            "    border: 2px solid  rgb(141, 127, 157);\n"
            "    background-color: rgb(157, 156, 179);\n"
            "    border-radius: 6px;    \n"
            "\n"
            "}\n"
            "QPushButton:hover {\n"
            "    background-color: rgb(188, 174, 206);\n"
            "    border: 2px solid rgb(61, 70, 86);\n"
            "}\n"
            "QPushButton:pressed {    \n"
            "    background-color: rgb(35, 40, 49);\n"
            "    border: 2px solid rgb(43, 50, 61);\n"
            "}\n"
            "QPushButton:disabled {\n"
            "    color: rgb(117, 117, 117);\n"
            "    background-color: rgb(51, 52, 68);\n"
            "}"
        )
        self.drop_data_table.setObjectName("drop_data_table")
        self.show_data_table = QtWidgets.QPushButton(self.tab)
        self.show_data_table.setGeometry(QtCore.QRect(230, 350, 81, 31))
        self.show_data_table.setStyleSheet(
            "QPushButton {\n"
            "    color: rgb(27, 29, 35);\n"
            "    border: 2px solid  rgb(141, 127, 157);\n"
            "    background-color: rgb(157, 156, 179);\n"
            "    border-radius: 6px;    \n"
            "\n"
            "}\n"
            "QPushButton:hover {\n"
            "    background-color: rgb(188, 174, 206);\n"
            "    border: 2px solid rgb(61, 70, 86);\n"
            "}\n"
            "QPushButton:pressed {    \n"
            "    background-color: rgb(35, 40, 49);\n"
            "    border: 2px solid rgb(43, 50, 61);\n"
            "}\n"
            "QPushButton:disabled {\n"
            "    color: rgb(117, 117, 117);\n"
            "    background-color: rgb(51, 52, 68);\n"
            "}"
        )
        self.show_data_table.setObjectName("show_data_table")
        self.databaselist = QtWidgets.QListWidget(self.tab)
        self.databaselist.setGeometry(QtCore.QRect(10, 390, 301, 191))
        self.databaselist.setStyleSheet(
            "QListWidget{\n"
            "    background-color: rgb(27, 29, 35);\n"
            "    border-radius: 5px;\n"
            "    border: 2px solid rgb(91, 101, 124);\n"
            "    padding: 5px;\n"
            "    padding-left: 10px;\n"
            "}\n"
            "QListWidget:hover{\n"
            "    border: 2px solid rgb(64, 71, 88);\n"
            "}\n"
            "QListWidget QAbstractItemView {\n"
            "    color: rgb(85, 170, 255);    \n"
            "    background-color: rgb(27, 29, 35);\n"
            "    padding: 10px;\n"
            "    selection-background-color: rgb(39, 44, 54);\n"
            "}"
        )
        self.databaselist.setObjectName("databaselist")

        self.show_data_table_2 = QtWidgets.QPushButton(
            self.tab, clicked=lambda: self.tables_list()
        )
        self.show_data_table_2.setGeometry(QtCore.QRect(140, 350, 81, 31))
        self.show_data_table_2.setStyleSheet(
            "QPushButton {\n"
            "    color: rgb(27, 29, 35);\n"
            "    border: 2px solid  rgb(141, 127, 157);\n"
            "    background-color: rgb(157, 156, 179);\n"
            "    border-radius: 6px;    \n"
            "\n"
            "}\n"
            "QPushButton:hover {\n"
            "    background-color: rgb(188, 174, 206);\n"
            "    border: 2px solid rgb(61, 70, 86);\n"
            "}\n"
            "QPushButton:pressed {    \n"
            "    background-color: rgb(35, 40, 49);\n"
            "    border: 2px solid rgb(43, 50, 61);\n"
            "}\n"
            "QPushButton:disabled {\n"
            "    color: rgb(117, 117, 117);\n"
            "    background-color: rgb(51, 52, 68);\n"
            "}"
        )
        self.show_data_table_2.setObjectName("show_data_table_2")

        self.tablemode = QtWidgets.QGroupBox(self.tab)
        self.tablemode.setGeometry(QtCore.QRect(0, 10, 131, 61))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setBold(True)
        font.setWeight(75)
        self.tablemode.setFont(font)
        self.tablemode.setObjectName("tablemode")
        self.imagemode = QtWidgets.QRadioButton(self.tablemode)
        self.imagemode.setGeometry(QtCore.QRect(30, 20, 91, 17))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setBold(True)
        font.setWeight(75)
        self.imagemode.setFont(font)
        self.imagemode.setChecked(True)
        self.imagemode.setObjectName("imagemode")
        self.listmode = QtWidgets.QRadioButton(self.tablemode)
        self.listmode.setGeometry(QtCore.QRect(30, 40, 82, 17))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setBold(True)
        font.setWeight(75)
        self.listmode.setFont(font)
        self.listmode.setObjectName("listmode")
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab)
        self.groupBox_2.setGeometry(QtCore.QRect(0, 90, 121, 281))
        self.groupBox_2.setFlat(False)
        self.groupBox_2.setCheckable(False)
        self.groupBox_2.setObjectName("groupBox_2")

        MainWindow.setWindowIcon(QtGui.QIcon("logo/IMicon.ICO"))

        self.checkBox_1 = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBox_1.setGeometry(QtCore.QRect(30, 20, 70, 17))
        self.checkBox_1.setChecked(True)
        self.checkBox_1.setObjectName("checkBox")
        self.checkBox_2 = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBox_2.setGeometry(QtCore.QRect(30, 50, 70, 17))
        self.checkBox_2.setChecked(True)
        self.checkBox_2.setObjectName("checkBox_2")
        self.checkBox_3 = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBox_3.setGeometry(QtCore.QRect(30, 80, 70, 17))
        self.checkBox_3.setChecked(True)
        self.checkBox_3.setObjectName("checkBox_3")
        self.checkBox_4 = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBox_4.setGeometry(QtCore.QRect(30, 110, 70, 17))
        self.checkBox_4.setChecked(True)
        self.checkBox_4.setObjectName("checkBox_4")
        self.checkBox_5 = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBox_5.setGeometry(QtCore.QRect(30, 140, 70, 17))
        self.checkBox_5.setChecked(True)
        self.checkBox_5.setObjectName("checkBox_5")
        self.checkBox_6 = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBox_6.setGeometry(QtCore.QRect(30, 170, 70, 17))
        self.checkBox_6.setChecked(True)
        self.checkBox_6.setObjectName("checkBox_6")
        self.checkBox_7 = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBox_7.setGeometry(QtCore.QRect(30, 200, 81, 17))
        self.checkBox_7.setChecked(True)
        self.checkBox_7.setObjectName("checkBox_7")
        self.checkBox_8 = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBox_8.setGeometry(QtCore.QRect(30, 230, 70, 17))
        self.checkBox_8.setChecked(True)
        self.checkBox_8.setObjectName("checkBox_8")
        self.checkBox_9 = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBox_9.setGeometry(QtCore.QRect(30, 260, 70, 17))
        self.checkBox_9.setChecked(True)
        self.checkBox_9.setObjectName("checkBox_9")

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.checkBox_10 = QtWidgets.QCheckBox(self.tab_2)
        self.checkBox_10.setChecked(False)
        self.checkBox_10.setGeometry(QtCore.QRect(10, 600, 101, 17))
        self.checkBox_10.setObjectName("checkBox_10")
        self.tabWidget.addTab(self.tab_2, "")
        self.gridLayout_3.addWidget(self.tabWidget, 0, 0, 3, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.statusbar.setStyleSheet("color: rgb(241, 241, 241);")
        MainWindow.setStatusBar(self.statusbar)

        self.abouttext = QtWidgets.QTextBrowser(self.tab_2)
        self.abouttext.setObjectName("abouttext")
        self.abouttext.setGeometry(QtCore.QRect(20, 160, 281, 401))
        self.abouttext.setOpenExternalLinks(True)
        self.abouttext.setOpenLinks(True)
        self.instapng = QtWidgets.QLabel(self.tab_2)
        self.instapng.setObjectName("instapng")
        self.instapng.setGeometry(QtCore.QRect(20, 20, 120, 120))
        font7 = QtGui.QFont()
        font7.setFamily("MS Serif")
        self.instapng.setFont(font7)
        self.instapng.setFrameShadow(QtWidgets.QFrame.Raised)
        self.instapng.setPixmap(QtGui.QPixmap("logo/IM_PNG.png"))
        self.instapng.setScaledContents(True)

        self.table_mode()
        self.imagemode.toggled.connect(self.table_mode)
        self.listmode.toggled.connect(self.table_mode)
        for cb in self.groupBox_2.findChildren(QtWidgets.QCheckBox):
            cb.clicked["bool"].connect(self.table_col)

        self.tables_list()
        self.show_data_table.clicked.connect(self.showtable)
        self.drop_data_table.clicked.connect(self.table_drop)

        self.likesmin.clicked.connect(self.likesmin_input.setEnabled)
        self.datelimit.clicked.connect(self.datelimit_input.setEnabled)

        self.table_col()
        self.reason.currentIndexChanged.connect(self.updat_reportbox2)
        self.list_to_login()
        self.imgai_location = ""

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.randomcm.clicked["bool"].connect(self.selecttext.setEnabled)
        self.comment.clicked["bool"].connect(self.commentbox.setEnabled)
        self.ocr.clicked["bool"].connect(self.ocr_input.setEnabled)
        self.addswitch.clicked["bool"].connect(self.switchspin.setEnabled)
        self.find.clicked["bool"].connect(self.findinput.setEnabled)
        self.comment.clicked["bool"].connect(self.randomcm.setEnabled)
        self.ai.clicked["bool"].connect(self.aiselect.setEnabled)
        self.likesmin.clicked["bool"].connect(self.likesmin_input.setEnabled)
        self.datelimit.clicked["bool"].connect(self.datelimit_input.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "InstaMachine"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Image"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Stats"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Price"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Name"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Phone"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Post Date"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "Search Date"))
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "Hashtag"))
        item = self.tableWidget.horizontalHeaderItem(8)
        item.setText(_translate("MainWindow", "Link"))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.setSortingEnabled(__sortingEnabled)
        self.ocr.setText(_translate("MainWindow", "OCR "))
        self.comment.setText(_translate("MainWindow", "Comment"))
        self.report.setText(_translate("MainWindow", "Report"))
        self.likesmin.setText(_translate("MainWindow", "Likes min"))
        self.followcombo.setItemText(0, _translate("MainWindow", "-"))
        self.followcombo.setItemText(1, _translate("MainWindow", "Follow"))
        self.followcombo.setItemText(2, _translate("MainWindow", "Unfollow"))
        self.set_like.setText(_translate("MainWindow", "Set Like"))
        self.overwrite.setText(_translate("MainWindow", "Overwrite Table"))
        self.likecombo.setItemText(0, _translate("MainWindow", "-"))
        self.likecombo.setItemText(1, _translate("MainWindow", "Like"))
        self.likecombo.setItemText(2, _translate("MainWindow", "Unlike"))
        self.datelimit.setText(_translate("MainWindow", "Date limit"))
        self.datelimit_input.setDisplayFormat(_translate("MainWindow", "MMM d, yyyy"))
        self.aiselect.setText(_translate("MainWindow", "Select"))
        self.randomcm.setText(_translate("MainWindow", "Random CM"))
        self.aicombo.setItemText(0, _translate("MainWindow", "Include"))
        self.aicombo.setItemText(1, _translate("MainWindow", "Exclude"))
        self.find.setText(_translate("MainWindow", "Find"))
        self.resume.setText(_translate("MainWindow", "Resume "))
        self.set_follow.setText(_translate("MainWindow", "Set Follow "))
        self.ai.setText(_translate("MainWindow", "Image A.I"))
        self.screenshot.setText(_translate("MainWindow", "Screenshot"))
        self.ocrlang.setItemText(0, _translate("MainWindow", "eng"))
        self.ocrlang.setItemText(1, _translate("MainWindow", "fas"))
        self.price.setText(_translate("MainWindow", "Price"))
        self.radiotag.setText(_translate("MainWindow", "Tag"))
        self.radiolocation.setText(_translate("MainWindow", "Location"))
        self.radioperson.setText(_translate("MainWindow", "Person"))
        self.radioButton_4.setText(_translate("MainWindow", "Single Link"))
        self.go.setText(_translate("MainWindow", "Go!"))
        self.reason.setItemText(0, _translate("MainWindow", "Select reason"))
        self.reason.setItemText(1, _translate("MainWindow", "It's spam"))
        self.reason.setItemText(
            2, _translate("MainWindow", "Nudity or sexual activity")
        )
        self.reason.setItemText(3, _translate("MainWindow", "Hate speech or symbols"))
        self.reason.setItemText(
            4, _translate("MainWindow", "Violence or dangerous organizations")
        )
        self.reason.setItemText(
            5, _translate("MainWindow", "Sale of illegal or regulated goods")
        )
        self.reason.setItemText(6, _translate("MainWindow", "Bullying or harassment"))
        self.reason.setItemText(
            7, _translate("MainWindow", "Intellectual property violation")
        )
        self.reason.setItemText(8, _translate("MainWindow", "Suicide or self-injury"))
        self.reason.setItemText(9, _translate("MainWindow", "Eating disorders"))
        self.reason.setItemText(10, _translate("MainWindow", "Scam or fraud"))
        self.reason.setItemText(11, _translate("MainWindow", "False information"))
        self.reason.setItemText(12, _translate("MainWindow", "I just don't like it"))
        self.scroll_limit.setText(_translate("MainWindow", "Scrolls"))
        self.selecttext.setText(_translate("MainWindow", "Select text"))
        self.bulkimage.setText(_translate("MainWindow", "Bulk Image Download"))
        self.label_2.setText(
            _translate(
                "MainWindow",
                "Filters                                                                                         ",
            )
        )
        self.label.setText(
            _translate(
                "MainWindow",
                "Actions                                                                                         ",
            )
        )
        self.phone.setText(_translate("MainWindow", "Phone"))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_5), _translate("MainWindow", "Session")
        )
        self.remember.setText(_translate("MainWindow", "Remember"))
        self.switchevery.setText(_translate("MainWindow", "Swich Every"))
        self.importlist.setText(_translate("MainWindow", "Import list"))
        self.min.setText(_translate("MainWindow", "Link"))
        self.add_account.setText(_translate("MainWindow", "Add To List"))
        self.remove_acc.setText(_translate("MainWindow", "Remove"))
        self.addswitch.setText(_translate("MainWindow", "Auto Switch"))
        self.password.setText(_translate("MainWindow", "Password"))
        self.select_acc.setText(_translate("MainWindow", "Select"))
        self.usernam.setText(_translate("MainWindow", "Username"))
        self.singlelink.setText(_translate("MainWindow", "Swich cn a Single Link"))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_6), _translate("MainWindow", "Accounts")
        )
        self.drop_data_table.setText(_translate("MainWindow", "Drop Table"))
        self.show_data_table.setText(_translate("MainWindow", "Show Table"))
        self.tablemode.setTitle(_translate("MainWindow", "Table Mode:"))
        self.imagemode.setText(_translate("MainWindow", "Image Mode"))
        self.listmode.setText(_translate("MainWindow", "List Mode"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Table Columns:"))
        self.checkBox_9.setText(_translate("MainWindow", "Link"))
        self.checkBox_2.setText(_translate("MainWindow", "Stats"))
        self.checkBox_1.setText(_translate("MainWindow", "Image"))
        self.checkBox_5.setText(_translate("MainWindow", "Phone"))
        self.checkBox_4.setText(_translate("MainWindow", "Name"))
        self.checkBox_7.setText(_translate("MainWindow", "Search Date"))
        self.checkBox_3.setText(_translate("MainWindow", "Price"))
        self.checkBox_8.setText(_translate("MainWindow", "Hashtag"))
        self.checkBox_6.setText(_translate("MainWindow", "Post Date"))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Table view")
        )
        self.checkBox_10.setText(_translate("MainWindow", "Show Webdriver"))
        self.show_data_table_2.setText(_translate("MainWindow", "Refresh"))
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "About")
        )
        self.abouttext.setHtml(
            _translate(
                "MainWindow",
                '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n'
                '<html><head><meta name="qrichtext" content="1" /><style type="text/css">\n'
                "p, li { white-space: pre-wrap; }\n"
                "</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:transparent;"><span style=" font-size:10pt; color:#ffffff; background-color:transparent;">InstaMachine ver 1.0</span></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:transparent;"><span style=" font-size:10pt; color:#ffffff; background-color:transparent;">by R.Jorj</span></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:transparent;"><span style'
                '=" font-size:10pt; color:#ffffff;"><br /></span></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:transparent;"><span style=" font-size:10pt; color:#ffffff; background-color:transparent;">InstaMachine is a post-oriented Instagram bot which means it is more focused on gathering data and storing it inside the SQLite database.</span></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:transparent;"><span style=" font-size:10pt; color:#ffffff; background-color:transparent;">I made this app solely to put to test my web scraping abilities as a beginner programmer and build up some portfolio, therefore I did not use any python\'s Instagram library like instapy. Please NOTE as I mentioned this is just a personal project and I do not encourage anyone to use this app against Instagram\'s terms of use.</span></p>\n'
                '<p style="-qt'
                '-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:transparent;"><br /></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:transparent;"><span style=" font-size:10pt; color:#ffffff; background-color:transparent;">In the end, anyone is welcome to contribute to this app. there is a lot of room for improvements. Please check my github for my other projects.</span></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:transparent;"><span style=" font-size:10pt; color:#ffffff;"><br /></span></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:transparent;"><a href="https://github.com/theRJorj"><span style=" font-size:10pt; text-decoration: '
                'underline; color:#a35cf9; background-color:transparent;">Github.com/theRJorj</span></a></p>\n'
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:transparent;"><span style=" font-size:10pt; color:#ffffff; background-color:transparent;">Email:www.the.r.jorj@gmail.com</span></p></body></html>',
                None,
            )
        )
        self.instapng.setText("")

    def table_drop(self):
        try:
            mycursor.execute(
                f"DROP TABLE IF EXISTS {self.databaselist.currentItem().text()} "
            )
            self.databaselist.clear()
            self.tables_list()
            self.statusbar.showMessage("Table droped")
        except:
            pass

    def table_col(self):
        counter = 0
        for i in self.groupBox_2.findChildren(QtWidgets.QCheckBox):
            if i.isChecked() == True:
                self.tableWidget.setColumnHidden(counter, False)
            else:
                self.tableWidget.setColumnHidden(counter, True)
            counter += 1

    def tables_list(self):
        self.databaselist.clear()
        mycursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tlist = mycursor.fetchall()
        for i in tlist:
            i = " ".join(i)
            self.databaselist.addItem(i)

    def table_mode(self):
        if self.listmode.isChecked():
            self.tableWidget.setColumnHidden(0, True)
            self.checkBox_1.setChecked(False)
            self.checkBox_1.setEnabled(False)
            return self.tableWidget.verticalHeader().setDefaultSectionSize(40)
        elif self.imagemode.isChecked():
            self.tableWidget.setColumnHidden(0, False)
            self.checkBox_1.setChecked(True)
            self.checkBox_1.setEnabled(True)
            return self.tableWidget.verticalHeader().setDefaultSectionSize(200)

    def login(self, browser):

        browser.get("https://www.instagram.com")
        browser.implicitly_wait(10)
        time.sleep(2)
        try:
            cookies = pickle.load(
                open(f"logins/cookies/{self.user_input.text()}_cookies.pkl", "rb")
            )
            for cookie in cookies:
                browser.add_cookie(cookie)
            self.statusbar.showMessage("Login by Cookie")
        except:
            self.add_acc(browser)

    def add_acc(self, browser):

        try:
            browser.find_element_by_xpath(
                "//*[@id='loginForm']/div/div[1]/div/label/input"
            ).click()
            user = browser.find_element_by_tag_name("input")
            user.send_keys(self.user_input.text())
            time.sleep(1)
            browser.find_element_by_xpath(
                "//*[@id='loginForm']/div/div[2]/div/label/input"
            ).click()

            password = browser.find_element_by_name("password")
            password.send_keys(self.pass_input.text())
            password.send_keys(Keys.ENTER)
            time.sleep(3)
            try:
                er = browser.find_element_by_xpath('//*[@id="slfErrorAlert"]')
                er = er.text
                self.statusbar.showMessage(er)
                print(er)
                return quit()

            except:
                pass

            browser.implicitly_wait(5)
            browser.find_element_by_xpath(
                "//*[@id='react-root']/section/main/div/div/div/section/div/button"
            ).click()
            time.sleep(1)
            try:
                browser.implicitly_wait(5)
                browser.find_element_by_xpath(
                    "/html/body/div[5]/div/div/div/div[3]/button[1]"
                ).click()
                time.sleep(1)
                pass
            except:
                pass
            if self.remember.isChecked():
                pickle.dump(
                    browser.get_cookies(),
                    open(f"logins/cookies/{self.user_input.text()}_cookies.pkl", "wb"),
                )
            else:
                pass
            self.statusbar.showMessage("Login Successful")
            print("Login Successful")
        except:
            self.statusbar.showMessage("Login Error!")
            print("Login Error!")
            return quit()

    def list_add_acc(self):
        with open("logins/login.txt", "a") as f:
            l = [self.user_input.text(), self.pass_input.text()]
            f.write(str(l))
            f.write("\n")
            f.close()
            self.acclist()

    def acclist(self):
        try:
            self.acc_list.clear()
            with open("logins/login.txt", "r") as f:
                alist = f.readlines()
                for i in alist:
                    i = re.sub(r"\n", "", str(i))
                    self.acc_list.addItem(i)
        except:
            pass

    def list_to_login(self):
        try:
            with open("logins/login.txt", "r") as f:
                up = ast.literal_eval(f.readline())
                self.user_input.setText(up[0])
                self.pass_input.setText(up[1])
                f.close()
        except:
            pass

    def import_list(self):
        self.textfile_acc = QtWidgets.QFileDialog.getOpenFileName(
            None, "Open text file", "", "Text Files (*.txt)"
        )
        if self.textfile_acc != ("", ""):
            txt_location = self.textfile_acc[0]
            f = open(rf"{txt_location}", "r")
            txt = f.read()
            f.close
            return self.acc_list.addItem(txt)
        else:
            return

    def acc_select(self):
        if self.acc_list.currentRow() != (-1):
            s = self.acc_list.currentItem().text()
            s = ast.literal_eval(s)
            self.user_input.setText(s[0])
            self.pass_input.setText(s[1])

    def removeacc(self):
        listItems = self.acc_list.selectedItems()
        if not listItems:
            return
        for item in listItems:
            self.acc_list.takeItem(self.acc_list.row(item))
        s = "\n".join(
            self.acc_list.item(i).text() for i in range(self.acc_list.count())
        )
        with open("logins/login.txt", "w") as f:
            f.write(s)
            f.close()
            self.statusbar.showMessage("Account removed!")

    def check_select(self):
        if self.randomcm.isChecked():
            self.selecttext.setEnabled(True)
        else:
            self.selecttext.setEnabled(False)
            self.commentbox.clear()

    def image_dialog(self):
        self.aiselect.setText("Select Image")
        self.imgfile = QtWidgets.QFileDialog.getOpenFileName(
            None, "Open image file", "", "Images (*.png *.jpg *.jpeg)"
        )
        if self.imgfile != ("", ""):
            self.imgai_location = self.imgfile[0]
            self.aiselect.setText("Selected!")
            self.statusbar.showMessage(self.imgai_location)
            print(self.imgai_location)
            return self.imgai_location
        else:
            return

    def text_dialog(self):
        self.textfile = QtWidgets.QFileDialog.getOpenFileName(
            None, "Open text file", "", "Text Files (*.txt)"
        )

        if self.textfile != ("", ""):
            txt_location = self.textfile[0]
            f = open(rf"{txt_location}", "r")
            txt = f.read()
            f.close
            return self.commentbox.setPlainText(txt)
        else:
            return

    def updat_reportbox2(self):
        self.reason2.clear()
        if self.reason.currentIndex() == 2:
            self.reason2.addItems(r1)
        if self.reason.currentIndex() == 4:
            self.reason2.addItems(r2)
        if self.reason.currentIndex() == 5:
            self.reason2.addItems(r3)
        if self.reason.currentIndex() == 6:
            self.reason2.addItems(r4)
        if self.reason.currentIndex() == 11:
            self.reason2.addItems(r5)

    def showtable(self):
        try:
            self.tableWidget.setRowCount(0)
            if self.show_data_table.clicked:
                q = self.databaselist.currentItem().text()
            else:
                q = self.search.text()
                q = q.replace(" ", "_")

            mycursor.execute(f"SELECT * FROM {q}")
            result = mycursor.fetchall()

            for row_number, row_data in enumerate(result):
                self.tableWidget.insertRow(row_number)
                for column_number, column_data in enumerate(row_data):
                    item = str(column_data)
                    if column_number == 0:
                        item = self.imagelabel(column_data)
                        self.tableWidget.setCellWidget(row_number, column_number, item)
                    else:
                        self.tableWidget.setItem(
                            row_number, column_number, QtWidgets.QTableWidgetItem(item)
                        )
            self.tableWidget.verticalHeader().setDefaultSectionSize(200)
        except:
            pass

    def imagelabel(self, image):
        imglabel = QtWidgets.QLabel(self.centralwidget)
        imglabel.setText("")
        imglabel.setScaledContents(True)
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(image, "jpeg")
        imglabel.setPixmap(pixmap)
        return imglabel

    def add_table(self, title):
        if re.search(r"^\d", title) != None:
            title = "_" + str(title)
        else:
            pass
        if self.overwrite.isChecked() == False:
            tablelist = conn.execute(
                f"""SELECT name FROM sqlite_master WHERE type='table'AND name='{title}'; """
            ).fetchall()

            if tablelist == []:
                mycursor.execute(
                    f"""CREATE TABLE {title} (image mediumblob not null,Stats varchar(500),Price varchar(500),Title varchar(50),Phone varchar(255),PostDate varchar(50),SearchDate varchar(50),Hashtags varchar(500),link varchar(500) primary key)"""
                )

        else:
            mycursor.execute(f"DROP TABLE IF EXISTS {title} ")
            mycursor.execute(
                f"""CREATE TABLE {title} (image mediumblob not null,Stats varchar(500),Price varchar(500),Title varchar(50),Phone varchar(255),PostDate varchar(50),SearchDate varchar(50),Hashtags varchar(500),link varchar(500) primary key)"""
            )

    def lastlink(self, title, alink):
        q = f"SELECT * FROM {title} WHERE link='{alink}' GROUP BY link "
        mycursor.execute(q)
        row = mycursor.fetchall()
        if row != None:
            return

    def follow(self, browser, stats_list):
        if self.followcombo.currentText() == "Follow":
            try:
                wait = WebDriverWait(browser, 5)
                follow_status = wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            "//*[@id='react-root']/section/main/div/div[1]/article/div/div[2]/div/div[1]/div/header/div[2]/div[1]/div[2]/button",
                        )
                    )
                )
                follow_status = browser.find_element_by_xpath(
                    "//*[@id='react-root']/section/main/div/div[1]/article/div/div[2]/div/div[1]/div/header/div[2]/div[1]/div[2]/button/div"
                )
                if follow_status.text == "Follow":
                    follow_status.click()
                    stats_list.append("Followed")

            except:
                self.statusbar.showMessage("follow not found")
                print("follow not found")
                return quit()

    def unfollow(self, browser, stats_list):
        if self.followcombo.currentText() == "Unfollow":
            try:
                wait = WebDriverWait(browser, 5)
                follow_status = wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            "/html/body/div[5]/div[3]/div/article/div/div[2]/div/div/div[1]/div/header/div[2]/div[1]/div[2]/button",
                        )
                    )
                )

                if follow_status.text == "Following":
                    follow_status.click()
                    time.sleep(1)
                    wait.until(
                        EC.element_to_be_clickable(
                            (By.XPATH, "/html/body/div[5]/div/div/div/div[3]/button[1]")
                        )
                    ).click()
                    time.sleep(2)
                    stats_list.append("Unfollowed")

            except:
                self.statusbar.showMessage("unfollow not found")
                print("unfollow not found")
                return quit()

    def comments(self, browser, stats_list):
        if self.comment.isChecked():
            try:
                browser.find_element_by_class_name("RxpZH").click()
                time.sleep(1)
                comment_text = browser.find_element_by_tag_name("textarea")
                browser.implicitly_wait(20)
                if self.randomcm.isChecked():
                    randtxt = (self.commentbox.toPlainText()).split("\n")
                    comment_text.send_keys(random.choice(randtxt))
                else:
                    comment_text.send_keys(self.commentbox.toPlainText())
                time.sleep(1)
                comment_text.send_keys(Keys.ENTER)
                time.sleep(4)
                stats_list.append("Commented")
            except:
                self.statusbar.showMessage("Comment is disabled on this post!")
                print("Comment is disabled on this post!")
                pass

    def likes(self, browser, stats_list):
        if self.likecombo.currentText() == "Like":
            like = browser.find_element_by_class_name("fr66n")
            soup = BeautifulSoup(like.get_attribute("innerHTML"), "html.parser")
            if soup.find("svg")["aria-label"] == "Like":
                like.click()
                time.sleep(1)
                stats_list.append("Liked")

    def unlike(self, browser, stats_list):
        if self.likecombo.currentText() == "Unlike":
            ulike = browser.find_element_by_class_name("fr66n")
            soup = BeautifulSoup(ulike.get_attribute("innerHTML"), "html.parser")
            if soup.find("svg")["aria-label"] == "Unlike":
                ulike.click()
                time.sleep(1)
                stats_list.append("Unliked")

    def screenshots(self, browser, link, stats_list):
        if self.screenshot.isChecked():
            time.sleep(1)
            link = str(link).replace("/", "").replace(".", "").replace(":", "")
            browser.save_screenshot("screenshot.png")
            sn = r"screenshot.png"
            sr = rf"screenshots/{link}.png"
            time.sleep(1)
            try:
                os.rename(sn, sr)
            except FileExistsError:
                os.replace(sn, sr)
            stats_list.append("Screenshot taken")

    def reportit(self, browser, reason2index, stats_list):
        if self.report.isChecked():
            browser.find_element_by_xpath(
                "//*[@id='react-root']/section/main/div/div[1]/article/div/div[2]/div/div[1]/div/div/button"
            ).click()
            time.sleep(1)
            browser.find_element_by_xpath(
                "/html/body/div[5]/div/div/div/div/button[1]"
            ).click()
            time.sleep(2)
            report_cat = f"/html/body/div[5]/div/div/div/div[2]/div/div/div/div[3]/button[{self.reason.currentIndex()}]"
            browser.find_element_by_xpath(f"{report_cat}").click()
            time.sleep(2)
            if self.reason.currentIndex() in (2, 4, 5, 6, 11):
                report_cat2 = f'//*[@id="igCoreRadioButtontag-{reason2index}"]'
                browser.find_element_by_xpath(f"{report_cat2}").click()
                time.sleep(2)
                soup = BeautifulSoup(browser.page_source, "html.parser")
                next_move = soup.find(text="Submit Report")
                if next_move != None:
                    try:
                        browser.find_element_by_xpath(
                            "/html/body/div[5]/div/div/div/div[2]/div/div/div/div[6]/button"
                        ).click()

                        time.sleep(2)
                        browser.find_element_by_xpath(
                            "/html/body/div[5]/div/div/div/div/div/div/div[4]/button"
                        ).click()
                        stats_list.append("Reported")

                    except:
                        browser.find_element_by_xpath(
                            "/html/body/div[5]/div/div/div/div[2]/div/div/div/div[6]/button"
                        ).click()
                        time.sleep(1)
                        stats_list.append("Reported")

                else:
                    browser.find_element_by_xpath(
                        "/html/body/div[5]/div/div/div/div[2]/div/div/button"
                    ).click()
                    time.sleep(2)
                    browser.find_element_by_xpath(
                        "/html/body/div[5]/div/div/div/div/div/div/div[4]/button"
                    ).click()
                    stats_list.append("Reported")
            else:
                try:
                    time.sleep(1)
                    browser.find_element_by_xpath(
                        "/html/body/div[5]/div/div/div/div/div/div/div[4]/button"
                    ).click()
                    time.sleep(1)
                    stats_list.append("Reported")
                except:
                    browser.find_element_by_xpath(
                        "/html/body/div[5]/div/div/div/div[2]/div/div/button"
                    ).click()
                    time.sleep(1)

                    browser.find_element_by_xpath(
                        "/html/body/div[5]/div/div/div/div/div/div/div[4]/button"
                    ).click()
                    time.sleep(1)
                    stats_list.append("Reported")

    def bulk_img(self, buimages, links, browser):
        if self.bulkimage.isChecked():
            for p, l in zip(buimages, links):
                browser.implicitly_wait(10)
                link = l.find("a", href=True)["href"]
                image = p.get_attribute("src")
                image_data = requests.get(image).content
                imlink = str(link).replace("/", "")
                image_name = imlink
                with open(
                    r"insta image/" + image_name + ".jpeg",
                    "wb",
                ) as f:
                    f.write(image_data)
                    f.close()
                    imglocation = "insta image/bulk_%s.jpeg" % (image_name)

    def photoai(self, image_name, stats_list):
        img1 = cv2.imread(f"{self.imgai_location}")
        img2 = cv2.imread(f"insta image/{image_name}.jpeg")
        if img1.shape == img2.shape:
            dif = cv2.subtract(img1, img2)
            b, g, r = cv2.split(dif)
            if (
                cv2.countNonZero(b) == 0
                and cv2.countNonZero(g) == 0
                and cv2.countNonZero(r) == 0
            ):
                print("Images match completely")
                stats_list.append("Image matches")
                return True
            else:
                print("Images NOT match")
                self.statusbar.showMessage("Images NOT match")
                return False
        else:
            return False

    def ocrtext(self, image_name, stats_list):
        time.sleep(1)
        pytesseract.pytesseract.tesseract_cmd = (
            r"C:/Program Files/Tesseract-OCR/tesseract.exe"
        )
        image = cv2.imread(f"insta image/{image_name}.jpeg")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        f = open("ocr_rec.txt", "a", encoding="utf-8")
        text = pytesseract.image_to_string(image, lang=str(self.ocrlang.currentText()))
        f.write(text)
        f.write("\n")
        f.close
        ocfile = open("ocr_rec.txt", "r+", encoding="utf-8")
        ocfiletxt = ocfile.read()
        ocfile.truncate(0)
        ocfile.close()
        inputtext = self.ocr_input.text()
        ocr_compare = re.search(rf"{inputtext}", ocfiletxt, re.IGNORECASE)

        if ocr_compare != None and self.aicombo.currentIndex() == 0:
            stats_list.append("OCR matches")
            print("OCR matched")
            return True
        elif ocr_compare != None and self.aicombo.currentIndex() == 1:
            self.statusbar.showMessage("OCR matched,Ignored")
            print("OCR matched,Ignored")
            return False
        elif ocr_compare == None and self.aicombo.currentIndex() == 0:
            self.statusbar.showMessage("No OCR match found")
            print("No OCR match found")
            return False
        elif ocr_compare == None and self.aicombo.currentIndex() == 1:
            stats_list.append("OCR not match")
            return True
        else:
            self.statusbar.showMessage("OCR error")
            print("OCR error")
            return False

    def get_links(self, browser, title, stats_list):
        if os.path.isfile(f"links_lists/{title}_linkslist.txt") != True:
            time.sleep(2)
            if self.radiolocation.isChecked():
                browser.get("https://www.instagram.com/explore/locations/" + title)
                time.sleep(3)
            elif self.radioperson.isChecked():
                browser.get("https://www.instagram.com/" + title)
                time.sleep(3)
            else:
                browser.get("https://www.instagram.com/explore/tags/" + title)
                time.sleep(3)
            last_height = browser.execute_script("return document.body.scrollHeight")
            page_scroll = int(self.scroll_number.text())
            while page_scroll:

                time.sleep(5)
                soup = BeautifulSoup(browser.page_source, "html.parser")
                links = soup.find_all(class_="v1Nh3 kIKUG _bz0w")
                buimages = browser.find_elements_by_class_name("FFVAD")
                # -----------------------------------------------------
                self.bulk_img(buimages, links, browser)
                self.list_of_links(links, title)
                # -----------------------------------------------------
                time.sleep(1)
                browser.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);"
                )
                time.sleep(5)
                new_height = browser.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
                page_scroll -= 1

    def list_of_links(self, links, title):
        link_counter = 0
        links_list = []
        for l in links:
            full_link = l.find("a", href=True)["href"]
            full_link = "https://www.instagram.com" + full_link
            links_list.append(full_link)
            link_counter += 1

        links_file = open(f"links_lists/{title}_linkslist.txt", "a", encoding="utf-8")
        for j in links_list:
            links_file.write(str(j) + "\n")
        links_file.close()
        shutil.copyfile(
            rf"links_lists/{title}_linkslist.txt",
            rf"links_lists/links_progress/pop_{title}_linkslist.txt",
        )
        self.statusbar.showMessage(f"{link_counter} Links stored")
        print(f"{link_counter} Links stored")

    def likes_count(self, browser, stats_list):
        try:
            n = browser.find_element_by_xpath(
                '//*[@id="react-root"]/section/main/div/div[1]/article/div/div[2]/div/div[2]/section[2]/div/div/div/a/div/span'
            )
            n = n.text
            stats_list.append(n + " like")
            n = n.replace(",", "")
            return n

        except:
            pass

    def location_post(self, browser, stats_list):
        try:
            lp = browser.find_element_by_xpath(
                '//*[@id="react-root"]/section/main/div/div[1]/article/div/div[2]/div/div[1]/div/header/div[2]/div[2]/div/div[2]/div/a'
            )
            lp = lp.text
            stats_list.append("Location:" + lp)
        except:
            pass

    # Main code -----------------------------------------------------------------------------------------------

    def letsgo(self):

        self.statusbar.showMessage("Started...")
        now = datetime.date.today()
        now = str(now).replace("-", "_")

        options = webdriver.ChromeOptions()
        if self.checkBox_10.isChecked() == False:
            options.add_argument("headless")
        chrome_service = ChromeService("chromedriver")
        chrome_service.creationflags = CREATE_NO_WINDOW
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        user_agent = "Chrome/83.0.4103.116"
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument(f"user-agent={user_agent}")
        options.add_argument("window-size=1920x1080")
        options.add_argument("--disable-gpu")
        browser = webdriver.Chrome(
            executable_path=r"chromedriver.exe",
            chrome_options=options,
            service=chrome_service,
        )

        counter = 0
        stats_list = []
        title = self.search.text()
        title = title.replace(" ", "_")
        reason2index = self.reason2.currentIndex()

        self.add_table(title)

        self.login(browser)

        if self.radioButton_4.isChecked():
            link = title
            pass
        else:
            # ---------------------------------------------------------
            self.get_links(browser, title, stats_list)
            # ----------------------------------------------------------
            if self.resume.isChecked():
                links_file = open(
                    f"links_lists/links_progress/pop_{title}_linkslist.txt",
                    "r",
                    encoding="utf-8",
                )
                links_list = ast.literal_eval(links_file.read())

            else:
                links_file = open(
                    f"links_lists/{title}_linkslist.txt",
                    "r",
                    encoding="utf-8",
                )
                links_list = links_file.read()
                links_list = links_list.split("\n")

            links_file.close()
            links_list.pop()

            if self.addswitch.isChecked():
                switch_int = self.switchspin.text()
                switch_count = int(switch_int)
        links_list = list(set(links_list))

        while len(links_list) != 0:
            self.statusbar.showMessage(str(len(links_list) - 1) + " Links remaining...")
            if self.addswitch.isChecked() and switch_count == 0:
                browser.close()
                switch_count = int(self.switchspin.text())
                list_count = self.acc_list.count()
                print(list_count)
                listidx = self.acc_list.currentRow()
                print(listidx)
                if listidx == list_count:
                    break
                else:
                    item = self.acc_list.item(listidx + 1).text()
                    print(item)
                    item = ast.literal_eval(item)
                    self.user_input.setText(item[0])
                    self.pass_input.setText(item[1])
                    browser = webdriver.Chrome(
                        executable_path=r"chromedriver.exe",
                        chrome_options=options,
                    )
                    self.login(browser)
                    time.sleep(3)
                    pass
            else:
                pass
            if self.singlelink.isChecked():
                link = title
            else:
                link_prog = open(
                    f"links_lists/links_progress/pop_{title}_linkslist.txt",
                    "w",
                    encoding="utf-8",
                )
                link_prog.write(str(links_list))
                link_prog.close()
                link = links_list.pop(0)

            browser.get(link)
            browser.implicitly_wait(10)
            try:
                sry = browser.find_element_by_xpath(
                    '//*[@id="react-root"]/section/main/div/div/h2'
                )
                if sry.text == "Sorry, this page isn't available.":
                    continue
            except:
                pass

            time.sleep(1)
            images = browser.find_element_by_class_name("FFVAD")
            image = images.get_attribute("src")
            image_data = requests.get(image).content
            imlink = str(link).replace("/", "").replace(":", "")
            image_name = imlink

            try:
                name = WebDriverWait(browser, 5).until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "//*[@id='react-root']/section/main/div/div[1]/article/div/div[2]/div/div[1]/div/header/div[2]/div[1]/div[1]/div/span/a",
                        )
                    )
                )
                name = name.text

            except TimeoutException:
                print("name not found")
                return quit()

            try:
                wait = WebDriverWait(browser, 5)
                note = wait.until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "//*[@id='react-root']/section/main/div/div[1]/article/div/div[2]/div/div[2]/div[1]/ul/div/li/div/div/div[2]",
                        )
                    )
                )
                note = "".join(note.text)
            except:
                print("note not found")
                return quit()

            stats_list.append("Name: " + name)
            telephone = ""
            priced = ""
            # -----------------------------------------------------
            tel = re.search(
                r"[0][9]\d{9}|[9]\d{8}|[۰][۹]([۰-۹]{9})|[۹]([۰-۹]{8})", str(note)
            )

            if tel != None:
                tel = tel.group()
                re.sub("\s+", "", tel)
                telephone = tel
                stats_list.append("Phone listed: " + telephone)
            elif self.phone.isChecked() and tel == None:
                stats_list = []
                continue
            # -----------------------------------------------------
            prices = re.search(
                r"(قیمت)(.*)([۰-۹]+)|([۰-۹]+)(.*)(قیمت)|(قیمت)(.*)([0-9]+)|([0-9]+)(.*)(قیمت)|تومان|تومن|ریال|toman|([0-9]+)(.*)(price)|(price)(.*)([0-9]+)|([0-9]+)(.*)(تومان)|(تومان)([0-9]+)(.*)|([۰-۹]+)(.*)(تومان)|(تومان)(.*)([۰-۹]+)",
                str(note),
            )
            if prices != None:
                prices = prices.group()
                priced = prices
                stats_list.append("Price listed: " + priced)

            elif self.price.isChecked() and prices == None:
                stats_list = []
                continue
            # -----------------------------------------------------
            findtext = self.findinput.text()
            findings = re.search(rf"{findtext}", str(note))

            if self.find.isChecked() and findings != None:
                stats_list.append("Find matches")
                pass
            elif self.find.isChecked() and findings == None:
                stats_list = []
                continue
            # -----------------------------------------------------
            date = str(now)
            postdate = browser.find_element_by_class_name("_1o9PC")
            postdate = postdate.get_attribute("title")
            stats_list.append("Posted: " + postdate)
            stats_list.append("Searched: " + date)
            # -----------------------------------------------------
            lc = self.likes_count(browser, stats_list)
            self.location_post(browser, stats_list)
            # -----------------------------------------------------
            if self.datelimit.isChecked():
                dl = self.datelimit_input.date()
                dl = str(dl.toPyDate())
                pd = datetime.datetime.strptime(postdate, "%b %d, %Y").strftime(
                    "%Y-%m-%d"
                )
                if pd <= dl:
                    stats_list = []
                    continue
            # -----------------------------------------------------
            try:
                if self.likesmin.isChecked() and int(lc) <= int(
                    self.likesmin_input.text()
                ):
                    stats_list = []
                    continue
            except:
                pass
            # -----------------------------------------------------
            with open(
                r"insta image/" + image_name + ".jpeg",
                "wb",
            ) as f:
                f.write(image_data)
                f.close()
                imglocation = "insta image/%s.jpeg" % (image_name)
                # -----------------------------------------------------
                if self.ai.isChecked():
                    if (
                        self.photoai(image_name, stats_list) == True
                        and self.aicombo.currentIndex() == 0
                    ):
                        pass
                    elif (
                        self.photoai(image_name, stats_list) == True
                        and self.aicombo.currentIndex() == 1
                    ):
                        stats_list = []
                        continue
                    elif (
                        self.photoai(image_name, stats_list) != True
                        and self.aicombo.currentIndex() == 0
                    ):
                        pass
                    else:
                        stats_list = []
                        continue
                # -----------------------------------------------------
                if self.ocr.isChecked():
                    if self.ocrtext(image_name, stats_list) == True:
                        pass
                    else:
                        stats_list = []
                        continue
                # -----------------------------------------------------
                tags = ""
                tag = re.findall(r"#\S+", str(note))
                if tag != None:
                    tags = " ".join(tag)
                    stats_list.append("Hashtags stored")
                # -----------------------------------------------------
                self.reportit(browser, reason2index, stats_list)
                self.screenshots(browser, link, stats_list)
                self.follow(browser, stats_list)
                self.unfollow(browser, stats_list)
                self.likes(browser, stats_list)
                self.unlike(browser, stats_list)
                time.sleep(0.5)
                self.comments(browser, stats_list)
                # -----------------------------------------------------
                stat = "\n".join(stats_list)

                mycursor.execute(
                    f"insert or ignore into {title} values(?,?,?,?,?,?,?,?,?)",
                    (
                        image_to_binary(imglocation),
                        stat,
                        priced,
                        name,
                        telephone,
                        postdate,
                        date,
                        tags,
                        link,
                    ),
                )

                conn.commit()
                stats_list = []
                counter += 1
                if self.addswitch.isChecked():
                    switch_count -= 1
                continue

        Notification = "Done! You have %i new post/s" % (int(counter))
        conn.commit()
        self.statusbar.showMessage(Notification)
        print(Notification)
        self.showtable()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

# By the.R.JORJ
