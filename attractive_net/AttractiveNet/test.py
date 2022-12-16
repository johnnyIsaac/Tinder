from keras.models import load_model
from keras.utils import load_img, img_to_array
import numpy
import os


def load_image(img_path, show=False):
    img = load_img(img_path, target_size=(300, 300))
    # (height, width, channels)
    img_tensor = img_to_array(img)
    # (1, height, width, channels), add a dimension because the model expects this shape: (batch_size, height, width, channels)
    img_tensor = numpy.expand_dims(img_tensor, axis=0)
    return img_tensor


def get_beauty_score(img_path):
    model_path = os.getcwd()+"/attractive_net/AttractiveNet/models/attractiveNet_mnv2.h5"
    print(model_path)
    model = load_model(model_path)
    # load a single image
    new_image = load_image(img_path)
    # check prediction
    pred = model.predict(new_image)
    return str(round(pred[0][0], 1))
