import logging
import os

import vtk
import numpy as np
import sys

import slicer, vtk, qt, SampleData
from slicer.ScriptedLoadableModule import *
from slicer.util import *

# <-------------------------------------------->
import vtkmodules.vtkInteractionStyle
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkFiltersCore import vtkTubeFilter
from vtkmodules.vtkFiltersSources import vtkLineSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)

#%%
#
# AnotherModule (Deep Brain Stimulation Project)
#

class AnotherModule(ScriptedLoadableModule):
    """Uses ScriptedLoadableModule base class, available at:
    https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def __init__(self, parent):
        ScriptedLoadableModule.__init__(self, parent)
        self.parent.title = "AnotherModule"  # TODO: make this more human readable by adding spaces
        self.parent.categories = ["Examples"]  # TODO: set categories (folders where the module shows up in the module selector)
        self.parent.dependencies = []  # TODO: add here list of module names that this module requires
        self.parent.contributors = ["Caroline Essert (University of Strasbourg), Mubarak Olaoluwa (Master Student)"]  # TODO: replace with "Firstname Lastname (Organization)"
        # TODO: update with short description of the module and a link to online module documentation
        self.parent.helpText = """
            This is an example of scripted loadable module bundled in an extension.
            See more information in <a href="https://github.com/organization/projectname#AnotherModule">module documentation</a>.
            """
        # TODO: replace with organization, grant and thanks
        self.parent.acknowledgementText = """
            This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc., Andras Lasso, PerkLab,
            and Steve Pieper, Isomics, Inc. and was partially funded by NIH grant 3P41RR013218-12S1.
            """

#%%
#
# AnotherModuleWidget (Deep Brain Stimulation Project)
#

class AnotherModuleWidget(ScriptedLoadableModuleWidget, VTKObservationMixin):
    """Uses ScriptedLoadableModuleWidget base class, available at:
    https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def __init__(self, parent=None):
        """
        Called when the user opens the module the first time and the widget is initialized.
        """
        ScriptedLoadableModuleWidget.__init__(self, parent)
        VTKObservationMixin.__init__(self)  # needed for parameter node observation
        # store logic in a member variable
        self.logic = AnotherModuleLogic()


    def setup(self):
        """
        Called when the user opens the module the first time and the widget is initialized.
        """
        # <<<< initialisation that needs to be here - don't remove >>>>
        ScriptedLoadableModuleWidget.setup(self)

        # <<<< Create Cylinder button  >>>>
        CreateCylinderButton = qt.QPushButton("Create Cylinder")
        self.layout.addWidget(CreateCylinderButton)
        CreateCylinderButton.connect('clicked(bool)', self.onCreateCylinderButtonClicked)

        # <<<< Locate the nuclues button >>>>
        CreateNucleusButton = qt.QPushButton("Locate the Nucleus")
        self.layout.addWidget(CreateNucleusButton)
        CreateNucleusButton.connect('clicked(bool)', self.onLocateNucleusButtonClicked)

        # <<<< Place ELectrodes button >>>>
        PlaceElectrodesButton = qt.QPushButton("Place Electrodes")
        self.layout.addWidget(PlaceElectrodesButton)
        PlaceElectrodesButton.connect('clicked(bool)', self.onPlaceElectrodesButtonClicked)

        # <<<< Compute Distance button >>>>
        distanceButton = qt.QPushButton("Compute Distance")
        self.layout.addWidget(distanceButton)
        distanceButton.connect('clicked(bool)', self.onDistanceButtonClicked)

        # <<<< Remove Added nodes button >>>>
        distanceButton = qt.QPushButton("Remove Added Nodes")
        self.layout.addWidget(distanceButton)
        distanceButton.connect('clicked(bool)', self.onRemoveButtonClicked)
        
        
    # <<<< Create Cylinder button callback function >>>>
    def onCreateCylinderButtonClicked(self):
        self.logic.createCylinder()

    # <<<< Locate the Nucleus button callback function >>>>
    def onLocateNucleusButtonClicked(self):
        self.logic.LocateNucleusButton()

    # <<<< PLace Electrodes button callback function >>>>
    def onPlaceElectrodesButtonClicked(self):
        self.logic.placeElectrodes()

    # <<<< Compute Distance button callback function >>>>
    def onDistanceButtonClicked(self):
        self.logic.computeDistance()

    # <<<< Compute Distance button callback function >>>>
    def onRemoveButtonClicked(self):
        self.logic.removeNodesButton()
        
  
