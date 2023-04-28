import base64
import cv2
import numpy as np
from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from Cropper import predictAndCropIm

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.fromstring(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    crops = predictAndCropIm(img)
    # print(len(crops))
    # do something with the OpenCV image here
    # you can access the filename with file.filename
    response = {}
    for clas in crops:
        for img in crops[clas]:
            retval, buffer = cv2.imencode('.jpg', img)
            encoded_image = base64.b64encode(buffer).decode('utf-8')
            response[clas] = response.get(clas,[]) + [encoded_image]
            # response(encoded_image,clas))
    return {"filename": file.filename,"images": response}
