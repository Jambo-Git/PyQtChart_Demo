#! python3
#coding: utf-8
import os
import sys
import math
import array

from PyQt5.QtCore import Qt, QTimer, QPointF
from PyQt5.QtWidgets import QApplication, QMainWindow

from PyQt5.QtChart import QChart, QChartView, QLineSeries

class DemoWindow(QMainWindow):
    def __init__(self, parent=None):
        super(DemoWindow, self).__init__(parent=parent)

        self.plotChart = QChart()
        self.plotChart.legend().hide()

        self.plotView = QChartView(self.plotChart)
        self.setCentralWidget(self.plotView)

        self.plotCurve = QLineSeries()
        self.plotCurve.setUseOpenGL(True)
        self.plotCurve.pen().setColor(Qt.red)
        self.plotChart.addSeries(self.plotCurve)

        self.plotChart.createDefaultAxes()
        self.plotChart.axisX().setLabelFormat('%d')

        self.RecvData = array.array('f')	# 存储接收到的传感器数据
        self.RecvIndx = 0

        self.tmrData = QTimer()				# 模拟传感器传送过来数据
        self.tmrData.setInterval(3)
        self.tmrData.timeout.connect(self.on_tmrData_timeout)
        self.tmrData.start()

        self.tmrPlot = QTimer()
        self.tmrPlot.setInterval(100)
        self.tmrPlot.timeout.connect(self.on_tmrPlot_timeout)
        self.tmrPlot.start()

    def on_tmrData_timeout(self):
    	val = math.sin(2*3.14 / 500 * self.RecvIndx)
    	self.RecvData.append(val)

    	self.RecvIndx += 1

    def on_tmrPlot_timeout(self):
    	self.RecvData = self.RecvData[-1000:]

    	plotData = []
    	for i, val in enumerate(self.RecvData):
    		plotData.append(QPointF(i, val))

    	self.plotCurve.replace(plotData)
    	self.plotChart.axisX().setMax(len(plotData))
    	self.plotChart.axisY().setRange(min(self.RecvData), max(self.RecvData))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DemoWindow()
    window.show()
    window.resize(700, 400)
    sys.exit(app.exec_())
