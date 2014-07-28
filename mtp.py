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
    
    self.showlasts = False
    self.showlastN = 50
    
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
      self.axes.plot( self.x, self.y, '-' )

      self.axes.set_xbound( upper=self.x[-1]+2 )
      if self.showlasts and len(self.x) > (self.showlastN+1):
        self.axes.set_xbound( self.x[-self.showlastN] )
        
    elif self.plotkind == self.plotnames[1]:
      """ Two Values plot as a function of the reading"""
      self.two()
      self.axes.clear()
      
      self.axes.plot( self.x, self.y, 'o-' )
      self.axes.plot( self.x, self.y1, 'o-' )
      
      self.axes.set_xbound( upper=self.x[-1]+2 )
      if self.showlasts and len(self.x) > (self.showlastN+1):
        self.axes.set_xbound( self.x[-self.showlastN] )

    elif self.plotkind == self.plotnames[2]:
      """ Two values scatter plot"""
      self.scatter()
      self.axes.clear()
      xx = []
      yy= []
      if self.showlasts and len(self.x) > (self.showlastN+1):
        n = len(self.x)
        l = self.showlastN
        xx = self.x[ n-l-1:n-1]
        yy = self.y[ n-l-1:n-1]
      else:
        xx = self.x
        yy = self.y

      self.axes.scatter( xx, yy )
      
    elif self.plotkind == self.plotnames[3]:
      """ Histogram """
      self.single()
      self.axes.clear()
      yy= []
      if self.showlasts and len(self.y) > (self.showlastN+1):
        n = len(self.y)
        l = self.showlastN
        yy = self.y[ n-l-1:n-1]
      else:
        yy = self.y

      self.axes.hist( yy, bins=50 )
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
        name = "plotduino_%d-%d-%d_%d%d%d.png" % ( ymdhms.year, 
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
    self.y1 = []
    self.t = 0