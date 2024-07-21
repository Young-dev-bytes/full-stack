import argparse
import requests
import asyncio
import threading
import time
import pandas as pd
import numpy as np
import gradio as gr

from threading import Timer
from gradio.themes.utils import colors
from PIL import Image, ImageDraw, ImageFont


num_chatbots = 3
model_type_def = {"0": "self_develop", "1": "college", "2": "central_control"}
label_model = ["自研Agent模型", "高校Agent模型", "中控模型"]


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--private", default=False, action="store_true")
    parser.add_argument("--port", default=21001, type=int)
    parser.add_argument("--controller_host", default="0.0.0.0", type=str)
    parser.add_argument("--demo_project_name", default="demo", type=str)
    args = parser.parse_args()
    return args


def build_complicated_task_tab():
    with gr.Row():
        with gr.Column(scale=3):
            text_in = gr.Text(visible=False)
            with gr.Accordion("case 1", open=True, visible=True):
                gr.Examples(
                    examples=["打开闹钟", "今天天气怎么样?", "今天星期几?"],
                    inputs=[text_in],
                    outputs=[text_in],
                    cache_examples=False,
                )

            with gr.Accordion("case 2", open=False, visible=True):
                gr.Examples(
                    examples=[],
                    inputs=[text_in],
                    outputs=[text_in],
                    cache_examples=False,
                )

            with gr.Accordion("case 3", open=False, visible=True):
                gr.Examples(
                    examples=[],
                    inputs=[text_in],
                    outputs=[text_in],
                    cache_examples=False,
                )

        with gr.Column(scale=9):
            chat_states = [gr.State([]) for _ in range(num_chatbots)]
            model_selectors = [None] * num_chatbots
            chatbots = [None] * num_chatbots
            with gr.Row():
                for i in range(num_chatbots):
                    with gr.Column(scale=3):
                        chat_states[i] = gr.State()
                        model_selectors[i], chatbots[i] = build_single_chatbot(i)
            with gr.Row():
                with gr.Column(scale=8):
                    chat_textbox = gr.Textbox(value="", lines=5, show_label=False, visible=True)
                with gr.Column(scale=2, min_width=100):
                    submit_btn = gr.Button(value="Submit", variant="primary", visible=True)
                    clear_btn = gr.Button(value="🗑️Clear history", interactive=True)

        submit_btn.click(
            add_text,
            [chat_textbox] + model_selectors,
            chatbots,
        ).then(predict, model_selectors + chatbots + [chat_textbox], chatbots)


        clear_btn.click(fn=clear_history, inputs=chatbots, outputs=chatbots, show_progress="hidden")

        text_in.change(
            fn=text_in_change,
            inputs=text_in,
            outputs=chat_textbox,
            show_progress="hidden",
        )


def build_single_chatbot(chatbot_id):
    chatbot_id = str(chatbot_id)
    _id = gr.Textbox(visible=False, value=chatbot_id)
    gr.Markdown(f"# <h3>🕵️‍♂️{label_model[int(chatbot_id)]}</h3>")
    with gr.Group(elem_id="share-region-named" + chatbot_id):
        with gr.Row(elem_id="model_selector_row" + chatbot_id):
            model_selector = build_model_selector(chatbot_id)
            button_fresh = gr.Button("fresh", scale=1, interactive=True, visible=True)
            output_state = gr.Textbox(placeholder="请先选择模型", show_label=False, container=True, interactive=False, max_lines=3)
            model_state = gr.State("ready")

            # timer = gr.Timer(5)
            # textbox = gr.Textbox()
            # textbox2 = gr.Textbox(set_textbox_fn, inputs=[textbox], every=timer)

        with gr.Accordion(open=True, visible=True):
            with gr.Row(elem_id="model_selector_row" + chatbot_id):
                load_btn= gr.Button("加载模型", scale=3, interactive=False, size="sm")
                unload_btn= gr.Button("卸载模型", scale=3, interactive=False, size="sm")
                chat_id = gr.Text(value=chatbot_id, visible=False)

                button_fresh.click(
                    build_model_selector,
                    gr.Text(value=chatbot_id, visible=False),
                    model_selector,
                )
                output_state.change(
                    listen_output_state,
                    [model_selector, model_state, output_state],
                    [output_state, model_state, unload_btn, load_btn],
                    show_progress="hidden",
                )

                model_selector.change(listen_model_status, [model_selector], [output_state,model_state])

                load_btn.click(
                    load_model_btn_operate,
                    inputs=[model_selector],
                    outputs=[model_state, output_state, model_selector, load_btn, unload_btn],
                    show_progress="hidden",
                )
                unload_btn.click(
                    unload_model_btn_operate,
                    inputs=[model_selector],
                    outputs=[model_state, output_state, model_selector, unload_btn, load_btn],
                    show_progress="hidden",
                )        
        with gr.Accordion("对话历史", open=True, visible=True) as chatbot_row:
            chatbot = gr.Chatbot(
                elem_id="chatbot" + chatbot_id,
                elem_classes=["chatbot" + chatbot_id],
                label="Model " + chatbot_id,
                height=600,
            )
    return model_selector, chatbot


