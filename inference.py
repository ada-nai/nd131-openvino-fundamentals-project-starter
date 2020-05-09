#!/usr/bin/env python3
"""
 Copyright (c) 2018 Intel Corporation.

 Permission is hereby granted, free of charge, to any person obtaining
 a copy of this software and associated documentation files (the
 "Software"), to deal in the Software without restriction, including
 without limitation the rights to use, copy, modify, merge, publish,
 distribute, sublicense, and/or sell copies of the Software, and to
 permit persons to whom the Software is furnished to do so, subject to
 the following conditions:

 The above copyright notice and this permission notice shall be
 included in all copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
 LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
 OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
 WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import os
import sys
import logging as log
from openvino.inference_engine import IENetwork, IECore


class Network:
    """
    Load and configure inference plugins for the specified target devices 
    and performs synchronous and asynchronous modes for the specified infer requests.
    """

    def __init__(self):
        
        ### TODO: Initialize any class variables desired ###
        self.plugin = None
        self.input_blob = None
        self.output_blob = None
        self.Network = None
        self.exec_network = None
        self.infer_request = None
        
        
        

    def load_model(self, model, device= 'CPU', cpu_extension= None):
        
        ### TODO: Load the model ###
        model_xml = model
        model_bin = os.path.splitext(model_xml)[0]+'.bin'
        
        ### Initialize the plugin ###
        self.plugin = IECore()
        

        ### TODO: Add any necessary extensions ###
        if cpu_extension and "CPU" in device:
            self.plugin.add_extension(cpu_extension, device)
        
        ### TODO: Return the loaded inference plugin ###
        self.network = IENetwork(model= model_xml, weights= model_bin)
        
        
        ### TODO: Check for supported layers ###
        
        ### TODO: Get the supported layers of the network
        supported_layers = self.plugin.query_network(network= self.network, device_name="CPU")

        ### TODO: Check for any unsupported layers, and let the user
        ###       know if anything is missing. Exit the program, if so.
        unsupported_layers = [l for l in self.network.layers.keys() if l not in supported_layers]
        if len(unsupported_layers) != 0:
            log.warning("Unsupported layers found: {}".format(unsupported_layers))
              
        
        # Load network to IE
        self.exec_network = self.plugin.load_network(self.network, device)
        
        self.input_blob = next(iter(self.network.inputs))
        self.output_blob = next(iter(self.network.outputs))
            
        return

    def get_input_shape(self):
        
        ### TODO: Return the shape of the input layer ###
        return self.network.inputs[self.input_blob].shape

    def exec_net(self, image):
        
        ### TODO: Start an asynchronous request ###
        self.exec_network.start_async(request_id= 0, 
                                     inputs={self.input_blob: image})
        return

    def wait(self):
        
        ### TODO: Wait for the request to be complete. ###
        status = self.exec_network.requests[0].wait(-1)
    
        return status

    def get_output(self):
        ### TODO: Extract and return the output results
        return self.exec_network.requests[0].outputs[self.output_blob]