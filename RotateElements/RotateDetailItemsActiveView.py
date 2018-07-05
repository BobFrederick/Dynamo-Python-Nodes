#Rotates visible detail items in view

import clr
import math

clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)

clr.AddReference('RevitAPI')
import Autodesk
from Autodesk.Revit.DB import *

clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

#get current document
doc = DocumentManager.Instance.CurrentDBDocument
#get current view
view = Document.ActiveView
#get elements in view to rotate
dtlComponent = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_DetailComponents).WhereElementIsNotElementType().ToElements()
#get input angle
angle = math.radians(IN[0])
#base point for rotation
bPoint = UnwrapElement(IN[1])
#1 create XYZ at base point
p1 = XYZ(bPoint.X,bPoint.Y,bPoint.Z)
#2 create XYZ above base point to generate line
p2 = XYZ(p1.X,p1.Y,p1.Z+1)
#3 generate line for axis
axis = Line.CreateBound(p1,p2)
# list to store moved elements
movedElements = []

#Start Revit Transaction to add to undo list
TransactionManager.Instance.EnsureInTransaction(doc)

#loop through elements to rotate and add to movedElements array for futher modification in Dynamo
for d in dtlComponent:
    Autodesk.Revit.DB.ElementTransformUtils.RotateElement(doc,d.Id,axis,angle)
    movedElements.append(d)

#Close Revit Transation
TransactionManager.Instance.TransactionTaskDone()

OUT = movedElements