def listen_model_status(model_name):
    print("listen_model_status:")
    resp_status_load = query_model_status(model_name)["message"]
    print(resp_status_load)
    if resp_status_load == "Running":
        return ["","load_success"]
    else:
        return ["change_not_load","not_load"]


async def listen_output_state(message, model_state, output_state):
    print("listen_output_state:"+message)
    print("model_state:"+model_state)
    print("output_state:"+output_state)
    # listen_load_model_btn_status(message)

    if message == "None":
        return [
            "您还没选择模型，请选择模型",
            "",
            gr.update(interactive=False),
            gr.update(interactive=False)
        ]

    if model_state == "loading" or model_state == "unloading":
        # time.sleep(4)
        await asyncio.sleep(3)  # 非阻塞的等待

    if model_state == "loading" or model_state == "load_success":
        return [
            "模型" + message + "加载成功,正在running,服务下载模型数据可能还需几分钟。\n 请等模型数据下载成功后,再进行推理",
            "load_success",
            gr.update(interactive=True),
            gr.update(interactive=False)
        ]

    if model_state == "unloading" or model_state == "unload_success":
        return [
            "模型" + message + "卸载成功",
            "unload_success",
            gr.update(interactive=False),
            gr.update(interactive=True),
        ]

    if model_state == "not_load":
        return [
            "模型" + message + "可以加载,可点击加载模型",
            "not_load",
            gr.update(interactive=False),
            gr.update(interactive=True),
        ] 


async def load_model_btn_operate(model_name):
    resp_load_model = load_model(model_name)
    print(resp_load_model)
    if resp_load_model["message"] == "ok":
        return [
            "loading",
            "服务正在启动, 模型加载中...耐心等待",
            gr.update(interactive=False),
            gr.update(interactive=False),
            gr.update(interactive=False),
        ]
    else:
        return [
            "load_failed",
            "加载失败,请重试...",
            gr.update(interactive=True),
            gr.update(interactive=True),
            gr.update(interactive=False),
        ]

def unload_model_btn_operate(model_name):
    print("unload_model_btn_operate:")
    resp_unload_model = unload_model(model_name)
    if resp_unload_model["message"] == "ok":
        print(resp_unload_model)
        return [
            "unloading",
            "模型正在卸载...耐心等待",
            gr.update(interactive=False),
            gr.update(interactive=False),
            gr.update(interactive=False),
        ]
    else:
        return [
            "load_failed",
            "卸载失败,请重试...",
            gr.update(interactive=False),
            gr.update(interactive=True),
            gr.update(interactive=False),
        ]

def listen_load_model_btn_status(model_name):
    print("listen_load_model_btn_status:")
    count= 0
    while True:
        # await asyncio.sleep(1)  # 非阻塞的等待
        time.sleep(1)  # 非阻塞的等待
        resp_status_load = query_model_status(model_name)["message"]
        print(resp_status_load)
        count+= 1
        resp_status_load = "Pending"
        if resp_status_load == "Running":
            return [
                gr.update(value="模型加载成功", interactive=False),
                "success",
                gr.update(interactive=False),
                gr.update(interactive=False),
                gr.update(interactive=True),
            ]
        elif resp_status_load == "Pending":
            print(count)
            if count >= 5:  # 假设任务在10秒后完成
                return [
                    gr.update(value="模型加载成功", interactive=False),
                    "success",
                    gr.update(interactive=False),
                    gr.update(interactive=False),
                    gr.update(interactive=True),
                ]

def change_btn_unload(model_name, button_state):
    print("change btn unload")
    print(f"button_state: {button_state}")
    if button_state == "success":
        return [
            gr.update(value="卸载模型", interactive=True),
            "unload",
            gr.update(interactive=False),
        ]
    if button_state == "unload_success":
        return [
            gr.update(value="加载模型", interactive=True),
            "load",
            gr.update(interactive=True),
        ]

