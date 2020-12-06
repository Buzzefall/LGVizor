import pyqtgraph as pg


class LabeledGraphItem(pg.GraphItem):
    def __init__(self):
        self.textItems = []
        pg.GraphItem.__init__(self)

    def setTexts(self, texts):
        for item in self.textItems:
            item.scene().removeItem(item)

        self.textItems.clear()

        for t in texts:
            item = pg.TextItem(t)
            item.setParentItem(self)
            self.textItems.append(item)

    def setData(self, **kwds):
        self.setTexts(kwds.pop('texts', []))

        for i, item in enumerate(self.textItems):
            item.setPos(*kwds['pos'][i])

        pg.GraphItem.setData(self, **kwds)
