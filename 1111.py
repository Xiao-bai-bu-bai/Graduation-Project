import torch
import gradio as gr

model = torch.hub.load("./", "custom", "runs/train/exp7/weights/best.pt", source="local")

description = "这是一个基于YOLOv5的口罩检测系统，可以检测图片中的人脸是否佩戴口罩。"

base_conf, base_iou = 0.25, 0.45


def det_image(img, conf, iou):
    model.conf = conf
    model.iou = iou
    return model(img).render()[0]


gr.Interface(
    inputs=[gr.Image(sources=['upload', 'webcam']), gr.Slider(minimum=0, maximum=1, value=base_conf),
            gr.Slider(minimum=0, maximum=1, value=base_iou)],
    outputs=gr.Image(),
    fn=det_image,
    description=description,
    examples=[["./VOCdevkit/images/train/1_Handshaking_Handshaking_1_65.jpg", base_conf, base_iou],
              ["./VOCdevkit/images/train/test_00004346.jpg", base_conf, base_iou], ]
    ).launch()


