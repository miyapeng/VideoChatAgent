import gradio as gr
import openai
#from main import preprocess, ReActAgent
from multiprocessing import Process
import os
import socket
from omegaconf import OmegaConf

config = OmegaConf.load('config/default.yaml')
openai_api_key = config['openai_api_key']
use_reid = config['use_reid']
vqa_tool = config['vqa_tool']
base_dir = config['base_dir']

def ask_question(video_file, question):
    # preprocess(video_path_list=[video_file], 
    #            base_dir=base_dir, 
    #            show_tracking=False)
    #answer, log = ReActAgent(video_path=video_file, question=question, base_dir=base_dir, vqa_tool=vqa_tool, use_reid=use_reid, openai_api_key=openai_api_key)
    answer = "test"
    log = "test"
    base_name = os.path.basename(video_file).replace(".mp4", "")
    reid_file = os.path.join("preprocess", base_name, "reid.mp4")
    return answer, reid_file, log

def respond(chat_history, video_file, question):
    answer, reid_file, log = ask_question(video_file, question)
    chat_history.append((question,answer))
    return chat_history, reid_file, log

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column(scale=6):
            video_input = gr.Video(label="Upload a video")
            question_input = gr.Textbox(label="Ask a question about the video.")
            submit_btn = gr.Button(value="Submit")
            clear = gr.ClearButton(value="Claer")
        with gr.Column(scale=6):
            chatbot = gr.Chatbot(label="VideoChat Window")
            output_reid = gr.Video(label="Video replay with object re-identifcation")
            output_log = gr.Textbox(label="Inference log")
    submit_btn.click(respond, inputs=[chatbot, video_input, question_input], outputs=[chatbot, output_reid, output_log])
    clear.click([video_input, question_input, chatbot, output_reid, output_log])
# Create Gradio interface
demo.launch(share=True)
