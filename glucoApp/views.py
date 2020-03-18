# import random
from wsgiref.util import FileWrapper
from zipfile import ZipFile

import numpy as np
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse

from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import os
# Create your views here.
from glucoApp.models import Experiment


MODEL_PATH = "{base_path}/my_model.h5".format(
	base_path=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@csrf_exempt
def upload(request):
    # initialize the data dictionary to be returned by the request
    data = {"success": False}

    # check to see if this is a post request
    if request.method == "POST":
        print(MODEL_PATH)
        # check to see if an image was uploaded
        if request.FILES.get("image", None) is not None:
            # grab the uploaded image

            im = request.FILES["image"]
            try:
                classifier = load_model(MODEL_PATH)
                img = image.load_img(im, target_size=(112, 112))
                img = np.expand_dims(img, axis=0)
                result = classifier.predict_classes(img)
                value=int(result[0])




            except:
                print("exception occur")
                return JsonResponse(data, status=500)
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


def index(request):
    print(MODEL_PATH)
    return HttpResponse("hello")

@csrf_exempt
def     check_value_change(request,pk):
    # initialize the data dictionary to be returned by the request
    data = {"success": False}
    try:
        single_exp = Experiment.objects.get(id=pk,is_confirmed=False)
    except Experiment.DoesNotExist:
        data['error']="Not exist"

        return JsonResponse(data,status=404)
    # check to see if this is a post request
    if request.method == "POST":
        # check to see if an image was uploaded
        url=request.POST.get("value", None)
            # grab the uploaded image
        if url is None:
                data["error"] = "No value provided."
                single_exp.is_confirmed=True


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



def download_image(request):
    exp_images=Experiment.objects.all()
    with ZipFile('export.zip', 'w') as export_zip:
        for exp_image in exp_images:
            exp_image_url = exp_image.image.url

            # image_path = settings.MEDIA_ROOT+ exp_image_url[11:]

            image_name="{0}_{1}.jpg".format(exp_image.id,exp_image.value)
            # Get your file name here.
            export_zip.write(exp_image_url, image_name)

    wrapper = FileWrapper(open('export.zip', 'rb'))
    content_type = 'application/zip'
    content_disposition = 'attachment; filename=export.zip'

    response = HttpResponse(wrapper, content_type=content_type)
    response['Content-Disposition'] = content_disposition
    return response
