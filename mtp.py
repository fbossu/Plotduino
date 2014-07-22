import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure


class mtp():
  def __init__(self, parent):
    self.dpi = 100
    self.fig = Figure((5.0, 4.0), dpi=self.dpi)
    self.canvas = FigureCanvas(self.fig)
    self.canvas.setParent(parent) 
    # axes, so, the actual plot
    self.axes = self.fig.add_subplot(111)
    
    self.plotnames = [ 'single', 'two', 'scatter' ]
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
      self.single()
      self.axes.clear()
      self.axes.plot( self.x, self.y, 'o-' )

    elif self.plotkind == self.plotnames[1]:
      self.two()
      self.axes.clear()
      self.axes.plot( self.x, self.y, 'o-' )
      self.axes.plot( self.x, self.y1, 'o-' )

    elif self.plotkind == self.plotnames[2]:
      self.scatter()
      #self.reset()
      self.axes.clear()
      self.axes.plot( self.x, self.y, 'o-' )
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
  
  def reset( self ):
    self.x = []
    self.y = []
    self.t = 0