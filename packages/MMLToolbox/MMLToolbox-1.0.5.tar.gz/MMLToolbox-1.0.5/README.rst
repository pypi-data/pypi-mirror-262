This package is a collection of usefule classes in order to help use the diffrent devices of the MML-laboratory

Welcome to MMLToolbox's documentation!
======================================

.. note::

   The package is currently under development and the documentation is adapted along with the features implemented.


PXIControl
==========


.. :py:module:: PXIControl
   
   :Synopsis: This class enables the user to interact with three different devices connected to a PXI-System.



.. :py:function:: PXIControl.connectHardware(dmmDict = 0, analogOutDict = 0, anlaogInDict = 0, switchSlotName = 0)

   This method is used to connect to PXI devices. This method also makes sure that the provided dictionaries have the correct keys. 

   :param dmmDict: Containins all Digital multi meters that need to be configured. When using the PXIe-4081 putting its specifications on the first place inside the dictionary is recommended.
   :type dmmDict: 2D dictionary[str] or None
   
   :param analogOutDict: Contains all the output channels that need to be configured.
   :type analogOutDict: 2D dictionary[str] or None
   
   :param analogInDict: Contains all the input channels that need to be configured.
   :type analogInDict: 2D dictionary[str] or None
   
   :param switchSlotName: The switch is used to start all devices synchronously.The string clarifys on which slot the Switch is connected.
   :type switchSlotName: str or None


   :return: Nothing on succses False on Error.
   :rtype: bool


.. :py:function:: PXIControl.createdmmSession(dmmDict)

    This method will configure the DMM's according to the provided values and adds the Dictionary to a global list.

    :param dmmDict: Containins all Digital multi meters that need to be configured. 
    :type dmmDict: 2D dictionary[str]

    
.. :py:function:: PXIControl.createAnalogOutputTask(analogOutDict)

    This method makes sure that the provided dictionaries have the correct keys if they do the AO will get configured according to the provided values and adds the Dictionary to a global list.

    :param analogOutDict: Contains all the channels that need to be configured.
    :type analogOutDict: 2D dictionary[str]


.. :py:function:: PXIControl.createAnalogInputTask(analogInDict)

    This method makes sure that the provided dictionaries have the correct keys if they do the AI's will get configured according to the provided values and adds the Dictionary to a global list.

    :param analogInDict: Containins all the channels that need to be configured.
    :type analogInDict: 2D dictionary[str]

.. :py:function:: PXIControl.configureDMM(slotName,range,sF,wavePoints)

    This method is used internally by createdmmSession to connect to the specified DMM  with the provided parameters.

    :param slotName: The slot to which the DMM is connected to.
    :type slotName: str

    :param range: The expected measurement range of the DMM.
    :type range: float

    :param sF: The sample frequency the DMM should measure at.
    :type sF: int 

    :param wavePoints: How many wavepoints the DMM should measure.
    :type wavePoints: int

.. :py:function:: PXIControl.addAnalogOutputChannel(slotName, channel, minVal, maxVal)

    This Method is used internally by createAnalogOutputTask to add the channels specified by the user to the analog output task

    :param slotName: The slot to which the DAQMX-card is connected to.
    :type slotName: str

    :param channel: Which channel of the DAQMX-card should be used.
    :type channel: str

    :param minVal: Less than the minimum value the channel should output. 
    :type minVal: int

    :param maxVal: More than the maximum value the channel should output
    :type maxVal: int

        
.. :py:function:: PXIControl.addAnalogInputChannel(slotName, channel, minVal, maxVal)

    This Method is used internally by createAnalogInputTask to add the channels specified by the user to the analog input task. 

    :param slotName: The slot to which the DAQMX-card is connected to.
    :type slotName: str

    :param channel: Which channel of the DAQMX-card should be used.
    :type channel: str

    :param minVal: Less than the minimum value the channel should output. 
    :type minVal: int

    :param maxVal: More than the maximum value the channel should output
    :type maxVal: int


