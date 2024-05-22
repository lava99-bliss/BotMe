from transformers import DetrImageProcessor, DetrForObjectDetection,BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch


def detect_object(image_path):
    ##detects obj in the provided image
    image=Image.open(image_path).convert('RGB')

    processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")
    model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")

    inputs = processor(images=image, return_tensors="pt")
    outputs = model(**inputs)

    # convert outputs (bounding boxes and class logits) to COCO API
    # let's only keep detections with score > 0.9
    target_sizes = torch.tensor([image.size[::-1]])
    results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.9)[0]

    detections=""

    for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
        detections += '[{},{},{},{}]    '.format(int(box[0]),int(box[1]),int(box[2]),int(box[3]))    
        detections +='{}    '.format(model.config.id2label[int(label)])
        detections += '  {}\n'.format(float(score))

    return detections

