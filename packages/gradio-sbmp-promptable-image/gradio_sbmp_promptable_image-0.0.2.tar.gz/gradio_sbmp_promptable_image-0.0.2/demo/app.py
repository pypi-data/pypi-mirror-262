
import gradio as gr
from gradio_sbmp_promptable_image import SBMPPromptableImage
import cv2

YELLOW = (255, 244, 79)
PURPLE = (177, 157, 217)

image_examples = [{"image": "images/cat.png", "points": []}]

def get_point_inputs(prompts):
    point_inputs = []
    for prompt in prompts:
        if prompt[2] == 1.0 and prompt[5] == 4.0:
            point_inputs.append((prompt[0], prompt[1], 1))

    return point_inputs

def get_box_inputs(prompts):
    box_inputs = []
    for prompt in prompts:
        if prompt[2] == 2.0 and prompt[5] == 3.0:
            box_inputs.append((prompt[0], prompt[1], prompt[3], prompt[4]))

    return box_inputs

def process_input(input_dict):
    img, points = input_dict['image'], input_dict['points']

    point_inputs = [(x,y) for x,y,label in get_point_inputs(points)]
    box_inputs = get_box_inputs(points)

    for point in point_inputs:
        x, y = int(point[0]), int(point[1])
        cv2.circle(img, (x, y), 2, PURPLE, thickness=10)

    for box in box_inputs:
        x1, y1, x2, y2 = int(box[0]), int(box[1]), int(box[2]), int(box[3])
        cv2.rectangle(img, (x1, y1), (x2, y2), YELLOW, 2)

    return img

demo = gr.Interface(
    process_input,
    SBMPPromptableImage(),
    gr.Image(),
    examples=image_examples,
)

if __name__ == "__main__":
    demo.launch()
