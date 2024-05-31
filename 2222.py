import torch
import gradio as gr

model_path = "./runs/train/exp7/weights/best.pt"
model = torch.hub.load("./", "custom", model_path, source="local")


description = "这是一个基于YOLOv5的口罩检测系统，可以检测摄像头实时视频中的人脸是否佩戴口罩。"
base_conf, base_iou = 0.25, 0.45


def det_camera(camera, conf, iou):
    model.conf = conf
    model.iou = iou
    return model(camera).render()[0]


gr.Interface(
    inputs=[gr.Image(streaming=True), gr.Slider(minimum=0, maximum=1, value=base_conf),
            gr.Slider(minimum=0, maximum=1, value=base_iou)],
    outputs=gr.Image(),
    fn=det_camera,
    description=description,
    live=True,
).launch()