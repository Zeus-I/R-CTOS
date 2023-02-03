from flask import Flask, render_template, Response, url_for, flash, request, redirect
import cv2
import urllib.request
import os
from werkzeug.utils import secure_filename
from bgrem import *


app = Flask(__name__)


cap = cv2.VideoCapture(0)  # use 0 for web camera
 


UPLOAD_FOLDER = 'static/uploads'
 
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def gen_frames():  # generate frame by frame from camera
    while True:
        # Capture frame-by-frame
        imgshirt = cv2.imread("./processing/1.png") 
        shirtgray = cv2.cvtColor(imgshirt,cv2.COLOR_BGR2GRAY) #grayscale conversion
        ret, orig_masks = cv2.threshold(shirtgray,0 , 255, cv2.THRESH_BINARY) #there may be some issues with image threshold...depending on the color/contrast of image
        orig_masks_inv = cv2.bitwise_not(orig_masks)
        origshirtHeight, origshirtWidth = imgshirt.shape[:2]

        face_cascade=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
 
        ret,img=cap.read()
       
        height = img.shape[0]
        width = img.shape[1]
        print(size)
        
        #cv2.namedWindow("img",cv2.WINDOW_NORMAL)
        #cv2.resizeWindow("img", (int(width*3/2), int(height*3/2)))
        gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        faces=face_cascade.detectMultiScale(gray,1.3,5)
 
        for (x,y,w,h) in faces:
            # cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            #cv2.rectangle(img,(100,200),(312,559),(255,255,255),2)
 
#|||||||||||||||||||||||||||||||SHIRT||||||||||||||||||||||||||||||||||||||||
 
            shirtWidth =  4 * w  #approx wrt face width
            shirtHeight = shirtWidth * origshirtHeight / origshirtWidth #preserving aspect ratio of original image..
            # Center the shirt..just random calculations..
            if(size == "small"):
                x1s = x-0.5*w
                x2s =x1s+2.5*w
                y1s = y+h
                y2s = y1s+h*4
                if x1s < 0:
                    x1s = 1
                if x2s > img.shape[1]:
                    x2s =img.shape[1]
                if y2s > img.shape[0] :
                    y2s =img.shape[0]
                temp=1
                if y1s>y2s:
                    temp=y1s
                    y1s=y2s
                    y2s=temp
            elif(size == "medium"):
                x1s = x-1.125*w
                x2s =x1s+3.25*w
                y1s = y+h
                y2s = y1s+h*4
                if x1s < 0:
                    x1s = 1
                if x2s > img.shape[1]:
                    x2s =img.shape[1]
                if y2s > img.shape[0] :
                    y2s =img.shape[0]
                temp=1
                if y1s>y2s:
                    temp=y1s
                    y1s=y2s
                    y2s=temp
            elif(size == "xtralarge"):
                x1s = x-1.25*w
                x2s =x1s+3.5*w
                y1s = y+h
                y2s = y1s+h*4.5
                if x1s < 0:
                    x1s = 1
                if x2s > img.shape[1]:
                    x2s =img.shape[1]
                if y2s > img.shape[0] :
                    y2s =img.shape[0]
                temp=1
                if y1s>y2s:
                    temp=y1s
                    y1s=y2s
                    y2s=temp
            elif(size == "xxtralarge"):
                x1s = x-1.5*w
                x2s =x1s+4*w
                y1s = y+h
                y2s = y1s+h*5
                if x1s < 0:
                    x1s = 1
                if x2s > img.shape[1]:
                    x2s =img.shape[1]
                if y2s > img.shape[0] :
                    y2s =img.shape[0]
                temp=1
                if y1s>y2s:
                    temp=y1s
                    y1s=y2s
                    y2s=temp
            else:
                x1s = x-1*w
                x2s =x1s+3*w
                y1s = y+h
                y2s = y1s+h*4
                if x1s < 0:
                    x1s = 1
                if x2s > img.shape[1]:
                    x2s =img.shape[1]
                if y2s > img.shape[0] :
                    y2s =img.shape[0]
                temp=1
                if y1s>y2s:
                    temp=y1s
                    y1s=y2s
                    y2s=temp
            # Check for clipping(whetehr x1 is coming out to be negative or not..)
 
            """
            if y+h >=y1s:
                y1s = 0
                y2s=0
            """
            # Re-calculate the width and height of the shirt image(to resize the image when it wud be pasted)
            shirtWidth = int(abs(x2s - x1s))
            shirtHeight = int(abs(y2s - y1s))
            y1s = int(y1s)
            y2s = int(y2s)
            x1s = int(x1s)
            x2s = int(x2s)
          
# Re-size the original image and the masks to the shirt sizes
            shirt = cv2.resize(imgshirt, (shirtWidth,shirtHeight), interpolation = cv2.INTER_AREA) #resize all,the masks you made,the originla image,everything
            mask = cv2.resize(orig_masks, (shirtWidth,shirtHeight), interpolation = cv2.INTER_AREA)
            masks_inv = cv2.resize(orig_masks_inv, (shirtWidth,shirtHeight), interpolation = cv2.INTER_AREA)
            try:
                rois = img[y1s:y2s, x1s:x2s]
                num=rois
                roi_bgs = cv2.bitwise_and(rois,num,mask = masks_inv)
                # roi_fg contains the image of the shirt only where the shirt is
                roi_fgs = cv2.bitwise_and(shirt,shirt,mask = mask)
                # join the roi_bg and roi_fg
                dsts = cv2.add(roi_bgs,roi_fgs)
                img[y1s:y2s, x1s:x2s] = dsts # place the joined image, saved to dst back over the original image
            #print "blurring"
            except:
                print('ggwp')
            break

        if not ret:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', img)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/upload')
def upload():
    return render_template('upload1.html')

# @app.route('/tryon',  methods=['POST'])
# def tryon():
#     return render_template('upload.html')


@app.route('/tryon', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        # filename = secure_filename(file.filename)
        filename = secure_filename("1.png") #assigning filename to uploaded image
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print('upload_image filename: ' + filename)
        flash('Image successfully uploaded')
        init("./static/uploads/1.png")
        global size
        size = request.form.get("size")
        return render_template('tryon.html')
        #return render_template('tryon.html')
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)


if __name__ == '__main__':
    app.run(debug=True)
