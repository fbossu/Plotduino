#!/usr/bin/env python
"""
Copyright 2014 Francesco Bossu
ciacco.posta@gmail.com

Plotduino is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

Plotduino is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

--------------------

"""
import sys, glib
from PyQt4 import QtGui, QtCore

#import my libraries
import mtp, data

class MainWin(QtGui.QMainWindow):
  def __init__( self, parent=None ):
    QtGui.QMainWindow.__init__( self, parent )
    self.setWindowTitle( 'Plotduino' )
    
    # the data acquisition
    self.data_source = data.data()
    self.data_source.selection = 0
    
    # time interval for the plot update
    self.timestep = 200
    
    # timer for updating the plot
    self.timer = QtCore.QTimer(self)

    #create the layout and connect the signals to the buttons
    self.set_layout()
    self.connectSignals()

  def set_layout( self ):
    """ definistion of the window layout """
    self.main_frame = QtGui.QWidget()
    #self.main_frame.setFixedHeight(500)
    
    self.plot = mtp.mtp( self.main_frame )
    
  
    #actual layout 
    #******************
    
    # layout left:
    #-------------
    vboxleft = QtGui.QVBoxLayout()
    
    # the matplotlib canvas
    vboxleft.addWidget(self.plot.canvas)    
 
    # the play and stop button
    hbox = QtGui.QHBoxLayout()
    self.play_button = QtGui.QPushButton("&Play")
    hbox.addWidget(self.play_button)
    self.stop_button = QtGui.QPushButton("&Stop")
    hbox.addWidget(self.stop_button)
    vboxleft.addLayout(hbox)

    #layout right:
    #------------

    # prepare the buttons, the horizontal lines and the spacing
    
    # Serial port configuration
    self.select_serial_box = QtGui.QComboBox()
    self.select_serial_box.addItems( self.data_source.si.getListOfSerialPorts() )
      
    # Configuration of the output plot
    self.plotname_box = QtGui.QComboBox()
    self.plotname_box.addItems( self.plot.plotnames )
    
    # select the time interval to update the plot
    labelspinbox = QtGui.QLabel("Update (ms):")
    self.spinbox_timestep = QtGui.QSpinBox()
    self.spinbox_timestep.setRange(100,2000) #from 0.1 to 5 seconds
    self.spinbox_timestep.setSingleStep(50)
    self.spinbox_timestep.setValue( self.timestep)
    labelspinbox.setBuddy(self.spinbox_timestep )
    
    # Close button
    self.save_button = QtGui.QPushButton("S&ave plot")

    # Close button
    self.close_button = QtGui.QPushButton("&Close")
    
    # in order to fix the width of the right layout
    # one needs to put the boxlayout in a widget
    vboxrightWidget = QtGui.QWidget()
    vboxright = QtGui.QVBoxLayout(vboxrightWidget)
    
    # inserting the widgets in the layout
    
    # serial configuration
    label = QtGui.QLabel("Serial configuration")
    vboxright.addWidget(label)
    vboxright.addWidget(self.select_serial_box)
    
    # horizontal line
    line = QtGui.QFrame(self)
    line.setFrameShape(QtGui.QFrame.HLine)
    line.setFrameShadow(QtGui.QFrame.Sunken)
    vboxright.addWidget(line)
    
    # plot type
    label = QtGui.QLabel("Plot type")
    vboxright.addWidget(label)
    vboxright.addWidget(self.plotname_box)
    
    # plot interval
    hbox_spinbox = QtGui.QHBoxLayout()
    hbox_spinbox.addWidget(labelspinbox)
    hbox_spinbox.addWidget(self.spinbox_timestep)
    vboxright.addLayout(hbox_spinbox)
    
    # vertical space
    vboxright.addItem(QtGui.QSpacerItem(20,40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding))
    
    # buttons
    vboxright.addWidget(self.save_button)
    vboxright.addWidget(self.close_button)
    
    #fix the width of the right layout through its enclosing widget
    vboxright.setContentsMargins(0,0,0,0)
    vboxrightWidget.setFixedWidth(150)
    
    
    
    # Global horizontal layout: takes the two vertical box layouts
    #-------------------------------------------------------------
    hboxmain = QtGui.QHBoxLayout()
    hboxmain.addLayout(vboxleft)
    hboxmain.addWidget(vboxrightWidget)
    
    # setting the global horizontal box as the main_frame layout
    #-----------------------------------------------------------
    self.main_frame.setLayout( hboxmain )
    self.setCentralWidget( self.main_frame )
    
    
  def connectSignals(self):
    """ """
    self.connect(self.play_button, QtCore.SIGNAL('clicked()'), self.play)
    self.connect(self.stop_button, QtCore.SIGNAL('clicked()'), self.stop)
    self.connect(self.close_button, QtCore.SIGNAL('clicked()'), self.close)
    self.connect(self.save_button, QtCore.SIGNAL('clicked()'), self.plot.saveplot)
    self.connect(self.timer, QtCore.SIGNAL('timeout()'), self.draw)
    

  def start_serial( self ):
    self.data_source.setPortName(self.select_serial_box.currentText())

  def play(self):
    """ This function is activated with the Play button. """
    # set the type of plot
    self.plot.plotkind = self.plotname_box.currentText()
    
    #connect the mtp interface to the data source
    self.plot.importdata( self.data_source )

    # start the serial communication
    self.start_serial()
    
    # get and set the time interval for updating the plot
    self.timestep = self.spinbox_timestep.value()
    
    #start the timer
    self.timer.start(self.timestep)
    
    #disable the various buttons
    self.play_button.setDown(True)
    self.play_button.setEnabled(False)
    self.stop_button.setEnabled(True)
    self.select_serial_box.setEnabled(False)
    self.plotname_box.setEnabled(False)
     
     
  def stop( self ):
    """ This function stop the acquisition and the update of the plot"""
    self.data_source.si.daqStop()
    self.timer.stop()
    
    #re-enable the play button
    self.play_button.setEnabled(True)
    self.stop_button.setEnabled(False)
    
  def draw(self):
    self.plot.updateplot()
    
  def __del__(self):
    del self.data_source
    del self.plot


#------------------------------------------------------------------    
def main():
  #start Qt the Qt application
  app = QtGui.QApplication(sys.argv)
  
  #create and draw the main window
  w = MainWin() 
  w.show()

  #exit when the window is closed 
  sys.exit(app.exec_())

if __name__ == '__main__':
    main()