.. :py:function:: PXIControl.configureSwitch(slotName)

    This method is used to connect to the switch on the specified slot and configure it in a way that it sends a trigger signal on trggerline 5.

    :param slotName: The slot to which the Switch is connected to.
    :type slotName: str

.. :py:function:: PXIControl.startAnalogOutputTask(outputSignal)

    This method should only be called after connecting to the DAQMX card via connectHardware. It will start the analog output task and write the given outputsignals to the specified channels.

    :param outputSignal: Every row contains the signal of a channel.
    :type outputSignal: 2D numpy-array


.. :py:function:: PXIControl.startAnalogInputTask()

    This method should only be called after connecting to the DAQMX card via connectHardware. It will start the analog input task and will start the data acquisition on the specified channels. If switchTrigger was set to true this method does not need to be called the values can simply get retrieved from the public variable analogInResults.

    :return: Contains the obtained data each row contains all acquired data of one channel.
    :rtype: 2D numpy-array


.. :py:function:: PXIControl.closeAnalogOutputTask()   

    Closes all analog output tasks.

.. :py:function:: PXIControl.closeAnalogInputTask()   

    Closes all analog input tasks.


.. :py:function:: PXIControl.triggerDevices(output_signal = 0)

    This method should only be called after connecting DMMs and/or analog out/input channels and the switch via connectHardware. This method will start the data acquisition of all connected DMMs at the same time. Also if switchTrigger is set to true for the analog channels of the DAQMX-card, they will also be triggered synchronously. When switchTrigger is set to true for an analog output channel the method expects you to pass an output signal as a parameter in the same format as for the startAnalogOutputTask.

    :param outputSignal: Every row contains the signal of a channel.
    :type outputSignal: 2D numpy-array


.. :py:function:: PXIControl.getMeasResults()

    This method fetches all the data acquired by all the connected DMMs and closes all DMM sessions


    :return: Every row contains all measured data of one DMM.
    :rtype: 2D numpy-array
    
StoreSetup
==========


.. :py:module:: StoreSetup
   
   :Synopsis: This class can be used to store the data you get from your PXI system and also data you acquire through post-processing in an HDF5 file.




.. :py:function:: StoreSetup.createFile()

    Description:
    This function creates an HDF5 file with the following groups:
    • info: Used to give a brief description about the measurement circuit and/or specific
    information about the measurements.
    • data: Used to store data acquired from the measurement. It does not matter if
    the data comes from the DMMs or analog inputs.
    • outputSignal: Used to store the electrical signal that was used to perform the
    measurement.
    • postProc: Used to store the data after it was processed.

.. :py:function:: StoreSetup.writeInfo(infoData)

    This function takes a nested dictionary and uses the keys as names for groups where it will store the connected data.

    :param infoData:  A dictionary that can contain other dictionaries or tuples. All keys in the dictionary will be used as group names.
    :type infoData: dict

    :return: None
    :rtype: None


.. :py:function:: StoreSetup.writeData()

    This method is used to store acquired data in the HDF5 file.

    :param iter: 
        The iteration number when performing multiple measurements.
    :type iter: int

    :param dataName: 
        The name(s) of the data that you want to store.
    :type dataName: str or list

    :param data: 
        The data or a 2D list of different data sets you want to store.
    :type data: list or 2D list

    :return: None
    :rtype: None

.. :py:function:: StoreSetup.writeOutputSignal()

    This method is used to store one or more output signals used to power the measurement circuit.

    :param iter: 
        The iteration number when performing multiple measurements.
    :type iter: int

    :param dataName: 
        The name(s) of the data that you want to store.
    :type dataName: str or list

    :param data: 
        The data or a 2D list of different data sets you want to store.
    :type data: list or 2D list

    :return: None
    :rtype: None

