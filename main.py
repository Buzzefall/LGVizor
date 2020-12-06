import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui

from LGGraph import LGGraph

pg.setConfigOptions(antialias=True)

widget = pg.GraphicsLayoutWidget(show=True)
widget.setWindowTitle('LGVizor')
widget.resize(1600, 900)

view_box = widget.addViewBox()
view_box.setAspectLocked()

graph_widget = pg.GraphItem()
view_box.addItem(graph_widget)

lg_graph = LGGraph()
lg_graph.parse_dictionary('http://langlearn.singularitynet.io//test/nlp/poc-english_5C_2018-06-06_0004.4.0.dict.txt')
pos, adj, colors, size = lg_graph.serialize(width_factor=2, height_factor=0.5)

graph_widget.setData(pos=pos, adj=adj, pen=colors, size=size, pxMode=False)

if __name__ == '__main__':
    import sys

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
