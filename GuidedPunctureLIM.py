import os
import unittest
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
import logging
import math

#
# GuidedPunctureLIM
#

class GuidedPunctureLIM(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "GuidedPunctureLIM" # TODO make this more human readable by adding spaces
    self.parent.categories = ["Examples"]
    self.parent.dependencies = []
    self.parent.contributors = ["John Doe (AnyWare Corp.)"] # replace with "Firstname Lastname (Organization)"
    self.parent.helpText = """
    This is an example of scripted loadable module bundled in an extension.
    It performs a simple thresholding on the input volume and optionally captures a screenshot.
    """
    self.parent.acknowledgementText = """
    This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc.
    and Steve Pieper, Isomics, Inc. and was partially funded by NIH grant 3P41RR013218-12S1.
""" # replace with organization, grant and thanks.

#
# GuidedPunctureLIMWidget
#

class GuidedPunctureLIMWidget(ScriptedLoadableModuleWidget):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setup(self):
    ScriptedLoadableModuleWidget.setup(self)

    # Transform Definition Area
    transformsCollapsibleButton = ctk.ctkCollapsibleButton()
    transformsCollapsibleButton.text = "Transforms"
    self.layout.addWidget(transformsCollapsibleButton)   
    parametersFormLayout = qt.QFormLayout(transformsCollapsibleButton)
    
    # ReferenceToTracker transform selector
    self.referenceToTrackerTransformMatrix = vtk.vtkMatrix4x4()
    self.referenceToTrackerTransformMatrix.SetElement( 0, 0, 1 ) # Row 1
    self.referenceToTrackerTransformMatrix.SetElement( 0, 1, 0 )
    self.referenceToTrackerTransformMatrix.SetElement( 0, 2, 0 )
    self.referenceToTrackerTransformMatrix.SetElement( 0, 3, 0 )      
    self.referenceToTrackerTransformMatrix.SetElement( 1, 0, 0 )  # Row 2
    self.referenceToTrackerTransformMatrix.SetElement( 1, 1, 1 )
    self.referenceToTrackerTransformMatrix.SetElement( 1, 2, 0 )
    self.referenceToTrackerTransformMatrix.SetElement( 1, 3, 0 )       
    self.referenceToTrackerTransformMatrix.SetElement( 2, 0, 0 )  # Row 3
    self.referenceToTrackerTransformMatrix.SetElement( 2, 1, 0 )
    self.referenceToTrackerTransformMatrix.SetElement( 2, 2, 1 )
    self.referenceToTrackerTransformMatrix.SetElement( 2, 3, 1000 )
    self.referenceToTrackerTransform=slicer.vtkMRMLLinearTransformNode()
    self.referenceToTrackerTransform.SetName("referenceToTrackerTransform")
    self.referenceToTrackerTransform.SetMatrixTransformToParent(self.referenceToTrackerTransformMatrix)
    slicer.mrmlScene.AddNode(self.referenceToTrackerTransform)
    
    # TrackerToReference transform selector
    self.trackerToReferenceTransformMatrix = vtk.vtkMatrix4x4()
    self.trackerToReferenceTransformMatrix.SetElement( 0, 0, 1 ) # Row 1
    self.trackerToReferenceTransformMatrix.SetElement( 0, 1, 0 )
    self.trackerToReferenceTransformMatrix.SetElement( 0, 2, 0 )
    self.trackerToReferenceTransformMatrix.SetElement( 0, 3, 0 )      
    self.trackerToReferenceTransformMatrix.SetElement( 1, 0, 0 )  # Row 2
    self.trackerToReferenceTransformMatrix.SetElement( 1, 1, 1 )
    self.trackerToReferenceTransformMatrix.SetElement( 1, 2, 0 )
    self.trackerToReferenceTransformMatrix.SetElement( 1, 3, 0 )       
    self.trackerToReferenceTransformMatrix.SetElement( 2, 0, 0 )  # Row 3
    self.trackerToReferenceTransformMatrix.SetElement( 2, 1, 0 )
    self.trackerToReferenceTransformMatrix.SetElement( 2, 2, 1 )
    self.trackerToReferenceTransformMatrix.SetElement( 2, 3, 0 )
    self.trackerToReferenceTransform=slicer.vtkMRMLLinearTransformNode()
    self.trackerToReferenceTransform.SetName("trackerToReferenceTransform")
    self.trackerToReferenceTransform.SetMatrixTransformToParent(self.trackerToReferenceTransformMatrix)
    slicer.mrmlScene.AddNode(self.trackerToReferenceTransform)

    # PointerToTracker transform selector
    self.pointerToTrackerTransformMatrix = vtk.vtkMatrix4x4()
    self.pointerToTrackerTransformMatrix.SetElement( 0, 0, 1 ) # Row 1
    self.pointerToTrackerTransformMatrix.SetElement( 0, 1, 0 )
    self.pointerToTrackerTransformMatrix.SetElement( 0, 2, 0 )
    self.pointerToTrackerTransformMatrix.SetElement( 0, 3, 18 )      
    self.pointerToTrackerTransformMatrix.SetElement( 1, 0, 0 )  # Row 2
    self.pointerToTrackerTransformMatrix.SetElement( 1, 1, 0.68 )
    self.pointerToTrackerTransformMatrix.SetElement( 1, 2, -0.73 )
    self.pointerToTrackerTransformMatrix.SetElement( 1, 3, -128.08 )       
    self.pointerToTrackerTransformMatrix.SetElement( 2, 0, 0 )  # Row 3
    self.pointerToTrackerTransformMatrix.SetElement( 2, 1, 0.73 )
    self.pointerToTrackerTransformMatrix.SetElement( 2, 2, 0.68 )
    self.pointerToTrackerTransformMatrix.SetElement( 2, 3, -51.30 )
    self.pointerToTrackerTransform=slicer.vtkMRMLLinearTransformNode()
    self.pointerToTrackerTransform.SetName("pointerToTrackerTransform")
    self.pointerToTrackerTransform.SetMatrixTransformToParent(self.pointerToTrackerTransformMatrix)
    slicer.mrmlScene.AddNode(self.pointerToTrackerTransform)

    # PointerTipToPointer transform selector
    self.pointerTipToPointerTransformMatrix = vtk.vtkMatrix4x4()
    self.pointerTipToPointerTransformMatrix.SetElement( 0, 0, 1 ) # Row 1
    self.pointerTipToPointerTransformMatrix.SetElement( 0, 1, 0 )
    self.pointerTipToPointerTransformMatrix.SetElement( 0, 2, 0 )
    self.pointerTipToPointerTransformMatrix.SetElement( 0, 3, 0 )      
    self.pointerTipToPointerTransformMatrix.SetElement( 1, 0, 0 )  # Row 2
    self.pointerTipToPointerTransformMatrix.SetElement( 1, 1, 1 )
    self.pointerTipToPointerTransformMatrix.SetElement( 1, 2, 0 )
    self.pointerTipToPointerTransformMatrix.SetElement( 1, 3, 0 )       
    self.pointerTipToPointerTransformMatrix.SetElement( 2, 0, 0 )  # Row 3
    self.pointerTipToPointerTransformMatrix.SetElement( 2, 1, 0 )
    self.pointerTipToPointerTransformMatrix.SetElement( 2, 2, 1 )
    self.pointerTipToPointerTransformMatrix.SetElement( 2, 3, 0 )
    self.pointerTipToPointerTransform=slicer.vtkMRMLLinearTransformNode()
    self.pointerTipToPointerTransform.SetName("pointerTipToPointerTransform")
    self.pointerTipToPointerTransform.SetMatrixTransformToParent(self.pointerTipToPointerTransformMatrix)
    slicer.mrmlScene.AddNode(self.pointerTipToPointerTransform)

    # NeedleToTracker transform selector
    self.needleToTrackerTransformMatrix = vtk.vtkMatrix4x4()
    self.needleToTrackerTransformMatrix.SetElement( 0, 0, 1 ) # Row 1
    self.needleToTrackerTransformMatrix.SetElement( 0, 1, 0 )
    self.needleToTrackerTransformMatrix.SetElement( 0, 2, 0 )
    self.needleToTrackerTransformMatrix.SetElement( 0, 3, 0 )      
    self.needleToTrackerTransformMatrix.SetElement( 1, 0, 0 )  # Row 2
    self.needleToTrackerTransformMatrix.SetElement( 1, 1, 0.9 )
    self.needleToTrackerTransformMatrix.SetElement( 1, 2, -0.44 )
    self.needleToTrackerTransformMatrix.SetElement( 1, 3, -17.08 )       
    self.needleToTrackerTransformMatrix.SetElement( 2, 0, 0 )  # Row 3
    self.needleToTrackerTransformMatrix.SetElement( 2, 1, 0.44 )
    self.needleToTrackerTransformMatrix.SetElement( 2, 2, 0.9 )
    self.needleToTrackerTransformMatrix.SetElement( 2, 3, -8.33 )
    self.needleToTrackerTransform=slicer.vtkMRMLLinearTransformNode()
    self.needleToTrackerTransform.SetName("needleToTrackerTransform")
    self.needleToTrackerTransform.SetMatrixTransformToParent(self.needleToTrackerTransformMatrix)
    slicer.mrmlScene.AddNode(self.needleToTrackerTransform)

    # NeedleTipToNeedle transform selector
    self.needleTipToNeedleTransformMatrix = vtk.vtkMatrix4x4()
    self.needleTipToNeedleTransformMatrix.SetElement( 0, 0, 1 ) # Row 1
    self.needleTipToNeedleTransformMatrix.SetElement( 0, 1, 0 )
    self.needleTipToNeedleTransformMatrix.SetElement( 0, 2, 0 )
    self.needleTipToNeedleTransformMatrix.SetElement( 0, 3, 0 )      
    self.needleTipToNeedleTransformMatrix.SetElement( 1, 0, 0 )  # Row 2
    self.needleTipToNeedleTransformMatrix.SetElement( 1, 1, 1 )
    self.needleTipToNeedleTransformMatrix.SetElement( 1, 2, 0 )
    self.needleTipToNeedleTransformMatrix.SetElement( 1, 3, 0 )       
    self.needleTipToNeedleTransformMatrix.SetElement( 2, 0, 0 )  # Row 3
    self.needleTipToNeedleTransformMatrix.SetElement( 2, 1, 0 )
    self.needleTipToNeedleTransformMatrix.SetElement( 2, 2, 1 )
    self.needleTipToNeedleTransformMatrix.SetElement( 2, 3, 0 )
    self.needleTipToNeedleTransform=slicer.vtkMRMLLinearTransformNode()
    self.needleTipToNeedleTransform.SetName("needleTipToNeedleTransform")
    self.needleTipToNeedleTransform.SetMatrixTransformToParent(self.needleTipToNeedleTransformMatrix)
    slicer.mrmlScene.AddNode(self.needleTipToNeedleTransform)

    # PatientToReference transform selector
    self.patientToReferenceTransformMatrix = vtk.vtkMatrix4x4()
    self.patientToReferenceTransformMatrix.SetElement( 0, 0, 1 ) # Row 1
    self.patientToReferenceTransformMatrix.SetElement( 0, 1, 0 )
    self.patientToReferenceTransformMatrix.SetElement( 0, 2, 0 )
    self.patientToReferenceTransformMatrix.SetElement( 0, 3, 0 )      
    self.patientToReferenceTransformMatrix.SetElement( 1, 0, 0 )  # Row 2
    self.patientToReferenceTransformMatrix.SetElement( 1, 1, 1 )
    self.patientToReferenceTransformMatrix.SetElement( 1, 2, 0 )
    self.patientToReferenceTransformMatrix.SetElement( 1, 3, 0 )       
    self.patientToReferenceTransformMatrix.SetElement( 2, 0, 0 )  # Row 3
    self.patientToReferenceTransformMatrix.SetElement( 2, 1, 0 )
    self.patientToReferenceTransformMatrix.SetElement( 2, 2, 1 )
    self.patientToReferenceTransformMatrix.SetElement( 2, 3, 0 )
    self.patientToReferenceTransform=slicer.vtkMRMLLinearTransformNode()
    self.patientToReferenceTransform.SetName("patientToReferenceTransform")
    self.patientToReferenceTransform.SetMatrixTransformToParent(self.patientToReferenceTransformMatrix)
    slicer.mrmlScene.AddNode(self.patientToReferenceTransform)

    # Apply Transforms For Navigation Button
    self.applyTransformsForNavigationButton = qt.QPushButton("Apply Transforms For Navigation")
    self.applyTransformsForNavigationButton.toolTip = "Apply selected transforms."
    self.applyTransformsForNavigationButton.enabled = True
    parametersFormLayout.addRow(self.applyTransformsForNavigationButton)

    # Navigation Area
    navigationCollapsibleButton = ctk.ctkCollapsibleButton()
    navigationCollapsibleButton.text = "Navigation"
    self.layout.addWidget(navigationCollapsibleButton)   
    parametersFormLayout = qt.QFormLayout(navigationCollapsibleButton)

    # Soft Tissue Visibility Button
    self.softTissueVisibilityButton = qt.QPushButton()
    self.softTissueVisibilityButton.toolTip = "Apply pointer viewpoint."
    self.softTissueVisibilityButton.enabled = True
    self.softTissueVisibilityButtonState = 0
    self.softTissueVisibilityButtonStateText0 = "Make Soft Tissue Invisible"
    self.softTissueVisibilityButtonStateText1 = "Make Soft Tissue Visible"
    self.softTissueVisibilityButton.setText(self.softTissueVisibilityButtonStateText0)
    parametersFormLayout.addRow(self.softTissueVisibilityButton)

    # Bone Visibility Button
    self.boneVisibilityButton = qt.QPushButton()
    self.boneVisibilityButton.toolTip = "Apply pointer viewpoint."
    self.boneVisibilityButton.enabled = True
    self.boneVisibilityButtonState = 0
    self.boneVisibilityButtonStateText0 = "Make Bone Invisible"
    self.boneVisibilityButtonStateText1 = "Make Bone Visible"
    self.boneVisibilityButton.setText(self.boneVisibilityButtonStateText0)
    parametersFormLayout.addRow(self.boneVisibilityButton)

    # Target Fiducial selector
    self.targetFiducialSelector = slicer.qMRMLNodeComboBox()
    self.targetFiducialSelector.nodeTypes = ( ("vtkMRMLMarkupsFiducialNode"), "" )
    self.targetFiducialSelector.selectNodeUponCreation = True
    self.targetFiducialSelector.addEnabled = False
    self.targetFiducialSelector.removeEnabled = False
    self.targetFiducialSelector.noneEnabled = False
    self.targetFiducialSelector.showHidden = False
    self.targetFiducialSelector.showChildNodeTypes = False
    self.targetFiducialSelector.setMRMLScene( slicer.mrmlScene )
    self.targetFiducialSelector.setToolTip( "Pick the target fiducial." )
    parametersFormLayout.addRow("Target Fiducial: ", self.targetFiducialSelector)

    # Calculate Distance Button
    self.calculateDistanceButton = qt.QPushButton("Calculate Distance")
    self.calculateDistanceButton.enabled = True
    self.calculateDistanceButton.checkable = True
    parametersFormLayout.addRow(self.calculateDistanceButton)   

    # connections
    self.applyTransformsForNavigationButton.connect('clicked(bool)', self.onApplyTransformsForNavigationClicked)
    self.softTissueVisibilityButton.connect('clicked(bool)', self.onSoftTissueVisibilityButtonClicked)
    self.boneVisibilityButton.connect('clicked(bool)', self.onBoneVisibilityButtonClicked)
    self.calculateDistanceButton.connect('clicked(bool)', self.onCalculateDistanceClicked)
    
    # Add vertical spacer
    self.layout.addStretch(1)

    # Load models
    guidedPunctureLIMModuleDataPath = slicer.modules.guidedpuncturelim.path.replace("GuidedPunctureLIM.py","") + 'Resources/Models/'
    self.boneModel = slicer.util.getNode('BoneModel')
    if not self.boneModel:
        slicer.util.loadModel(guidedPunctureLIMModuleDataPath + 'BoneModel.stl')
        self.boneModel = slicer.util.getNode(pattern="BoneModel")
        self.boneModelDisplay=self.boneModel.GetModelDisplayNode()
        self.boneModelDisplay.SetColor([1,1,1])

    self.softTissueModel = slicer.util.getNode('SoftTissueModel')
    if not self.softTissueModel:
        slicer.util.loadModel(guidedPunctureLIMModuleDataPath + 'SoftTissueModel.stl')
        self.softTissueModel = slicer.util.getNode(pattern="SoftTissueModel")
        self.softTissueModelDisplay=self.softTissueModel.GetModelDisplayNode()
        self.softTissueModelDisplay.SetColor([1,0.7,0.53])

    self.needleModel = slicer.util.getNode('NeedleModel')
    if not self.needleModel:
        slicer.util.loadModel(guidedPunctureLIMModuleDataPath + 'NeedleModel.stl')
        self.needleModel = slicer.util.getNode(pattern="NeedleModel")
        self.needleModelDisplay=self.needleModel.GetModelDisplayNode()
        self.needleModelDisplay.SetColor([0,1,1])

    self.pointerModel = slicer.util.getNode('PointerModel')
    if not self.pointerModel:
        slicer.util.loadModel(guidedPunctureLIMModuleDataPath + 'PointerModel.stl')
        self.pointerModel = slicer.util.getNode(pattern="PointerModel")
        self.pointerModelDisplay=self.pointerModel.GetModelDisplayNode()
        self.pointerModelDisplay.SetColor([0,0,0])
    
  def cleanup(self):
    pass

  def onApplyTransformsForNavigationClicked(self):
    self.applyTransformsForNavigationButton.enabled = False
    logic = GuidedPunctureLIMLogic()
    logic.resetTransformTree(self.boneModel, self.softTissueModel, self.pointerModel, self.needleModel)
    logic.buildTransformTreeForNavigation(self.boneModel, self.softTissueModel, self.pointerModel, self.needleModel, self.referenceToTrackerTransform, self.pointerToTrackerTransform, self.pointerTipToPointerTransform, self.needleToTrackerTransform, self.needleTipToNeedleTransform, self.patientToReferenceTransform)

  def onSoftTissueVisibilityButtonClicked(self):
    if self.softTissueVisibilityButtonState == 0:
          self.softTissueModelDisplay.VisibilityOff()
          self.softTissueVisibilityButtonState = 1
          self.softTissueVisibilityButton.setText(self.softTissueVisibilityButtonStateText1)
    else: 
          self.softTissueModelDisplay.VisibilityOn()
          self.softTissueVisibilityButtonState = 0
          self.softTissueVisibilityButton.setText(self.softTissueVisibilityButtonStateText0)

  def onBoneVisibilityButtonClicked(self):
    if self.boneVisibilityButtonState == 0:
          self.boneModelDisplay.VisibilityOff()
          self.boneVisibilityButtonState = 1
          self.boneVisibilityButton.setText(self.boneVisibilityButtonStateText1)
    else: 
          self.boneModelDisplay.VisibilityOn()
          self.boneVisibilityButtonState = 0
          self.boneVisibilityButton.setText(self.boneVisibilityButtonStateText0)

  def onCalculateDistanceClicked(self):
    if self.calculateDistanceButton.checked:    
      logic = GuidedPunctureLIMLogic()
      logic.SetMembers(self.needleTipToNeedleTransform, self.needleToTrackerTransform)
      logic.addCalculateDistanceObserver()  
    elif not self.calculateDistanceButton.checked:        
      logic = GuidedPunctureLIMLogic()
      logic.removeCalculateDistanceObserver()  
#
# GuidedPunctureLIMLogic
#

class GuidedPunctureLIMLogic(ScriptedLoadableModuleLogic):
  """This class should implement all the actual
  computation done by your module.  The interface
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget.
  Uses ScriptedLoadableModuleLogic base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """
  def __init__(self):
    
    self.toolTipToTool = slicer.util.getNode('toolTipToTool')
    if not self.toolTipToTool:
      self.toolTipToTool=slicer.vtkMRMLLinearTransformNode()
      self.toolTipToTool.SetName("toolTipToTool")
      m = vtk.vtkMatrix4x4()
      m.SetElement( 0, 0, 1 ) # Row 1
      m.SetElement( 0, 1, 0 )
      m.SetElement( 0, 2, 0 )
      m.SetElement( 0, 3, 0 )      
      m.SetElement( 1, 0, 0 )  # Row 2
      m.SetElement( 1, 1, 1 )
      m.SetElement( 1, 2, 0 )
      m.SetElement( 1, 3, 0 )       
      m.SetElement( 2, 0, 0 )  # Row 3
      m.SetElement( 2, 1, 0 )
      m.SetElement( 2, 2, 1 )
      m.SetElement( 2, 3, 0 )
      self.toolTipToTool.SetMatrixTransformToParent(m)
      slicer.mrmlScene.AddNode(self.toolTipToTool)

    self.toolToReference = slicer.util.getNode('toolToReference')
    if not self.toolToReference:
      self.toolToReference=slicer.vtkMRMLLinearTransformNode()
      self.toolToReference.SetName("toolToReference")
      self.toolToReference.SetMatrixTransformToParent(m)
      slicer.mrmlScene.AddNode(self.toolToReference)
   
    self.tipFiducial = slicer.util.getNode('Tip')
    if not self.tipFiducial:
      self.tipFiducial = slicer.vtkMRMLMarkupsFiducialNode()  
      self.tipFiducial.SetName('Tip')
      self.tipFiducial.AddFiducial(0, 0, 0)
      self.tipFiducial.SetNthFiducialLabel(0, '')
      slicer.mrmlScene.AddNode(self.tipFiducial)
      self.tipFiducial.SetDisplayVisibility(True)
      self.tipFiducial.GetDisplayNode().SetGlyphType(1) # Vertex2D
      self.tipFiducial.GetDisplayNode().SetTextScale(1.3)
      self.tipFiducial.GetDisplayNode().SetSelectedColor(1,1,1)

    self.targetFiducial = slicer.util.getNode('Target')
    if not self.targetFiducial:
      self.targetFiducial = slicer.vtkMRMLMarkupsFiducialNode()  
      self.targetFiducial.SetName('Target')
      self.targetFiducial.AddFiducial(0, 0, 0)
      self.targetFiducial.SetNthFiducialLabel(0, '')
      slicer.mrmlScene.AddNode(self.targetFiducial)
      self.targetFiducial.SetDisplayVisibility(True)
      self.targetFiducial.GetDisplayNode().SetGlyphType(1) # Vertex2D
      self.targetFiducial.GetDisplayNode().SetTextScale(1.3)
      self.targetFiducial.GetDisplayNode().SetSelectedColor(1,1,1)
      
    self.line = slicer.util.getNode('Line')
    if not self.line:
      self.line = slicer.vtkMRMLModelNode()
      self.line.SetName('Line')
      linePolyData = vtk.vtkPolyData()
      self.line.SetAndObservePolyData(linePolyData)      
      modelDisplay = slicer.vtkMRMLModelDisplayNode()
      modelDisplay.SetSliceIntersectionVisibility(True)
      modelDisplay.SetColor(0,1,0)
      slicer.mrmlScene.AddNode(modelDisplay)      
      self.line.SetAndObserveDisplayNodeID(modelDisplay.GetID())      
      slicer.mrmlScene.AddNode(self.line)
      
    # VTK objects
    self.transformPolyDataFilter = vtk.vtkTransformPolyDataFilter()
    self.cellLocator = vtk.vtkCellLocator()
    
    # 3D View
    threeDWidget = slicer.app.layoutManager().threeDWidget(0)
    self.threeDView = threeDWidget.threeDView()
    
    self.callbackObserverTag = -1

  def buildTransformTreeForRegistration(self, boneModelNode, softTissueModelNode, pointerModelNode, needleModelNode, trackerToReferenceTransformNode, pointerToTrackerTransformNode, pointerTipToPointerTransformNode, needleToTrackerTransformNode, needleTipToNeedleTransformNode):
    # Pointer
    pointerModelNode.SetAndObserveTransformNodeID(pointerTipToPointerTransformNode.GetID())
    pointerTipToPointerTransformNode.SetAndObserveTransformNodeID(pointerToTrackerTransformNode.GetID())
    pointerToTrackerTransformNode.SetAndObserveTransformNodeID(trackerToReferenceTransformNode.GetID())

    # Needle
    needleModelNode.SetAndObserveTransformNodeID(needleTipToNeedleTransformNode.GetID())
    needleTipToNeedleTransformNode.SetAndObserveTransformNodeID(needleToTrackerTransformNode.GetID())

  def buildTransformTreeForNavigation (self, boneModelNode, softTissueModelNode, pointerModelNode, needleModelNode, referenceToTrackerTransformNode, pointerToTrackerTransformNode, pointerTipToPointerTransformNode, needleToTrackerTransformNode, needleTipToNeedleTransformNode, patientToReferenceTransformNode):
    # Pointer
    pointerModelNode.SetAndObserveTransformNodeID(pointerTipToPointerTransformNode.GetID())
    pointerTipToPointerTransformNode.SetAndObserveTransformNodeID(pointerToTrackerTransformNode.GetID())
    
    # Needle
    needleModelNode.SetAndObserveTransformNodeID(needleTipToNeedleTransformNode.GetID())
    needleTipToNeedleTransformNode.SetAndObserveTransformNodeID(needleToTrackerTransformNode.GetID())

    # Patient
    boneModelNode.SetAndObserveTransformNodeID(patientToReferenceTransformNode.GetID())
    softTissueModelNode.SetAndObserveTransformNodeID(patientToReferenceTransformNode.GetID())
    patientToReferenceTransformNode.SetAndObserveTransformNodeID(referenceToTrackerTransformNode.GetID())

  def resetTransformTree(self, boneModelNode, softTissueModelNode, pointerModelNode, needleModelNode):
     # Reset transform tree
    pointerModelNode.SetAndObserveTransformNodeID(None)
    needleModelNode.SetAndObserveTransformNodeID(None)
    pointerModelNode.SetAndObserveTransformNodeID(None)
    needleModelNode.SetAndObserveTransformNodeID(None)

  def SetMembers(self, toolTipToTool, toolToReference):
    self.toolTipToTool = toolTipToTool
    self.toolToReference = toolToReference
    
  def addCalculateDistanceObserver(self):
    print("[TEST] addCalculateDistanceObserver")
    if self.callbackObserverTag == -1:
      self.tipFiducial.SetAndObserveTransformNodeID(self.toolTipToTool.GetID())
      self.callbackObserverTag = self.toolToReference.AddObserver('ModifiedEvent', self.calculateCallback(self.toolTipToTool)) # slicer.vtkMRMLMarkupsNode.MarkupAddedEvent
      logging.info('addCalculateDistanceObserver')

  def removeCalculateDistanceObserver(self):
    print("[TEST] removeCalculateDistanceObserver")
    if self.callbackObserverTag != -1:
      self.toolToReference.RemoveObserver(self.callbackObserverTag)
      self.callbackObserverTag = -1
      logging.info('removeCalculateDistanceObserver')
      
  def calculateCallback(self, transformNode, event=None):
    print("[TEST] calculateCallback")
    self.calculateDistance()

  def calculateDistance(self):
    print("[TEST] calculateDistance")
    tipPoint = [0.0,0.0,0.0]
    targetPoint = [0.0, 0.0, 0.0]

    m = vtk.vtkMatrix4x4()
    self.toolTipToTool.GetMatrixTransformToWorld(m)
    tipPoint[0] = m.GetElement(0, 3)
    tipPoint[1] = m.GetElement(1, 3)
    tipPoint[2] = m.GetElement(2, 3)

    self.targetFiducial.GetNthFiducialPosition (1, targetPoint)        
    
    distance = math.sqrt(math.pow(tipPoint[0]-targetPoint[0], 2) + math.pow(tipPoint[1]-targetPoint[1], 2) + math.pow(tipPoint[2]-targetPoint[2], 2))
    
    self.drawLineBetweenPoints(tipPoint, targetPoint)
    
  def drawLineBetweenPoints(self, point1, point2):        
    # Create a vtkPoints object and store the points in it
    points = vtk.vtkPoints()
    points.InsertNextPoint(point1)
    points.InsertNextPoint(point2)

    # Create line
    line = vtk.vtkLine()
    line.GetPointIds().SetId(0,0) 
    line.GetPointIds().SetId(1,1)
    lineCellArray = vtk.vtkCellArray()
    lineCellArray.InsertNextCell(line)
    
    # Update model data
    self.line.GetPolyData().SetPoints(points)
    self.line.GetPolyData().SetLines(lineCellArray)


class GuidedPunctureLIMTest(ScriptedLoadableModuleTest):
  """
  This is the test case for your scripted module.
  Uses ScriptedLoadableModuleTest base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear(0)

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.test_GuidedPunctureLIM1()

  
