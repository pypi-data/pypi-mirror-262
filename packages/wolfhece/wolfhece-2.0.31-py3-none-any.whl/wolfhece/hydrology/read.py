import numpy as np
import os
import logging
from struct import unpack, calcsize, unpack_from


# Constants
NOT_A_FILE = -1


# Class FileIO
class FileIO:
    name:str
    directory:str
    fileTxt:str
    fileDat:str
    type:int
    updated:bool
    hasTwin:bool

    def __init__(self,filename, absPath='') -> None:
        self.name = ""
        self.directory = ""
        self.fileTxt = ""
        self.fileDat = ""
        self.type = NOT_A_FILE
        self.updated = False
        self.hasTwin = False

        # Check if the file exist and look for its pair equivalent
        isOk, name = check_path(filename, prefix=absPath)
        if not isOk:
            return

        self.name = self.get_name(name)


    def read(self):
        # Read the desired file
        return


    def get_name(self, fileName):
        # Returns the name of the file only while removing the extension and the whole path
        basename_without_ext = os.path.splitext(os.path.basename(fileName))[0]
        return basename_without_ext


    def get_directory(self, fileName):
        # Returns the path/directory of the file
        dirname = os.path.dirname(fileName)
        return dirname


    def check_format(self, fileName):
        # Determine which format it is :
        # - .dat/.bin -> binary file
        # - .txt -> if the end of the format is any
        ext = os.path.splitext(fileName)[1]
        if ext == ".dat" :
            self.fileDat = fileName
        elif ext ==".bin":
            self.fileDat = fileName
        else:
            self.fileTxt = fileName

        return

    def check_twin(self):
        # Will check if the file has a twin in txt and/or binary
        return

    def check_twin_same(self):
        # Will check if the file both twin files are the same
        return

    def update_dat2txt(self):
        # Will update the .dat file according to the .txt file
        return

    def update_txt2dat(self):
        # Will update the .txt file according to the .dat file
        return


def read_bin_old(path, fileName, nbBytes=[], uniform_format=-1, hydro=False) -> list:

    f = open(os.path.join(path,fileName), "rb")
    num = f.read(4)
    nbL = int.from_bytes(num, byteorder='little', signed=True)
    num = f.read(4)
    nbC = int.from_bytes(num, byteorder='little', signed=True)
    print("nb lines = ", nbL)
    print("nb col = ", nbC)

    if nbBytes==[]:
        if uniform_format == -1:
            nbBytes = [1,1,2,1,1,1,8]
        else:
            nbBytes = nbC * [uniform_format]

    if hydro:
        nbCol = nbC+1
    else:
        nbCol = nbC

    Data = []
    for i in range(nbL):
        Data.append([])
        for j in range(nbCol):
            if(nbBytes[j]!=8):
                numB = f.read(nbBytes[j])
                myNum = int.from_bytes(numB, byteorder='little', signed=True)
                Data[i].append(myNum)
            elif(nbBytes[j]==8):
                numB = f.read(8)
                temp = np.frombuffer(numB,dtype=np.float64)
                Data[i].append(temp[0])

    f.close()
    return Data



def read_bin(path, fileName, format="", nbBytes=[], uniform_format=-1, hydro=False, oldVersion=True) -> list:

    if not oldVersion:
        if format == "":
            format = "<bbhbbbd"

        with open(os.path.join(path,fileName), "rb") as file:
            all_bytes = file.read()
        nbL = int.from_bytes(all_bytes[:4], byteorder='little', signed=True)
        nbC = int.from_bytes(all_bytes[4:8], byteorder='little', signed=True)
        Data = unpack(format*nbL, all_bytes[8:])
    else:
        Data = read_bin_old(path, fileName, nbBytes=nbBytes, uniform_format=uniform_format, hydro=hydro)


    return Data


def read_binary_file(path, fileName, format="", buffer_size=-1, init_offset=8):

    if format == "":
        # Classical format
        format = "<bbhbbbd"
    elif "<" in format:
        logging.warning("Format should start with '<' if you are on Windows. If not, the file can be read wrongly!")

    data_size = calcsize(format)  # Size of one set of values
    values_list = []  # List to store the values



    with open(os.path.join(path,fileName), 'rb') as file:
        buffer = file.read(init_offset)
        nbL = int.from_bytes(buffer[:4], byteorder='little', signed=True)
        nbC = int.from_bytes(buffer[4:8], byteorder='little', signed=True)
        # Check the compatibility between the format and the number of columns
        nb_args = format.replace("<", "")
        if nbC != nb_args:
            logging.error("The number of column is not compatible with the number of element in format")
        if buffer_size < 0:
            buffer_size = nbL

        while True:
            buffer = file.read(buffer_size)
            if not buffer:
                break

            offset = 0
            while offset + data_size <= len(buffer):
                # Unpack values from the buffer
                values = unpack_from(format, buffer, offset)

                values_list.append(list(values))
                offset += data_size

            remaining_bytes = len(buffer) - offset
            if remaining_bytes < data_size:
                # Store the remaining bytes for the next iteration
                file.seek(offset - len(buffer), 1)
                # break

    return values_list



def is_relative_path(path:str):

    isRelativePath = False

    if len(path)>0:
        if not os.path.isabs(path):
        # if path[0] == ".":
            isRelativePath = True
    else:
        isRelativePath = None

    return isRelativePath



def relative_2_absolute(fileName:str, prefix:str="", applyCWD:bool=True)-> tuple[bool, str] :

    info = 0

    if prefix == "" :
        if applyCWD :
            # prefix = os.path.dirname(__file__)
            prefix = os.getcwd()
        else:
            logging.error("The path is relative but no prefix is given")
            info = -1
            return info

    if is_relative_path(fileName):
        finalName = os.path.join(prefix, fileName)
    else:
        logging.warning("This path is not initially a relative path!")

        info  = 1
        finalName = fileName

    return info, finalName


def check_path(fileName:str, prefix:str="", applyCWD:bool=True) -> tuple[bool, str] :

    info, finalName = relative_2_absolute(fileName, prefix, applyCWD)
    if info<0:
        info = -2
        return info

    isPresent = os.path.exists(finalName)

    if(not(isPresent)):
        logging.error("ERROR : this file or directory does not exist")
        logging.error("File name : " + finalName)
        info = -1
        return info, fileName

    return info, os.path.normpath(finalName)
