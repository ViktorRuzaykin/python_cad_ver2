import pythoncom
import win32com.client


class Autocad:
    def __init__(self):
        self._app = None

    @property
    def app(self):
        self._app = win32com.client.GetActiveObject('AutoCAD.Application')
        return self._app

    @property
    def active_doc(self):
        return self.app.ActiveDocument

    ActiveDocument = active_doc
    Application = app

    @property
    def active_model(self):
        return self.active_doc.ModelSpace

    def prompt(self, text):
        """
        Выводит текст в консоли AutoCad
        :param text:
        :return:
        """
        print(text)
        self.active_doc.Utility.Prompt(u"%s\n" % text)

    def get_selection(self, text="Выберите объекты"):
        self.prompt(text)
        try:
            self.active_doc.SelectionSets.Item("SS1").Delete()
        except Exception:
            print('Delete selection failed')

        selection = self.active_doc.SelectionSets.Add('SS1')
        selection.SelectOnScreen()
        return selection


class APoint:
    def __new__(cls, x, y, z=0):
        return win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, (x, y, z))


class AVariant:
    def __new__(cls, vObject):
        return win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, (vObject))


class ADouble:
    def __new__(cls, xyz):
        return win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, (xyz))
