

import os
import argparse
import gradio as gr
from gradio.themes.utils import colors

from tab_entity_extraction import build_complicated_task_tab

def build_event_extraction_tab():
     with gr.Row():
        gr.Markdown(
        """
            ### 多意图任务
        """)

def build_screen_comprehension_tab():
     with gr.Row():
        gr.Markdown(
        """
            ### 复杂任务
        """)  


def build_screen_comprehension_tab_():
     with gr.Row():
        gr.Markdown(
        """
            ### 多模任务
        """)               


theme=gr.themes.Soft(primary_hue=colors.gray, neutral_hue=colors.neutral)
js_func = """
function refresh() {
    const url = new URL(window.location);

    if (url.searchParams.get('__theme') !== 'dark') {
        url.searchParams.set('__theme', 'dark');
        window.location.href = url.href;
    }
}
"""



css = """
.yourclass {
    height: 50px;
    font-size: 12px;
    # background-color:red;
    # width:20px;
}
"""
with gr.Blocks(theme=theme,js=js_func, css=css) as demo:
    with gr.Tabs(elem_classes="tab-buttons") as tabs:
        with gr.TabItem("单意图任务", elem_id="chat", id=1):
            build_complicated_task_tab()

        with gr.TabItem("多意图任务", elem_id="chat", id=2):
            build_event_extraction_tab()
        
        with gr.TabItem("复杂任务", elem_id="info", id=3):
            build_screen_comprehension_tab()

        with gr.TabItem("多模任务", elem_id="info", id=4):
            build_screen_comprehension_tab_()    



demo.launch()   