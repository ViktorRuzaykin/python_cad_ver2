import pythoncom
from pyautocad import Autocad, APoint, aDouble
import win32com.client

acad = win32com.client.Dispatch('AutoCAD.Application')
acadModel = acad.ActiveDocument.ModelSpace


def APoint(x, y, z=0):
    return win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, (x, y, z))


def aVariant(vObject):
    return win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_DISPATCH, (vObject))


def aDouble(xyz):
    return win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, (xyz))


c = acadModel.AddCircle(APoint(0, 0), 2)
pl = acadModel.AddPolyline(aDouble([0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0]))
pl.Color = 5
limiteExterior = []
limiteExterior.append(c)
limiteExterior = aVariant(limiteExterior)

hatch = acadModel.AddHatch(0, 'SOLID', True)
hatch.Color = 32
hatch.AppendOuterLoop(limiteExterior)
hatch.Evaluate()
