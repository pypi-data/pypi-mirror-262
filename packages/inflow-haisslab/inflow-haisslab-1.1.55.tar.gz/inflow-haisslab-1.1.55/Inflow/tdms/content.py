# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 20:03:25 2022

@author: tjostmou
"""

from nptdms import TdmsFile 
import numpy as np

def read(tdms_path,what = "data", **kwargs):
    tdms_reader = Reader(tdms_path)
    return eval(f"tdms_reader.{what}")(**kwargs)
    
class Reader(TdmsFile):
    
    def data(self,**unused_kwargs):

        tdms_data = {}
        for group in self.groups():
            dataframe = group.as_dataframe()
            tdms_data[group.name] = dataframe
        return tdms_data
    
    def properties(self):

        tdms_properties = {"root":{}}
        tdms_properties["root"].update(super().properties)
        for group in self.groups():
            tdms_properties[group.name] = {}
            tdms_properties[group.name].update(group.properties)

        return tdms_properties
        
    def data_as_trials(self,**unused_kwargs):
        return self.data(**unused_kwargs)

    def data_as_frames(self,**unused_kwargs):

        """Reads data as frames from a tdms file saved from pupil or whisker labview files.

        Returns:
            np.array : The 3D array of the video with time as first dimension, height and width as 2nd and 3rd dimensions.
        """

        tdms_data, tdms_properties = self.data(), self.properties()
        
        try : 
            tdms_properties = tdms_properties['root']
        except KeyError :
            pass
        framenb = tdms_properties["Pre_Trigger_Frames"] + tdms_properties["Post_Trigger_Frames"]
        width , height = tdms_properties["Width"] , tdms_properties["Height"]
        return np.array(tdms_data["Image"]["Image"]).reshape(framenb, height, width)
    
    def data_as_sweeps(self, groups = ['nostim_baseline_substracted','stim_baseline_substracted']):
        
        tdms_data, tdms_properties = self.data(), self.properties()
        data = {}
        for group in groups : 
            temp_images = np.flip(
                                  np.array(tdms_data[group]).reshape( 
                                                (tdms_properties[group]['frame_nb'] , 
                                                tdms_properties[group]['y_dimension'], 
                                                tdms_properties[group]['x_dimension']  
                                                )  
                                             ) 
                                     , axis = 1
                                  )
            data[group] = temp_images
        try :
            data['included_sweeps'] = np.array(tdms_data['included_sweeps']["is_included"].astype(bool))
        except KeyError :
            data['included_sweeps'] = [True for _ in groups]
        return data
    