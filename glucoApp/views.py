# import random
from wsgiref.util import FileWrapper
from zipfile import ZipFile


import requests
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
import imageio
from skimage.color import rgb2hsv, rgb2lab, rgb2ycbcr
# from skimage.transform import resize
import numpy as np
import cv2

import os
# Create your views here.
from glucoApp.models import Experiment


MODEL_PATH = "{base_path}/new_model.h5".format(
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
                
                datainp1=list()
		datainp2=list()
		datainp3=list()
		inp=imageio.imread(im)
		inp = cv2.resize(inp,(112, 112), interpolation = cv2.INTER_CUBIC)
		#inp_rgb=resize(inp_rgb,224,224)
		inp1=rgb2hsv(inp) 
		inp2=rgb2lab(inp)
		inp3=rgb2ycbcr(inp)

		datainp1.append(inp1)
		datainp2.append(inp2)
		datainp3.append(inp3)

		datainp1 = np.array(datainp1)
		datainp2 = np.array(datainp2)
		datainp3 = np.array(datainp3)

		preds = model.predict([datainp1,datainp2,datainp3])

		y_classes = preds.argmax(axis=-1) 
		value=y_classes[0]




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
    try:
        with ZipFile('export.zip', 'w') as export_zip:
            for exp_image in exp_images:
                exp_image_url = exp_image.image.url
                r = requests.get(exp_image_url, timeout=60)
                # image_path = settings.MEDIA_ROOT+ exp_image_url[11:]

                image_name="{0}_{1}.jpg".format(exp_image.id,exp_image.value)
                # Get your file name here.
                export_zip.write(r.content, image_name)
    except:
        print("error")


    wrapper = FileWrapper(open('export.zip', 'rb'))
    content_type = 'application/zip'
    content_disposition = 'attachment; filename=export.zip'

    response = HttpResponse(wrapper, content_type=content_type)
    response['Content-Disposition'] = content_disposition
    return response
