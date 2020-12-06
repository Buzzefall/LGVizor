import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui

from LGGraph import LGGraph

pg.setConfigOptions(antialias=True)

widget = pg.GraphicsLayoutWidget(show=True)
widget.setWindowTitle('pyqtgraph example: GraphItem')
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














# Define positions of nodes
# pos = np.array([
#     [0, 0],
#     [10, 0],
#     [0, 10],
#     [10, 10],
#     [5, 5],
#     [15, 5]
# ])
#
# # Define the set of connections in the graph
# adj = np.array([
#     [0, 1],
#     [1, 3],
#     [3, 2],
#     [2, 0],
# ])
#
# GraphicsItem
#
# # Define the symbol to use for each node (this is optional)
# symbols = ['o', 'o', 'o', 'o', 'o', 'o']
#
# # Define the line style for each connection (this is optional)
# lines = np.array([
#     (255, 0, 0, 255, 1),
#     (255, 0, 255, 255, 2),
#     (255, 0, 255, 255, 3),
#     (0, 255, 255, 255, 2),
#     (255, 0, 0, 255, 1),
#     (255, 255, 255, 255, 4),
# ], dtype=[('red', np.ubyte), ('green', np.ubyte), ('blue', np.ubyte), ('alpha', np.ubyte), ('width', float)])

# Update the graph
# center = pos.mean(axis=0)
# np.dot(pos - center)

# for t in range(0, 10):
#     x_rot = ((pos - center)[:, 0] ** 2) * np.cos(2 * np.pi * t / 10.)
#     y_rot = ((pos - center)[:, 1] ** 2) * np.sin(2 * np.pi * t / 10.)
#     pos = center + np.stack((x_rot, y_rot), axis=1)