from django.template.loader import get_template
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
import string
import random
import os
import json
from datetime import datetime
from django.contrib.auth import authenticate,login
from product.models import Product
from reservation.models import Reservation
from free_radius.models import Radcheck
from room.models import Room
import face_recognition
from PIL import Image
import base64
import cv2
import pickle
import numpy as np

def index(request):
    context = {
    }
    template = get_template( 'index.html')
    return HttpResponse(template.render(context,request))    

def list_rooms(request):
    if request.method == 'POST':
        data = request.POST.copy()
        product_obj = Product.objects.all()
        context = {
            'startdate' : data['start-date'],
            'enddate' : data['end-date'],
            'guest' : data['guest'],
            'product_obj' : product_obj
        }
        template = get_template( 'listrooms.html')
        return HttpResponse(template.render(context,request))   
    else:
        context = {
        }
        template = get_template( 'index.html')
        return HttpResponse(template.render(context,request))      

def booking(request, startdate, enddate, guest, pk):
    start_date_obj = datetime.strptime(startdate, '%d %B, %Y')
    end_date_obj = datetime.strptime(enddate, '%d %B, %Y')
    delta = end_date_obj - start_date_obj    
    product_obj = Product.objects.get(id=pk)

    t_price = delta.days * product_obj.price
    # user is logged in
    if request.user.is_authenticated:
        user_obj = request.user

        # user submit confirmation
        if request.method == 'POST':
            data = request.POST.copy()
            if data['confirm'] == 'ok':
                confirmation_code = "".join(random.choices(string.ascii_letters, k=8))
                Reservation.objects.create(
                    user = user_obj,
                    start_date = start_date_obj,
                    end_date = end_date_obj,
                    guest = guest,
                    days = delta.days,
                    price = t_price,
                    room = product_obj,
                    code = confirmation_code
                )
            context = {
                'code' : confirmation_code,
             }
            template = get_template( 'booking_confirmed.html')
            return HttpResponse(template.render(context,request)) 
                

        # display room details and prompt user to submit confirmation
        else:
            context = {
                'user_obj' : user_obj,
                'startdate' : start_date_obj,
                'enddate' : end_date_obj,
                'duration' : delta.days,
                'guest' : guest,
                'product_obj': product_obj,
                't_price' : t_price
            }
            template = get_template( 'booking_confirmation.html')
            return HttpResponse(template.render(context,request)) 
    
    # user is not created or logged in
    else:
        if request.method == 'POST':
            data = request.POST.copy()
            user_obj = authenticate(username=data['username'], password=data['password'])
            if user_obj is not None and user_obj.is_active:
                login(request, user_obj)
                context = {
                    'startdate' : start_date_obj,
                    'enddate' : end_date_obj,
                    'duration' : delta.days,
                    'guest' : guest,
                    'product_obj': product_obj,
                    't_price' : t_price
                }
                template = get_template( 'booking_confirmation.html')
                return HttpResponse(template.render(context,request))   
            else:
                context = {
                    'startdate' : start_date_obj,
                    'enddate' : end_date_obj,
                    'duration' : delta.days,
                    'guest' : guest,
                    'product_obj': product_obj,
                    't_price' : t_price
                }
                template = get_template( 'booking_confirmation.html')
                return HttpResponse(template.render(context,request))       
    
        context = {
            'startdate' : start_date_obj,
            'enddate' : end_date_obj,
            'duration' : delta.days,
            'guest' : guest,
            'product_obj': product_obj,
            't_price' : t_price
        }
        template = get_template( 'booking_confirmation.html')
        return HttpResponse(template.render(context,request))  


def check_in_out(request):
    context = {

    }
    template = get_template( 'check_in_out.html')
    return HttpResponse(template.render(context,request))  

