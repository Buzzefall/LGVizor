from pyqtgraph.Qt import QtCore, QtGui

from lgvizor.LGGraph import LGGraph
from lgvizor.helpers import prepare_qt_widget


if __name__ == '__main__':
    import sys

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        dict_url = 'http://langlearn.singularitynet.io//test/nlp/poc-english_5C_2018-06-06_0004.4.0.dict.txt'

        lg_graph = LGGraph()
        lg_graph.parse_dictionary(dict_url)
        pos, adj, colors, size = lg_graph.serialize(width_factor=2, height_factor=0.5)

        widget, view_box = prepare_qt_widget(1920, 1080)
        widget.setData(pos=pos, adj=adj, pen=colors, size=size, pxMode=False)

        QtGui.QApplication.instance().exec_()
