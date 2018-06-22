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

#elements in project
#get the section views
sViews = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Viewers).WhereElementIsNotElementType().ToElements()
#get the elevation views
eViews = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Elev).WhereElementIsNotElementType().ToElements()
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
movedViews = []

#Start Revit Transaction to add to undo list
TransactionManager.Instance.EnsureInTransaction(doc)

#loop through sections to rotate
for s in sViews:
    Autodesk.Revit.DB.ElementTransformUtils.RotateElement(doc,s.Id,axis,angle)
    movedViews.append(s)
for e in eViews:
    Autodesk.Revit.DB.ElementTransformUtils.RotateElement(doc,e.Id,axis,angle)
    movedViews.append(e)

#Close Revit Transation
TransactionManager.Instance.TransactionTaskDone()

OUT = movedViews


import Revit.Elements.Views as rv 
rv.AxonometricView().