def check_in(request):
    if request.method == "POST":
        data = request.POST.copy()
        try:
            reserve_obj = Reservation.objects.get(code=data['code'],is_active=True)
            context = {
                "reserve_obj" : reserve_obj
            }
            template = get_template( 'check_in.html')
            return HttpResponse(template.render(context,request)) 
        except Reservation.DoesNotExist:
            context = {
            }                
            template = get_template( 'no_reservation_found.html')
            return HttpResponse(template.render(context,request))                    

    else:
        context = {
        }        
        template = get_template( 'check_in.html')
        return HttpResponse(template.render(context,request))  

def check_in_confirmation(request, pk):
    
    reserve_obj = Reservation.objects.get(id=pk)
    room_obj = Room.objects.filter(room_type__name__contains = reserve_obj.room.name, is_active=False)[:1].get()

    if request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest":
        data = json.load(request)

        # save data to variable image
        image = data.get('imgBase64')

        # remove prefix to make image base64 encoding
        profile_image = image.removeprefix("data:image/png;base64,")
        room_obj.is_active = True
        room_obj.user = reserve_obj.user
        room_obj.save()
        reserve_obj.is_active = False
        reserve_obj.save()
        rad_user = Radcheck.objects.create(username=str(room_obj.number), attribute="Cleartext-Password", op=":=", value=reserve_obj.user.last_name)

        # save image to file
        imgdata = base64.b64decode(profile_image)
        filename = '/var/www/alehotel/django_hotel/media/base64.jpg'  # I assume you have a way of picking unique filenames

        # open image file
        with open(filename, 'wb') as f:
            f.write(imgdata)  

        # defined all faces encoding dictionary            
        all_face_encodings = {}

        # if dataset_faces.dat exist, load saved encoding into all_face_encodings
        try:
            with open('/var/www/alehotel/django_hotel/media/dataset_faces.dat', 'rb') as f:
                openfile = pickle.load(f)
            
            for key in openfile:
                all_face_encodings[key] = openfile[key]       
        except:
            pass

        # convert image to face_encoding
        saved_image = face_recognition.load_image_file("/var/www/alehotel/django_hotel/media/base64.jpg")

        # save face_encoding into all_face_encodings variable
        all_face_encodings[str(room_obj.number)] = face_recognition.face_encodings(saved_image)[0]

        # save updated encoding to dataset_faces.dat
        with open('/var/www/alehotel/django_hotel/media/dataset_faces.dat', 'wb') as f:
            pickle.dump(all_face_encodings, f)

        return JsonResponse({'status': "uploaded"})               
    else:
        context = {
            "room_obj": room_obj
        }
        template = get_template( 'room_confirmation.html')
        return HttpResponse(template.render(context,request))  

def check_in_completed(request):
    context = {
    }
    template = get_template( 'check_in_completed.html')
    return HttpResponse(template.render(context,request))          

def check_out(request):
    if request.method == "POST":
        data = request.POST.copy()
        try:
            room_obj = Room.objects.get(number=data['room_num'], is_active=True)
            room_obj.is_active = False
            room_obj.save()
            try:
                rad_user = Radcheck.objects.get(username=data['room_num'])
                rad_user.delete()
            except:
                pass
            all_face_encodings = {}
            # if dataset_faces.dat exist, load saved encoding into all_face_encodings
            try:
                with open('/var/www/alehotel/django_hotel/media/dataset_faces.dat', 'rb') as f:
                    openfile = pickle.load(f)
                
                for key in openfile:
                    if key == str(room_obj.number):
                        pass

                    else:
                        all_face_encodings[key] = openfile[key]   

                # save updated encoding to dataset_faces.dat
                with open('/var/www/alehotel/django_hotel/media/dataset_faces.dat', 'wb') as f:
                    pickle.dump(all_face_encodings, f)  
                    
                context = {
                }
                template = get_template( 'check_out_completed.html')
                return HttpResponse(template.render(context,request))                                   

            except:
                pass
                context = {
                }
                template = get_template( 'check_out_completed.html')
                return HttpResponse(template.render(context,request)) 
        except Room.DoesNotExist:
            context = {
            }                
            template = get_template( 'check_out_error.html')
            return HttpResponse(template.render(context,request))                    

    else:
        context = {
        }        
        template = get_template( 'check_out.html')
        return HttpResponse(template.render(context,request))  