.. :py:function:: StoreSetup.writePostProcInfo()

    This method is used to store information about the post-processing.

    :param postProcData: 
        A dictionary where each key will be used to name the connected item.
    :type postProcData: dict

    :return: None
    :rtype: None

.. :py:function:: StoreSetup.writePostProc()

    This method is used to store all the processed data in the HDF5 file.

    :param iter: 
        The iteration number when performing multiple measurements.
    :type iter: int

    :param dataName: 
        The name(s) of the data that you want to store.
    :type dataName: str or list

    :param data: 
        The data or a 2D list of different data sets you want to store.
    :type data: list or 2D list

    :return: None
    :rtype: None


.. :py:function:: StoreSetup.readData(iter=None, storeName=None)

    This method will return either the data of a specific iteration or of all iterations. You can also choose all the available data of an iteration or only specified data.

    :param iter: 
        (optional int) The iteration number that you want to get the data from. If no value is given, the data of all iterations will be returned.
    :type iter: int or None

    :param storeName: 
        (optional string) The specific data you want from an iteration. If no value is given, all available data will be returned.
    :type storeName: str or None

    :return: None
    :rtype: None

.. :py:function:: StoreSetup.readInfoValue(storeName)

    Returns the value of an item stored in the `info` group.

    :param storeName: 
        The name of the item you want to get.
    :type storeName: str

    :return: None
    :rtype: None

.. :py:function:: StoreSetup.readOutputSignal(iter=None, storeName=None)

    This method will return either the output signal of a specific iteration or of all iterations. You can also choose all the available data of an iteration or only specified data.

    :param iter: 
        (optional int) The iteration number that you want to get the data from. If no value is given, the data of all iterations will be returned.
    :type iter: int or None

    :param storeName: 
        (optional string) The specific data you want from an iteration. If no value is given, all available data will be returned.
    :type storeName: str or None

    :return: None
    :rtype: None


.. :py:function:: StoreSetup.readPostProc(iter=None, storeName=None)

    This method will return either the processed data of a specific iteration or of all iterations. You can also choose all the available data of an iteration or only specified data.

    :param iter: 
        (optional int) The iteration number that you want to get the data from. If no value is given, the data of all iterations will be returned.
    :type iter: int or None

    :param storeName: 
        (optional string) The specific data you want from an iteration. If no value is given, all available data will be returned.
    :type storeName: str or None

    :return: None
    :rtype: None

PYCoord
=======
.. :py:module:: PYCoord
    
    :Synopsis: This class handles the communication with Feinmess devices via RS232

.. :py:constructor::


.. :py::function:: PyCoord.initSystem()

    This method is used to put the system into an initial position which is always the same.

.. :py:function:: PyCoord.relativePos(x = None, y = None, z = None)

    This method moves an axis the specified amount of steps away from its current position.

    :param x: List with two elements.The first element specifies the movement speeed. The second element specifies the amount of steps you want the axis to take.
    :type x: list
    
    :param y: List with two elements.The first element specifies the movement speeed. The second element specifies the amount of steps you want the axis to take.
    :type x: list

    :param z: List with two elements.The first element specifies the movement speeed. The second element specifies the amount of steps you want the axis to take.
    :type x: list

.. :py:function:: PyCoord.absolutePos(x = None, y = None, z = None)

    This method moves an axis to an absolute position in the coordinate system of the Feinmess system.

    :param x: List with two elements.The first element specifies the movement speeed. The second element specifies the absolute position you want the axis to endup.
    :type x: list
    
    :param y: List with two elements.The first element specifies the movement speeed. The second element specifies the absolute position you want the axis to endup.
    :type x: list

    :param z: List with two elements.The first element specifies the movement speeed. The second element specifies the absolute position you want the axis to endup.
    :type x: list

.. :py:function:: PyCoord.getPos()

    This method returns the current position of all connected axis.

    :return: A list every element holds the current position of an axis in alphabetical order.
    :rtype: list
