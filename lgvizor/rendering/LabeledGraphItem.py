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
            item = pg.TextItem(text=t, anchor=(0.5, 0))
            item.setParentItem(self)
            self.textItems.append(item)

    def setData(self, **kwargs):
        if 'texts' in kwargs:
            self.size = kwargs['size']
            self.texts = kwargs['texts']
            self.setTexts(self.texts)
            for i, item in enumerate(self.textItems):
                x, y = kwargs['pos'][i]
                item.setPos(x, y)

        pg.GraphItem.setData(self, **kwargs)