def unlock_door(request):

    if request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest":
        data = json.load(request)
        # save data to variable image
        image = data.get('imgBase64')

        # remove prefix to make image base64 encoding
        profile_image = image.removeprefix("data:image/png;base64,")

        # save image to file
        imgdata = base64.b64decode(profile_image)
        filename = '/var/www/alehotel/django_hotel/media/base64.jpg'  # I assume you have a way of picking unique filenames

        # open image file
        with open(filename, 'wb') as f:
            f.write(imgdata)  

        # defined all faces encoding dictionary            
        all_face_encodings = {}
        # convert image to face_encoding
        saved_image = face_recognition.load_image_file("/var/www/alehotel/django_hotel/media/base64.jpg")

        # if dataset_faces.dat exist, load saved encoding into all_face_encodings
        try:
            with open('/var/www/alehotel/django_hotel/media/dataset_faces.dat', 'rb') as f:
                openfile = pickle.load(f)
            
            for key in openfile:
                all_face_encodings[key] = openfile[key]       
        except:
            pass

        known_face_names = list(all_face_encodings.keys())
        known_face_encodings = np.array(list(all_face_encodings.values()))            

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(saved_image)
        face_encodings = face_recognition.face_encodings(saved_image, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                return JsonResponse({'status': name})  
                # return JsonResponse({'status': "Not found"})               
            else:
                return JsonResponse({'status': "Not found"})               
        return JsonResponse({'status': "Not found"})  
    else:
        context = {
        }
        template = get_template( 'unlock_room.html')
        return HttpResponse(template.render(context,request))          


def stringToRGB(base64_string):
    imgdata = base64.b64decode(str(base64_string))
    img = Image.open(io.BytesIO(imgdata))
    opencv_img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
    return opencv_img     


def stellar_login(request):
    url = error_msg = None

    if request.method == "POST":
        data = request.POST.copy()
        username = data['user']
        password = data['password']
        url = data['url']


        try:
            rad_obj = Radcheck.objects.get(username=username)
            if (rad_obj.value == password):
                context = {
                    "username" : username,
                    "password" : password,
                    "ap_login_url" : "https://cportal.al-enterprise.com/login",
                    "url" : url,
                    "onerror" : "https://192.168.2.243/ale/login?error=1",
                }
                template = get_template( 'auto_login.html')
                return HttpResponse(template.render(context,request))                  
        except:
            error_msg = "User not found or password incorrect"
            context = {
                "ap_login_url" : "https://cportal.al-enterprise.com/login",
                "url" : url,
                "onerror" : "https://192.168.2.243/ale/login?error=1",
                "error_msg" : error_msg
            }
            template = get_template( 'stellar_login.html')
            return HttpResponse(template.render(context,request))   

    else:
        try:
            error = request.GET['error']

            if error == "1":
                error_msg = "User not found or password incorrect"

        except:
            pass
        
        try:
            clientmac = request.GET['clientmac']
        except:
            pass

        try:
            clientip = request.GET['clientip']
        except:
            pass        

        try:
            switchmac = request.GET['switchmac']
        except:
            pass        

        try:
            switchip = request.GET['switchip']
        except:
            pass     

        try:
            ssid = request.GET['ssid']
        except:
            pass     

        try:
            url = request.GET['url']
        except:
            pass     


        context = {
            "ap_login_url" : "https://cportal.al-enterprise.com/login",
            "url" : url,
            "onerror" : "https://192.168.2.243/ale/login?error=1",
            "error_msg" : error_msg
        }
        template = get_template( 'stellar_login.html')
        return HttpResponse(template.render(context,request))         

    

