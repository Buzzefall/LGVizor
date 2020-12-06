import pyqtgraph as pg


def get_colored_pen(color, width):
    if color == 'red':
        pen = (255, 0, 0, 255, width)
    elif color == 'green':
        pen = (0, 255, 0, 255, width)
    elif color == 'blue':
        pen = (0, 0, 255, 255, width)
    else:
        pen = (255, 255, 255, 255, width)

    return pen


def prepare_qt_widget(w=800, h=600):
    pg.setConfigOptions(antialias=True)

    layout_widget = pg.GraphicsLayoutWidget(show=True)
    layout_widget.setWindowTitle('LGVizor')
    layout_widget.resize(w, h)

    view_box = layout_widget.addViewBox()
    view_box.setAspectLocked()

    graph_widget = pg.GraphItem()
    view_box.addItem(graph_widget)

    return graph_widget, layout_widget
