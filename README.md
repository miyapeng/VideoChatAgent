<h1>VideoChatAgent: 一个可以与视频聊天的代理</h1>

英文说明请见<a href="README.md">README.md</a>

# 介绍
VideoChatAgent 是一个多模态代理，可以理解输入视频并回答你提出的问题。你可以像与ChatGPT聊天一样与它进行视频聊天，展示代理的强大功能。

<p align="center">
<img src="imgs/teaser.png" width=90%>
</p>
在这项工作中，我使用了Agent的工作理念。此工作采用了结构：时间记忆 和 对象记忆 来存储时间和对象信息。我使用的模型是 GPT4V。

在 VideoChatAgent 中，我的设计原则是提供一组最少但足够的工具，重点是记忆查询。考虑以下工具：

- 字幕检索：给定时间记忆 $M_t$，以开始和结束时间步 $t_{start}$ 和 $t_{end}$ 作为参数，工具 caption_retrieval(·) 简单地检索这些时间步的字幕。由于上下文限制，最大允许的时间窗口为 15 段，即它偏好 $end < start + 15$。
- 片段定位：目标是根据文本查询 $s_{query}$ 定位视频片段。工具 segment_localization(·) 比较空间记忆中的特征与查询语句，考虑查询-视频相似度和查询-字幕相似度。它返回前 5 个视频片段。
- 视觉问答：此工具回答关于较短视频片段的问题，允许获取时间记忆字幕或对象记忆状态中未包含的其他信息。
- 对象记忆查询：此工具从对象记忆 $M_o$ 中对视频中出现的对象执行复杂信息检索。

给定一个视频和一个问题，VideoAgent 有两个阶段：记忆构建阶段和推理阶段。在记忆构建阶段，从视频中提取结构化信息并存储在记忆中。在推理阶段，一个大语言模型被提示使用一组工具与记忆交互以回答问题。

# 演示
我提供了一个演示供用户尝试，你可以在<a href="https://a763ce75f542f09d73.gradio.live">Demo</a>中体验。
注意：在输入完一段视频后一定要点击claer键!!!

演示视频如下：
<p align="center">
  <video width="90%" controls>
    <source src="imgs/display.mp4" type="video/mp4">
    Your browser does not support the video tag.
  </video>
</p>


有时会断开连接，因为我在服务器上运行演示。如果遇到错误，请发送电子邮件至 miyapeng78@gmail.com。

# 安装指南
使用以下命令创建名为 videochatagent 的环境。

```
conda env create -f envrionment.yaml
```

通过下面指令创建[Video-LLaVA](https://github.com/PKU-YuanGroup/Video-LLaVA)环境:
```sh
git clone https://github.com/PKU-YuanGroup/Video-LLaVA
cd Video-LLaVA
conda create -n videollava python=3.10 -y
conda activate videollava
pip install --upgrade pip  # enable PEP 660 support
pip install -e .
pip install -e ".[train]"
pip install flash-attn --no-build-isolation
pip install decord opencv-python git+https://github.com/facebookresearch/pytorchvideo.git@28fe037d212663c6a24f373b94cc5d478c8c1a1d
```

从[here](https://zenodo.org/records/11031717)下载 ```cache_dir.zip```和 ```tool_models.zip```.zip，并将它们解压到 ```VideoChatAgent``` 目录下。这将在 VideoAgent 目录下创建两个文件夹：```cache_dir```（```VideoLLaVA``` 的模型权重）和 ```tool_models```（所有其他模型的模型权重）。

# 使用方法
确保你位于 VideoAgent 目录下。
在```config/default.yaml```中输入你的 OpenAI api 密钥。
```vqa_tool```有两种选择，当你选择videollava时，你需要运行以下指令：
```sh
conda activate videollava
python video-llava.py
```
当出现```ready for connection!```时便可执行下一步，如果你vqa_tool选择gpt4v时，你无需运行上面的指令，只需运行下面的指令即可。
打开终端并运行：

```
conda activate videoagent
python demo.py
```
这将创建如下所示的 Gradio 演示。

<p align="center">
<img src="imgs/demo.png" width=90%>
</p>

你可以选择示例视频进行推理，也可以上传自己的视频和问题。一旦提交，VideoChatAgent 将开始处理你的视频，并将文件存储在```preprocess/your_video_name```下。处理输入视频后，它将回答你的问题。
结果将提供：

- 问题的答案
- 输入视频的对象重识别重播
- VideoAgent 的推理日志（思维链）

对于批量推理，你可以运行：
```
conda activate videoagent
python main.py
```