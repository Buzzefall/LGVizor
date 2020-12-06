from pyqtgraph.Qt import QtCore, QtGui

from lgvizor.data.LinkGrammarGraph import LinkGrammarGraph
from lgvizor.rendering.helpers import prepare_qt_widget

if __name__ == '__main__':
    import sys

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        dict_url = 'http://langlearn.singularitynet.io//test/nlp/poc-english_5C_2018-06-06_0004.4.0.dict.txt'

        lg_graph = LinkGrammarGraph()
        lg_graph.parse_dictionary(dict_url)
        pos, adj, colors, size, texts = lg_graph.serialize(width_factor=5, height_factor=1)

        graph_widget, layout_widget = prepare_qt_widget(1920, 1080)
        graph_widget.setData(pos=pos, adj=adj, pen=colors, size=size, pxMode=False, texts=texts)

        QtGui.QApplication.instance().exec_()
