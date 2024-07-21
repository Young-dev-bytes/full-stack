
"""
A controller manages distributed workers.
It sends worker addresses to clients.
"""

import time
import json
import asyncio
import logging
import requests
import threading
import uvicorn
import argparse
import dataclasses

from utils import build_logger
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse

app = FastAPI()

logger = build_logger("controller", "controller.log")

class Controller:

    def __init__(self):
        self.worker_info_dict = {}
        print("init")
        threading.Thread(target=self._check_works).start()

    def _check_works(self):
        print("_check_works")
        print(self.worker_info_dict)
        while True:
            print("true")
            print(self.worker_info_dict)
            del_worker = []
            for model_name in self.worker_info_dict:
                if time.time() - self.worker_info_dict[model_name]["time"] > 60:
                    del_worker.append(model_name)
            if del_worker:
                for model_name in del_worker:
                    logger.info(f"del {model_name} for {self.worker_info_dict[model_name]['tab']}")
                    del self.worker_info_dict[model_name]
            time.sleep(10)
    
    def register_worker(self, data):
        model_name = data["model_name"]
        if model_name not in self.worker_info_dict:
            data.update({'time':time.time()})
            self.worker_info_dict[model_name] = data
            logger.info(f"{model_name} register for {data['tab']}, info:{data}")
            return 'ok'
        else:
            logger.info(f"{model_name} already_existed")
            return 'already_existed'

    def register_check_info(self, data):
        model_name = data["model_name"]
        if model_name in self.worker_info_dict:
            data.update({'time':time.time()})
            self.worker_info_dict[model_name] = data
            logger.info(f"{model_name} register for {data['tab']}, info:{data}")
            return 'ok'
        else:
            logger.info(f"{model_name} not found")
            return 'not found'
        
    def heart_beat(self, data):
        model_name = data["model_name"]
        if model_name in self.worker_info_dict:
            self.worker_info_dict[model_name]["time"] = time.time()
            logger.info(f"{model_name} beat")
        else:
            self.register_worker(data)
            logger.info(f"{model_name} reregister")

    def get_address_by_name(self, model_name):
        worker_address = self.worker_info_dict[model_name]['worker_address']
        logger.info(f"get {model_name} address: {worker_address}")
        return worker_address
    
    def get_models_by_tab(self, tab):
        model_names = []
        for model_name in self.worker_info_dict:
            if tab in self.worker_info_dict[model_name]['tab']:
                model_names.append(model_name)
        logger.info(f"get {tab} model names: {model_names}")
        return model_names

    def get_models_by_type(self, model_type):
        model_names = []
        for model_name in self.worker_info_dict:
            if model_type in self.worker_info_dict[model_name]['model_type']:
                model_names.append(model_name)
        logger.info(f"get {model_type} model names: {model_names}")
        return model_names    



@app.post("/register_worker")
async def register_worker(request: Request):
    data = await request.json()
    result = controller.register_worker(data)
    return {'response': result}

@app.post("/register_check_info")
async def register_check_info(request: Request):
    data = await request.json()
    result = controller.register_check_info(data)
    return {'response': result}    

@app.post("/heart_beat")
async def heart_beat(request: Request):
    data = await request.json()
    controller.heart_beat(data)

@app.post("/list_models")
async def list_models(request: Request):
    data = await request.json()
    print(data)
    model_names = controller.get_models_by_type(data['model_type'])
    return {"model_names": model_names}

@app.post("/get_worker_address")
async def get_worker_address(request: Request):
    data = await request.json()
    addr = controller.get_address_by_name(data["model"])
    return {"address": addr}


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=int, default=21001)
    args = parser.parse_args()
    logger.info(f"args: {args}")
    controller = Controller()
    uvicorn.run(app, host=args.host, port=args.port, log_level="info")


