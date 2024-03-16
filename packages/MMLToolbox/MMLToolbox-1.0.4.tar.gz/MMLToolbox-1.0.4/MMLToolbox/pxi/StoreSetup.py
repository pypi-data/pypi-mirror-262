#%% Import
import h5py
import collections.abc
import re

#%% Define Class



class StoreSetup:
  """This class can be used to store the data you get from your PXI system and also data you acquire through post-processing in an HDF5 file."""

  def __init__(self, fileName: str = "") -> None:
    self.fileName = fileName


  def createFile(self) -> None:
    """This function creates an HDF5 file with the following groups:
    info: Used to give a brief description about the measurement circuit and/or specific information about the measurements.
    
    data: Used to store data acquired from the measurement. It does not matter if the data comes from the DMMs or analog inputs.
    outputSignal: Used to store the electrical signal that was used to perform the measurement.
    postProc: Used to store the data after it was processed.
    """
    with h5py.File(f"{self.fileName}.hdf5", "w") as hf:
      hf.create_group("info")
      hf.create_group("data")
      hf.create_group("outputSignal")
      hf.create_group("postProc")

  def writeInfo(self, infoData) -> None:
    """This function takes a nested dictionary and uses the keys as names for groups where it will store the connected data.

    :param infoData:  A dictionary that can contain other dictionaries or tuples. All keys in the dictionary will be used as group names.
    :type infoData: dict

    :return: None
    :rtype: None
    """

    with h5py.File(f"{self.fileName}.hdf5", "a") as hf:
      grp_info = hf["info"]

      for group_name, data in infoData.items():
        if group_name in grp_info:
          del grp_info[group_name]
        grp_name = grp_info.create_group(group_name)

        if isinstance(data, dict):
          names = list(data.keys())

          for name in names:
            items: dict = data[name]
            hfKey = grp_name.create_group(name)

            for key, item in items.items():
              self.__writeInfoEntry(hfKey,item,key)

        else:
          if isinstance(data, tuple):
            value, unit = data
            self.__writeInfoEntry(grp_name,value,"value",unit)


  def __writeInfoEntry(self,grp_name:h5py.File,value,name:str="value",unit:str="") -> None:
    if value is str:
      grp_name.create_dataset(name=name, data=value, dtype=h5py.special_dtype(vlen=str))
    else:
      grp_name.create_dataset(name=name, data=value)

    if unit != "":
      grp_name.create_dataset(name="unit", data=unit, dtype=h5py.special_dtype(vlen=str))


  def writeData(self,iter,dataName,data) -> None:
    """    This method is used to store acquired data in the HDF5 file.

    :param iter: The iteration number when performing multiple measurements.
    :type iter: int

    :param dataName: The name(s) of the data that you want to store.
    :type dataName: str or list

    :param data: The data or a 2D list of different data sets you want to store.
    :type data: list or 2D list

    :return: None
    :rtype: None
    """
    with h5py.File(f"{self.fileName}.hdf5", "a") as hf:
      grp_data = hf["data"]
      if isinstance(dataName,collections.abc.Iterable) and not isinstance(dataName,str):
        self.__writeIterable(grp_data,iter,dataName,data)
      else:
        self.__writeSingle(grp_data,iter,dataName,data)


  def writeOutputSignal(self,iter,dataName,data) -> None:
    """This method is used to store one or more output signals used to power the measurement circuit.

    :param iter: The iteration number when performing multiple measurements.
    :type iter: int

    :param dataName: The name(s) of the data that you want to store.
    :type dataName: str or list

    :param data: The data or a 2D list of different data sets you want to store.
    :type data: list or 2D list

    :return: None
    :rtype: None

    
    """
    
    with h5py.File(f"{self.fileName}.hdf5", "a") as hf:
      grp_data = hf["outputSignal"]
      if isinstance(dataName,collections.abc.Iterable) and not isinstance(dataName,str):
        self.__writeIterable(grp_data,iter,dataName,data)
      else:
        self.__writeSingle(grp_data,iter,dataName,data)


  def writePosProc(self,iter,dataName,data) -> None:
    """    This method is used to store all the processed data in the HDF5 file.

    :param iter: The iteration number when performing multiple measurements.
    :type iter: int

    :param dataName: The name(s) of the data that you want to store.
    :type dataName: str or list

    :param data: The data or a 2D list of different data sets you want to store.
    :type data: list or 2D list

    :return: None
    :rtype: None
    """
    with h5py.File(f"{self.fileName}.hdf5", "a") as hf:
      grp_postProc = hf["postProc"]

      if f"step-{iter}" in grp_postProc and dataName in grp_postProc[f"step-{iter}"]:
        del grp_postProc[f"step-{iter}"][dataName]

      if isinstance(dataName,collections.abc.Iterable) and not isinstance(dataName,str):
        self.__writeIterable(grp_postProc,iter,dataName,data)
      else:
        self.__writeSingle(grp_postProc,iter,dataName,data)


  def __writeIterable(self,grp,iter,dataName,data) -> None:
    if f"step-{int(iter)}" in grp:
      grp_name = grp[f"step-{int(iter)}"]
    else:
      grp_name = grp.create_group(f"step-{int(iter)}")

    for name, value in zip(dataName,data):
      grp_name.create_dataset(name=name, data=value)


  def __writeSingle(self,grp,iter,name,value) -> None:
    if f"step-{int(iter)}" in grp:
      grp_name = grp[f"step-{int(iter)}"]
    else:
      grp_name = grp.create_group(f"step-{int(iter)}")

    grp_name.create_dataset(name=name, data=value)

  def readData(self,iter="all",storeName="all"):
    """    This method will return either the data of a specific iteration or of all iterations. You can also choose all the available data of an iteration or only specified data.

    :param iter: (optional int) The iteration number that you want to get the data from. If no value is given, the data of all iterations will be returned.
    :type iter: int or None

    :param storeName: (optional string) The specific data you want from an iteration. If no value is given, all available data will be returned.
    :type storeName: str or None

    :return: None
    :rtype: None
    """
    with h5py.File(f"{self.fileName}.hdf5", "r") as hf:
      grp = hf["data"]
      if iter == "all":
        return self.__readIter(grp,storeName)
      else:
        return self.__readSingleIter(grp,iter,storeName)
      
  def readInfoValue(self,storeName):
    """    Returns the value of an item stored in the `info` group.

    :param storeName: The name of the item you want to get.
    :type storeName: str

    :return: None
    :rtype: None
    """
    
    with h5py.File(f"{self.fileName}.hdf5", "r") as hf:
      grp = hf[f"info/{storeName}"]
      return self.__readSingleStoreName(grp,"value")
    
  def readPostProcInfoValue(self,storeName):
    """"""
    with h5py.File(f"{self.fileName}.hdf5", "r") as hf:
      grp = hf[f"info/{storeName}"]
      return self.__readSingleStoreName(grp,"value")
      
  def readOutputSignal(self,iter="all",storeName="all"):
    """    This method will return either the output signal of a specific iteration or of all iterations. You can also choose all the available data of an iteration or only specified data.

    :param iter: (optional int) The iteration number that you want to get the data from. If no value is given, the data of all iterations will be returned.
    :type iter: int or None

    :param storeName: (optional string) The specific data you want from an iteration. If no value is given, all available data will be returned.
    :type storeName: str or None

    :return: None
    :rtype: None
    """
    
    with h5py.File(f"{self.fileName}.hdf5", "r") as hf:
      grp = hf["outputSignal"]
      if iter == "all":
        return self.__readIter(grp,storeName)
      else:
        return self.__readSingleIter(grp,iter,storeName)


  def readPostProc(self,iter="all",storeName="all"):
    """    This method will return either the processed data of a specific iteration or of all iterations. You can also choose all the available data of an iteration or only specified data.

    :param iter: (optional int) The iteration number that you want to get the data from. If no value is given, the data of all iterations will be returned.
    :type iter: int or None

    :param storeName: (optional string) The specific data you want from an iteration. If no value is given, all available data will be returned.
    :type storeName: str or None

    :return: None
    :rtype: None
    """
    with h5py.File(f"{self.fileName}.hdf5", "r") as hf:
      grp = hf["postProc"]
      if iter == "all":
        return self.__readIter(grp,storeName)
      else:
        return self.__readSingleIter(grp,iter,storeName)


  def __readIter(self,grp,storeName):
    returnDict = {}
    for iterStep in grp.keys():
      if iterStep != "info":
        grpIter = grp[iterStep]
        if storeName == "all":
          returnDict[iterStep] = self.__readStoreName(grpIter)
        else:
          returnDict[iterStep] = self.__readSingleStoreName(grpIter,storeName)

    return dict(sorted(returnDict.items(), key=lambda item: int(re.search("(\d+)",item[0]).group(1))))

  def __readSingleIter(self,grp,iter,storeName):
    grp = grp[f"step-{int(iter)}"]
    if storeName == "all":
      return self.__readStoreName(grp)
    else:
      return self.__readSingleStoreName(grp,storeName)

  def __readStoreName(self,grp):
    returnDict={}
    for storeName in grp.keys():
      returnDict[storeName] = grp[storeName][:]
    return returnDict

  def __readSingleStoreName(self,grp,storeName):
    return grp[storeName][()]
















