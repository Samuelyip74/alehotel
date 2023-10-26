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
from room.models import Room

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
    room_obj = Room.objects.filter(room_type__name__contains = reserve_obj.room.name, room_type__is_active=True)[:1].get()
    if request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest":
        data = json.load(request)
        profile_image = data.get('imgBase64')
        room_obj.is_active = True
        room_obj.save()
        reserve_obj.is_active = False
        reserve_obj.save()
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

def check_out(requst):
    pass