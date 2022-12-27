import time
from pyautocad import Autocad, APoint, aDouble

from pyacadcom import AcadPoint, AutoCAD, adouble
import keyboard

# from arryautocad import Autocad, APoint, ADouble

acad = AutoCAD()

acadDoc = acad.ActiveDocument
mSp = acadDoc.ModelSpace

# flow
# Document > BlocksCollection > Block > BlockReference

# insertion point for block
ip = AcadPoint(0, 0, 0).coordinates


# adding block to documents block collection
b1 = acadDoc.Blocks.Add(ip, "Test_block_1")

# adding geometries to block
lin = 0, 0, 0, 10000, 0, 0, 10000, 5000, 0, 0, 5000, 0, 0, 0, 0

l = b1.AddLine(AcadPoint(0, 250, 0).coordinates, AcadPoint(10000, 250, 0).coordinates)
pl = b1.AddPolyline(adouble(lin))



"""#  выноска
g = 0, 0, 0, 4, 4, 0, 5, 4, 0
mtext = mSp.AddMText(APoint(4, 4, 0), 10, 'Text')
mtext.TextString = 1
mSp.AddLeader(ADouble(g), mtext, 0)"""


def coords(coord):
    g = [coord[0], coord[1], coord[2], coord[0] + 15, coord[1] + 15, coord[2]]
    return adouble(g)


j = acadDoc.Utility.GetInteger("Enter start num: ")
for i in range(1, 9):

    pt = acadDoc.Utility.GetPoint(AcadPoint(0, 0, 0).coordinates, 'GetPoint: ')
    lead = mSp.AddMLeader(coords(pt), 0)
    lead[0].TextString = j
    lead[0].TextLeftAttachmentType = 7
    j += 2
    # time.sleep(0.5)



# adding block instance to drawing (creating a reference to the block)
# block_ref1 = mSp.InsertBlock(APoint(50, 50, 0), "Test_block_1", 1, 1, 1, 0)

