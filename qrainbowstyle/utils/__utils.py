from qtpy.QtWidgets import QApplication
import qrainbowstyle


def setStylesheetOnQApp(style):
    """Set stylesheet on current app."""
    app = QApplication.instance()
    app.setStyleSheet(qrainbowstyle.load_stylesheet(style=style))


class StyleLooper:
    def __init__(self):
        super(StyleLooper, self).__init__()

        self.style_index = 0
        self.styles = qrainbowstyle.getAvailableStyles()

    def change(self):
        self.style_index = self.style_index + 1
        if self.style_index >= len(self.styles):
            self.style_index = 0

        setStylesheetOnQApp(self.styles[self.style_index])
