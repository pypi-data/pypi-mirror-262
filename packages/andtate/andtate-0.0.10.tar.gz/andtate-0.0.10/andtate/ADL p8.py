!pip install torchvision
import torch
import torchvision
import torchvision.transforms as transforms
import pycocotools
from PIL import Image
from pycocotools.coco import COCO
from torchvision.models.detection import fasterrcnn_resnet50_fpn
from torchvision.utils import draw_bounding_boxes

holiday = Image.open("kids.jpg").convert('RGB')
holiday

kids_playing = Image.open("kids.jpg").convert('RGB')
kids_playing

#holiday_tensor_int = PIL_to_tensor(holiday)
#kids_playing_tensor_int = PIL_to_tensor(kids_playing)

holiday_tensor_int = transforms.PILToTensor()(holiday)
kids_playing_tensor_int = transforms.PILToTensor()(kids_playing)
holiday_tensor_int.shape
kids_playing_tensor_int.shape

holiday_tensor_int = holiday_tensor_int.unsqueeze(dim=0)
kids_playing_tensor_int = kids_playing_tensor_int.unsqueeze(dim=0)
holiday_tensor_int.shape, kids_playing_tensor_int.shape

print(holiday_tensor_int.min(), holiday_tensor_int.max())

holiday_tensor_float = holiday_tensor_int / 255.0
kids_playing_tensor_float = kids_playing_tensor_int / 255.0
print(holiday_tensor_float.min(), holiday_tensor_float.max())

object_detection_model = fasterrcnn_resnet50_fpn(pretrained=True, progress=False)
object_detection_model.eval();
holiday_preds = object_detection_model(holiday_tensor_float)
holiday_preds

holiday_preds[0]["boxes"] = holiday_preds[0]["boxes"][holiday_preds[0]["scores"] > 0.8]
holiday_preds[0]["labels"] = holiday_preds[0]["labels"][holiday_preds[0]["scores"] > 0.8]
holiday_preds[0]["scores"] = holiday_preds[0]["scores"][holiday_preds[0]["scores"] > 0.8]
holiday_preds

kids_preds = object_detection_model(kids_playing_tensor_float)
kids_preds

#from pycocotools.coco import COCO
!wget https://huggingface.co/datasets/merve/coco/resolve/main/annotations/instances_val2017.json?download=true
!mv instances_val2017.json?download=true instances_val2017.json
annFile='/content/instances_val2017.json'
coco=COCO(annFile)
holiday_labels = coco.loadCats(holiday_preds[0]["labels"].numpy())
holiday_labels

kids_labels = coco.loadCats(kids_preds[0]["labels"].numpy())
kids_labels

holiday_annot_labels = ["{}-{:.2f}".format(label["name"], prob) for label, prob in zip(holiday_labels, holiday_preds[0]["scores"].detach().numpy())]
holiday_output = draw_bounding_boxes(image=holiday_tensor_int[0],
                                     boxes=holiday_preds[0]["boxes"],
                                     labels=holiday_annot_labels,
                                     colors=["red" if label["name"]=="person" else "green" for label in holiday_labels],
                                     width=2
)
holiday_output.shape
