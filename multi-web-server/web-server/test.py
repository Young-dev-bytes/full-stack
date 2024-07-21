import gradio as gr
import time
import random

# 定义一个函数来更新按钮的状态


def update_button():
    states = ["模型未加载", "模型加载中", "模型已加载"]
    return random.choice(states)

# 创建Gradio界面
def create_interface():
    with gr.Blocks() as demo:
        button_state_test = gr.Button("模型未加载", scale=1, interactive=False)
        
        # 定义一个Timer，每隔5秒调用update_button函数，并更新按钮的值
        timer = gr.Timer(interval=5, function=update_button, outputs=button_state_test)
        
        
        # 运行Timer
        timer.run()

    return demo

if __name__ == "__main__":
    demo = create_interface()
    demo.launch()