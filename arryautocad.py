import pythoncom
import win32com.client


acad = win32com.client.Dispatch('AutoCAD.Application')
acadDoc = acad.ActiveDocument
acadModel = acad.ActiveDocument.ModelSpace


def APoint(x, y, z=0):
    return win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, (x, y, z))


def aVariant(vObject):
    return win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, (vObject))


def aDouble(xyz):
    return win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, (xyz))


def prompt(text):
    """
    Выводит текст в консоли AutoCad
    :param text:
    :return:
    """
    print(text)
    acadDoc.Utility.Prompt(u"%s\n" % text)


def get_selection(text="Выберите объекты"):
    prompt(text)
    try:
        acadDoc.SelectionSets.Item("SS1").Delete()
    except Exception:
        print('Delete selection failed')

    selection = acadDoc.SelectionSets.Add('SS1')
    selection.SelectOnScreen()
    return selection

