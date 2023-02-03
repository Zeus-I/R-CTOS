# R - ctos
## _Real-time cloths tryon system
A flask application that allows user to try upper cloths from any shopping website by using opencv library from python. 
You first need manually clone or download the repository and install all the libraries from requirements.txt.
```sh
$ pip install -r requirements.txt
```
You need to run ctos.py in your machine.
```sh
$ python ctos.py
```
>Open http://127.0.0.1:5000/

You will see the home page of our application.
![image](https://user-images.githubusercontent.com/86234577/164490321-34b1ec63-f4b2-49d7-9d6a-7ca21161ef6a.png)

When you click on “Let Get Started”. You will see the try-on page where you have to put the image of the cloth you want to try and below that you will see the selection size dropdown selection field.
![image](https://user-images.githubusercontent.com/86234577/164490421-e0880043-5d6a-4697-92c8-f2cb912e5614.png)

You can take the cloth image from any shopping website like Amazon, Flipcart, Myntra, etc. by taking a screenshot of the cloth area. Here I am taking a t-shirt from Amazon.
![image](https://user-images.githubusercontent.com/86234577/164490823-8aa08612-5f46-4409-984c-cc7abd61ae93.png)

After snipping the required part from the image you have to save that image in your machine.
![image](https://user-images.githubusercontent.com/86234577/164490739-d214bb6d-6a1b-4609-8641-96667b1a52c9.png)

In the try-on page of our site you have to upload the image there and after selecting your size you have to click on upload.
![image](https://user-images.githubusercontent.com/86234577/164490960-bc553808-9eaf-4311-aa8b-560b546f39a0.png)

After clicking the upload button yo will see the page where actual real time cloth try-on is being done and on this screen you will be able to see how the will look on you and after that you can by that cloth if it looks good on you.
![image](https://user-images.githubusercontent.com/86234577/164491098-2bd6c91f-7313-4e83-85f6-c2b91a055f4b.png)


