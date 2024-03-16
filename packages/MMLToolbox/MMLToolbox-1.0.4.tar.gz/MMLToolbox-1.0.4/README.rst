This package is a collection of usefule classes in order to help use the diffrent devices of the MML-laboratory

Welcome to MMLToolbox's documentation!
======================================

.. note::

   The package is currently under development and the documentation is adapted along with the features implemented.



PXIControl
==========

.. :py:module:: PXIControl
    :Synopsis: This class enables the user to interact with three different devices connected to a PXI-System.

.. :aurofunction:: MMLToolbox.pxi.PXIControl.connectHardware

.. :aurofunction:: MMLToolbox.pxi.PXIControl.createdmmSession

.. :aurofunction:: MMLToolbox.pxi.PXIControl.createAnalogOutputTask

.. :aurofunction:: MMLToolbox.pxi.PXIControl.createAnalogInputTask

.. :aurofunction:: MMLToolbox.pxi.PXIControl.configureDMM

.. :aurofunction:: MMLToolbox.pxi.PXIControl.addAnalogOutputChannel

.. :aurofunction:: MMLToolbox.pxi.PXIControl.addAnalogInputChannel

.. :aurofunction:: MMLToolbox.pxi.PXIControl.configureSwitch

.. :aurofunction:: MMLToolbox.pxi.PXIControl.startAnalogOutputTask

.. :aurofunction:: MMLToolbox.pxi.PXIControl.startAnalogInputTask

.. :aurofunction:: MMLToolbox.pxi.PXIControl.closeAnalogOutputTask

.. :aurofunction:: MMLToolbox.pxi.PXIControl.closeAnalogInputTask

.. :aurofunction:: MMLToolbox.pxi.PXIControl.triggerDevices

.. :aurofunction:: MMLToolbox.pxi.PXIControl.getMeasResults
    
PYCoord
=======
.. :py:module:: PYCoord
    
    :Synopsis: This class handles the communication with Feinmess devices via RS232

.. :aurofunction:: MMLToolbox.coord.Coord.PyCoord.initSystem

.. :aurofunction:: MMLToolbox.coord.Coord.PyCoord.relativePos

.. :aurofunction:: MMLToolbox.coord.Coord.PyCoord.absolutePos

.. :aurofunction:: MMLToolbox.coord.Coord.PyCoord.getPos

StoreSetup
==========


.. :py:module:: StoreSetup
   
   :Synopsis: This class can be used to store the data you get from your PXI system and also data you acquire through post-processing in an HDF5 file.

.. :aurofunction:: MMLToolbox.pxi.StoreSetup.StoreSetup.createFile

.. :aurofunction:: MMLToolbox.pxi.StoreSetup.StoreSetup.writeInfo

.. :aurofunction:: MMLToolbox.pxi.StoreSetup.StoreSetup.writeData

.. :aurofunction:: MMLToolbox.pxi.StoreSetup.StoreSetup.writeOutputSignal

.. :aurofunction:: MMLToolbox.pxi.StoreSetup.StoreSetup.writePostProcInfo

.. :aurofunction:: MMLToolbox.pxi.StoreSetup.StoreSetup.writePostProc
    
.. :aurofunction:: MMLToolbox.pxi.StoreSetup.StoreSetup.readData
    
.. :aurofunction:: MMLToolbox.pxi.StoreSetup.StoreSetup.readInfoValue

.. :aurofunction:: MMLToolbox.pxi.StoreSetup.StoreSetup.readOutputSignal

.. :aurofunction:: MMLToolbox.pxi.StoreSetup.StoreSetup.readPostProc
    