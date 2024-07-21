"""
A model worker executes the model.
"""
import time
import argparse
import requests
import uvicorn
import threading
import logging

from constants import CONTROLLER_HEART_BEAT_EXPIRATION
from fastapi import FastAPI, Request, BackgroundTasks
from utils import build_logger
from fastapi.responses import StreamingResponse, JSONResponse


logger = build_logger("model", "model.log")

class ModelWorker:
    def __init__(self, host, port, register_host, controller_address, model_name, model_type, tab):
        self.host = host
        self.port = port
        self.register_host = register_host
        self.worker_address = f"http://{register_host}:{port}"
        self.controller_address = controller_address
        self.model_name = model_name
        self.model_type = model_type
        self.tab = tab
        self.worker_info = {
                "model_name": self.model_name,
                "worker_address": self.worker_address,
                "model_type": self.model_type,
                "tab": self.tab
            }
        self.check_register_info_to_controller()
        # threading.Thread(target=self.send_heart_beat_to_controller).start()

    def check_register_info_to_controller(self):
        url = self.controller_address + "/register_check_info"
        response = requests.post(url, json=self.worker_info)
        assert response.status_code == 200

    def generate(self, params):
        text = params['text']
        print(params)
        print(text)
        # demo modelname time 1
        curTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()+28800))
        logger.info(f"当前模型名称是：{self.model_name}，模型类型是：{self.model_type}，时间是：{curTime}")
        demo = [
            {"user": text, "assistant":""}
        ]
        return self.model.llm_predict1(demo)


app = FastAPI()

@app.post("/worker_generate")
async def generate_stream(request: Request):
    params = await request.json()
    response = model_worker.generate(params)
    return JSONResponse(response)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--model-path", type=str, default="")
    parser.add_argument("--device", type=str, default="cuda:0")
    parser.add_argument("--host", type=str, default="127.0.0.1")
    parser.add_argument("--register-host", type=str, default="127.0.0.1")
    parser.add_argument("--port", type=int, default=21002)
    parser.add_argument("--controller-address", type=str, default="http://127.0.0.1:21001")
    parser.add_argument("--model-name", type=str, default="")
    parser.add_argument("--model-type", type=str, default="")
    parser.add_argument("--tab", type=str, default="")
    

    args = parser.parse_args() 

    model_worker = ModelWorker(
        host = args.host, 
        port = args.port, 
        register_host = args.register_host,
        controller_address = args.controller_address,
        model_name = args.model_name,
        model_type = args.model_type,
        tab = args.tab)
    uvicorn.run(app, host=args.host, port=args.port, log_level="info")