def load_model(model_name):
    print("starting load model: ")
    print(model_name)
    args = get_args()
    load_model_address = f"http://{args.controller_host}:21001/load_model"
    path = f"/root/demo/${args.demo_project_name}/yaml/{model_name}.yaml"
    # pload = {"path": "/root/demo/aicentralcontrol/yaml/web.yaml"}
    pload = {"path": path}
    # load model
    try:
        response = requests.post(load_model_address, json=pload).json()
    except:
        response = {"message": e.get}
    if "message" not in response:
        response = {"message": "error"}    
        response = {"message": "ok"}
        return response
    print(response)
    return response

def unload_model(model_name):
    print("start unload model")
    args = get_args()
    unload_model_addr = f"http://{args.controller_host}:21001/unload_model"
    # aicentralcontrol-qwen-7b-model-server-deployment
    deployment_name = f"{args.demo_project_name}-{model_name}-model-load-server-deployment"
    pload = {"deployment_name": deployment_name}
    # unload model
    try:
        response = requests.post(unload_model_addr, json=pload).json()
    except:
        response = {"message": "unload model failed"}

    print(response)

    if "message" not in response:
        response = {"message": "error"}    
        response = {"message": "ok"}
        return response
    print(response)
    return response

def query_model_status(model_name):
    print("start query model status")
    args = get_args()
    load_model_status_addr = f"http://{args.controller_host}:21001/status_model"
    # aicentralcontrol-qwen-7b-model-server-deployment
    model_name = "qwen-7b"
    deployment_name = f"{args.demo_project_name}-{model_name}-model-server-deployment"
    pload = {"deployment_name": deployment_name}
    print(deployment_name)
    # load model status
    try:
        response = requests.post(load_model_status_addr, json=pload).json()
    except:
        response = {"message": "query model status failed"}
    print(response)
    if "message" not in response:
        response = {"message": "error"}    
        # response = {"message": "Running"}
        return response
    return response

def text_in_change(text):
    return text

def clear_history(chat_history1, chat_history2, chat_history3):
    return [None, None, None]

def add_text(text, model_selector1, model_selector2, model_selector3):
    chat_history_list = [None, None, None]
    model_selectors = [model_selector1, model_selector2, model_selector3]
    # content of submit
    print(text)
    # submiting models
    print(model_selectors)

    for i in range(num_chatbots):
        if model_selectors[i] != "None":
            chat_history = [text, None, None]
            chat_history_list[i] = chat_history

    # [[['今天工作怎么样', None]], [['今天工作怎么样', None]], ""]
    print(chat_history_list)
    return chat_history_list

def predict(
    model_selector1,
    model_selectors2,
    model_selectors3,
    chat_history1,
    chat_history2,
    chat_history3,
    chat_textbox,
):
    model_selectors = [model_selector1, model_selectors2, model_selectors3]
    chat_history_list = [chat_history1, chat_history2, chat_history3]
    for i in range(num_chatbots):
        model_selected = model_selectors[i]
        if model_selected == "None":
            chat_history = [[None, None]]
        else:
            text = chat_textbox
            # ['查天气(日期=今天) THEN system.if() THEN 提醒()']
            response = predict_single_http(model_selected, text)
            chat_history = [[text, response[0]]]
            chat_history_list[i].append(chat_history[0])
    # [[['你好', 'system.if(其他条件=你好) THEN 提醒()']], [], []]
    # return [[['123','456'],['789','891']], None, None]
    return chat_history_list

def build_model_selector(chatbot_id):
    tab = ""
    model_names = ["None"]
    model_type = model_type_def[chatbot_id]
    pload = {"tab": "", "model_type": model_type}
    headers = {"Content-Type": "application/json;charset=UTF-8"}
    args = get_args()
    model_names += requests.post(
        f"http://{args.controller_host}:21001/list_models", json=pload
    ).json()["model_names"]
    print(model_names)
    model_selector = gr.Dropdown(
        choices=model_names,
        value=model_names[0],
        interactive=True,
        show_label=False,
        container=False,
        scale=2,
    )
    return model_selector

def predict_single_http(model_name, text):

    args = get_args()
    controller_address = f"http://{args.controller_host}:21001/get_worker_address"
    headers = {"User-Agent": "Demo Client"}
    pload = {"model": model_name, "text": text}
    # model server addr
    worker_addr = requests.post(controller_address, json=pload).json()["address"]
    print(worker_addr)
    try:
        # resp
        response = requests.post(
            worker_addr + "/worker_generate",
            headers=headers,
            json=pload,
            stream=False,
            timeout=10,
        ).json()
    except:
        response = "似乎卡住了，再试一下呢"
    return response
