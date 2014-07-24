import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from datetime import datetime

class mtp():
  def __init__(self, parent):
    self.dpi = 100
    self.fig = Figure((5.0, 4.0), dpi=self.dpi)
    self.canvas = FigureCanvas(self.fig)
    self.canvas.setParent(parent) 
    # axes, so, the actual plot
    self.axes = self.fig.add_subplot(111)
    
    self.plotnames = [ 'single', 'two', 'scatter', 'histo' ]
    self.plotkind = self.plotnames[0]
    self.x  = []
    self.y  = []
    self.y1 = []
    self.t = 0
    
  def importdata(self, data ):
    self.datasource = data
    
  def updateplot( self ):
    if not self.datasource:
      print "Error: no data"
      return
    
    if self.plotkind == self.plotnames[0]:
      """ Single Value plot as a function of the reading"""
      self.single()
      self.axes.clear()
      self.axes.plot( self.x, self.y, 'o-' )

    elif self.plotkind == self.plotnames[1]:
      """ Two Values plot as a function of the reading"""
      self.two()
      self.axes.clear()
      self.axes.plot( self.x, self.y, 'o-' )
      self.axes.plot( self.x, self.y1, 'o-' )

    elif self.plotkind == self.plotnames[2]:
      """ Two values scatter plot"""
      self.scatter()
      #self.reset()
      self.axes.clear()
      self.axes.scatter( self.x, self.y )
      
    elif self.plotkind == self.plotnames[3]:
      self.single()
      self.axes.clear()
      self.axes.hist( self.y, bins=50 )
    else:
      print "Bad selection"
    
    self.canvas.draw()
    
  def single( self ):
    values = self.datasource.getdata(1)
    self.y.append( values[0] )
    self.x.append(self.t)
    self.t += 1
    return self.x, self.y
  
  def scatter( self ):
    values = self.datasource.getdata(2)
    self.y.append( values[0] )
    self.x.append( values[1] )
    return self.x, self.y
  
  def two( self ):
    values = self.datasource.getdata(2)
    self.y.append( values[0] )
    self.y1.append( values[1] )
    self.x.append(self.t)
    self.t += 1
    return self.x, self.y
  
  def saveplot(self, name=None):
      if not name:
        ymdhms = datetime.now()
        name = "plotduino_%d-%d-%d_%d%d%d.png" % (ymdhms.year, 
                                                  ymdhms.month, 
                                                  ymdhms.day, 
                                                  ymdhms.hour,
                                                  ymdhms.minute, 
                                                  ymdhms.second )
      
      print "saving plot...", name
      try:
        self.fig.savefig( name )
      except:
        print "Exception raied saving the plot"
  
  def reset( self ):
    self.x = []
    self.y = []
    self.t = 0