#%%
#
# AnotherModuleLogic (Deep Brain Stimulation Project)
#

class AnotherModuleLogic(ScriptedLoadableModuleLogic):
    """This class should implement all the actual
    computation done by your module.  The interface
    should be such that other python code can import
    this class and make use of the functionality without
    requiring an instance of the Widget.
    Uses ScriptedLoadableModuleLogic base class, available at:
    https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def __init__(self):
        """
        Called when the logic class is instantiated. Can be used for initializing member variables.
        """
        ScriptedLoadableModuleLogic.__init__(self)
        
    def createCylinder(self, caller=None, event=None): 
        try:
            # <<< Creating the first Fiducial node of the cylinder >>>
            markupsNodeID = slicer.modules.markups.logic().AddNewFiducialNode()
            markupsNode = getNode(markupsNodeID)
            markupsNode.SetName('F')
            markupsNode.AddControlPoint(50.0,50.0,50.0)
            self.f = getNode('F')
            self.pos=[0,0,0]
            self.f.GetNthControlPointPosition(0,self.pos)
            modelDisplay = self.f.GetDisplayNode()
            modelDisplay.SetGlyphScale(3.0)
            #print(self.pos)
            
            # <<< Creating the second Fiducial node of the cylinder >>>
            markupsNodeID_2 = slicer.modules.markups.logic().AddNewFiducialNode()
            markupsNode_2 = getNode(markupsNodeID_2)
            markupsNode_2.SetName('F2')
            markupsNode_2.AddControlPoint(50.0,200.0,50.0)
            self.f2 = getNode('F2')
            self.pos2=[0,0,0]
            self.f2.GetNthControlPointPosition(0,self.pos2)
            modelDisplay2 = self.f2.GetDisplayNode()
            modelDisplay2.SetGlyphScale(3.0)
            #print(self.pos2)
            
            # <<< Create the vtkLineSource for the Cylinder >>>
            self.lineSource = vtk.vtkLineSource()
            self.lineSource.SetPoint1(self.pos[0],self.pos[1],self.pos[2])
            self.lineSource.SetPoint2(self.pos2[0],self.pos2[1],self.pos2[2])

            # <<< Create a tube filter >>>
            self.tubeFilter = vtk.vtkTubeFilter()
            self.tubeFilter.SetInputConnection(self.lineSource.GetOutputPort())
            self.tubeFilter.SetRadius(1)
            self.tubeFilter.SetNumberOfSides(50)
            self.tubeFilter.Update()
            self.tube = self.tubeFilter.GetOutputPort()
            slicer.modules.models.logic().AddModel(self.tube)

            self.modelDisplayTube = slicer.modules.models.logic().AddModel(self.tube)
            modelDisplayTubeD = self.modelDisplayTube.GetDisplayNode()
            modelDisplayTubeD.SetColor(0,0,1)
            modelDisplayTubeD.SetRepresentation(slicer.vtkMRMLDisplayNode.WireframeRepresentation)
            modelDisplayTubeD.SetOpacity(0.2)

        except slicer.util.MRMLNodeNotFoundException:
            print("Unable to Create Cylinder")

        # <<< Observer for updating the vtkLinesource function >>>
        self.f.AddObserver(slicer.vtkMRMLMarkupsNode.PointModifiedEvent, self.update)
        self.f2.AddObserver(slicer.vtkMRMLMarkupsNode.PointModifiedEvent, self.update)

        # <<< Observer for updating the distance when F-2 is moved >>>
        self.f.AddObserver(slicer.vtkMRMLMarkupsNode.PointModifiedEvent, self.updateDistance)
        self.f2.AddObserver(slicer.vtkMRMLMarkupsNode.PointModifiedEvent, self.updateDistance)

    def LocateNucleusButton(self, caller=None, event=None):
    # <<< Creating another Fiducial node (F-3) for locating the Nucleus >>>
        self.electrodeNodeID = slicer.modules.markups.logic().AddNewFiducialNode()
        self.electrodeNode = getNode(self.electrodeNodeID)
        self.electrodeNode.SetName('F3')
        self.electrodeNode.AddControlPoint(0.0,0.0,100.0)
        self.electNode = getNode('F3')
        self.electNodePos=[0,0,0]
        self.electNode.GetNthControlPointPosition(0,self.electNodePos)
        self.electNodeDisplay = self.electNode.GetDisplayNode()
        self.electNodeDisplay.SetGlyphScale(3.0)
        #print(self.electNodePos)        

    # <<< vtkLinesource Update function >>>
    def update(self, caller=None, event=None):
        self.f.GetNthControlPointPosition(0,self.pos)
        self.f2.GetNthControlPointPosition(0,self.pos2)

        self.lineSource.SetPoint1(self.pos[0],self.pos[1],self.pos[2])
        self.lineSource.SetPoint2(self.pos2[0],self.pos2[1],self.pos2[2])

        self.tubeFilter.SetInputConnection(self.lineSource.GetOutputPort())
        self.tubeFilter.Update()

    """
    <<< Placing the electrode on the STN function >>>
    <<< This function gets the position of F-3 when placed on the STN and update this position on F-1 to extend F-1 to STN  >>>
    """
    def placeElectrodes(self, caller=None, event=None):
        try:
            self.electNode = getNode('F3')
            self.electNodePos=[0,0,0]
            self.electNode.GetNthControlPointPosition(0,self.electNodePos)

            self.f = getNode('F')
            self.pos=[0,0,0]
            self.f.SetNthControlPointPosition(0,self.electNodePos)
            modelDisplay = self.f.GetDisplayNode()
            modelDisplay.SetGlyphScale(3.0)

            slicer.mrmlScene.RemoveNode(self.electNode)

        except slicer.util.MRMLNodeNotFoundException:
            print("Please create a cylinder first")
            print(3 * "\n")
             
    # <<< Callback Function for updating the distance when the cylinder is moved>>>
    def updateDistance(self, caller=None, event=None):
         # <<< Loading the ventricles >>>
        lat_vent_1 = slicer.mrmlScene.GetFirstNodeByName('63_lateral_ventricle_left.vtk')
        lat_vent_2 = slicer.mrmlScene.GetFirstNodeByName('63_lateral_ventricle_right.vtk')
        third_vent = slicer.mrmlScene.GetFirstNodeByName('63_third_ventricle.vtk')
        fourth_vent = slicer.mrmlScene.GetFirstNodeByName('63_fourth_ventricle.vtk')

        # <<< Create an array list for the ventricles and an empty list to store the minimum distance for each of the ventricles >>> 
        vent_arr = [lat_vent_1, lat_vent_2, third_vent, fourth_vent]
        self.distance_vent_list = []

        # <<< Looping through the ventricles to calculate the minimum distance for each >>>
        for i in range(4):

            # <<< Applying vtkTriangleFilter at the Tubefilter Output. This is necessary to calculate the distance using vtkPolyDataFilter >>> 
            self.a = vtk.vtkTriangleFilter()
            self.a.SetInputConnection(self.tube)
            self.a.Update()
            self.b = self.a.GetOutputPort()
            self.addTri = slicer.modules.models.logic().AddModel(self.b)

            # <<< Getting the VtkPolyData of the ventricle Model and the TriangleFilter Model >>>
            lat_vent_polyData = vent_arr[i].GetPolyData()
            tri_polyData = self.addTri.GetPolyData()

            # <<< Computing the mimimum distance >>>
            distance = vtk.vtkDistancePolyDataFilter()
            distance.SignedDistanceOff()
            distance.SetInputData(0, lat_vent_polyData)
            distance.SetInputData(1, tri_polyData)
            distance.ComputeSecondDistanceOn()
            distance.Update()
            #print(distance_1.GetOutput())

            self.distance = (np.min(distance.GetOutput().GetPointData().GetArray('Distance')))
            self.distance_vent_list.append(self.distance)
            #print(np.asarray(distance_1.GetOutput().GetPointData().GetArray('Distance')))
        
        # <<<<<<<< For Sulci >>>>>>>> 
        # <<< Loading the sulci >>>
        sulci_1= slicer.mrmlScene.GetFirstNodeByName('63_sulci_left.vtk')
        sulci_2= slicer.mrmlScene.GetFirstNodeByName('63_sulci_right.vtk')

        # <<< Create an array list for the sulci and an empty list to store the minimum distance for each of them >>> 
        sul_arr = [sulci_1, sulci_2]
        self.distance_sul_list = []

        # <<< Looping through the sulci to calculate the minimum distance for each >>>
        for i in range(2):

            # <<< Applying vtkTriangleFilter at the Tubefilter Output. This is necessary to calculate the distance using vtkPolyDataFilter >>> 
            self.a = vtk.vtkTriangleFilter()
            self.a.SetInputConnection(self.tube)
            self.a.Update()
            self.b = self.a.GetOutputPort()
            self.addTri = slicer.modules.models.logic().AddModel(self.b)

            # <<< Getting the VtkPolyData of the ventricle Model and the TriangleFilter Model >>>
            sulci_polyData = sul_arr[i].GetPolyData()
            tri_polyData = self.addTri.GetPolyData()

            # <<< Computing the mimimum distance >>>
            distance = vtk.vtkDistancePolyDataFilter()
            distance.SignedDistanceOff()
            distance.SetInputData(0, sulci_polyData)
            distance.SetInputData(1, tri_polyData)
            distance.ComputeSecondDistanceOn()
            distance.Update()
            #print(distance_1.GetOutput())

            self.distance = (np.min(distance.GetOutput().GetPointData().GetArray('Distance')))
            self.distance_sul_list.append(self.distance)
            #print(np.asarray(distance_1.GetOutput().GetPointData().GetArray('Distance')))


    # <<< For Computing the distance when the Compute Distance Button is Clicked
    def computeDistance(self, caller=None, event=None):
        try:
            self.updateDistance()
            #print(self.distance_list)
            print("Distance to Ventricles")
            print(np.min(self.distance_vent_list))
            
            print("Distance to Sulci")
            print(np.min(self.distance_sul_list))
            print(3 * "\n")

        except:
            print("Please create a cylinder first")
            print(3 * "\n")


    # <<< Remove Added Nodes Button >>>
    def removeNodesButton(self):
        try:
            slicer.mrmlScene.RemoveNode(self.f)
            slicer.mrmlScene.RemoveNode(self.f2)
            #slicer.mrmlScene.Clear()
        except:
            print("No Nodes to be removed")
            print(3 * "\n")
        
#%%
#
# AnotherModuleTest(Deep Brain Stimulation Project)
#

class AnotherModuleTest(ScriptedLoadableModuleTest):
    """
    This is the test case for your scripted module.
    Uses ScriptedLoadableModuleTest base class, available at:
    https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def setUp(self):
        """ Do whatever is needed to reset the state - typically a scene clear will be enough.
        """

    def runTest(self):
        """Run as few or as many tests as needed here.
        """
        self.setUp()
        self.test_AnotherModule1()

    def test_AnotherModule1(self):
        """ Ideally you should have several levels of tests.  At the lowest level
        tests should exercise the functionality of the logic with different inputs
        (both valid and invalid).  At higher levels your tests should emulate the
        way the user would interact with your code and confirm that it still works
        the way you intended.
        One of the most important features of the tests is that it should alert other
        developers when their changes will have an impact on the behavior of your
        module.  For example, if a developer removes a feature that you depend on,
        your test should break so they know that the feature is needed.
        """

        # quick message box to inform that the test is starting
        self.delayDisplay("Starting the test")

        # get the logic
        logic = AnotherModuleLogic()
        
        # quick message box to inform that the test has successfully ended
        self.delayDisplay('Test passed')
    