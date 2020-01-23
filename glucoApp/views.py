# import random
import numpy as np
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from django.shortcuts import render
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import os
# Create your views here.
from .models import Experiment

MODEL_PATH = "{base_path}/my_model.h5".format(
	base_path=os.path.abspath(os.path.dirname(__file__)))

@csrf_exempt
def upload(request):
    # initialize the data dictionary to be returned by the request
    data = {"success": False}

    # check to see if this is a post request
    if request.method == "POST":
        # check to see if an image was uploaded
        if request.FILES.get("image", None) is not None:
            # grab the uploaded image

            im = request.FILES["image"]
            try:
                classifier = load_model(MODEL_PATH)
                img = image.load_img(im, target_size=(112, 112))
                img = np.expand_dims(img, axis=0)
                result = classifier.predict_classes(img)
                value=result[0]

            except:
                print("exception occur")
            exp=Experiment(image=im,value=value)
            exp.save()


        ### START WRAPPING OF COMPUTER VISION APP
        # Insert code here to process the image and update
        # the `data` dictionary with your results
        ### END WRAPPING OF COMPUTER VISION APP
        data['id']=exp.id
        data['value']=exp.value
        data['is_confirmed']=exp.is_confirmed
        # update the data dictionary
        data["success"] = True

    # return a JSON response
    return JsonResponse(data,status=201)


@csrf_exempt
def check_value_change(request,pk):
    # initialize the data dictionary to be returned by the request
    data = {"success": False}
    try:
        single_exp = SomeModel.objects.get(foo='bar',is_confirmed=False)
    except SomeModel.DoesNotExist:
        single_exp = None
    # check to see if this is a post request
    if request.method == "POST":
        # check to see if an image was uploaded
        url=request.POST.get("value", None)
            # grab the uploaded image
        if url is None:
                data["error"] = "No value provided."
                single_exp.is_confirmed=True
                single_exp.save()
                return JsonResponse(data)

        else:
            single_exp.value = request.POST.get("value", None)
            single_exp.is_confirmed = True

        single_exp.save()


        ### START WRAPPING OF COMPUTER VISION APP
        # Insert code here to process the image and update
        # the `data` dictionary with your results
        ### END WRAPPING OF COMPUTER VISION APP
        data['id']=single_exp.id
        data['value']=single_exp.value
        data['is_confirmed']=single_exp.is_confirmed
        # update the data dictionary
        data["success"] = True

    # return a JSON response
    return JsonResponse(data,status=201)
