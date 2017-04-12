import json
import os
import pickle
import pyrebase

from datetime import datetime
from PIL import Image

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from api.models import Jaunt
from api.models import Membership
from api.models import Photo
from api.serializers import jaunt_serializer
from api.serializers import photo_serializer
from Jaunt.settings import FIREBASE_CONFIG

firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
storage = firebase.storage()
db = firebase.database()


def get_next_shortcode():
    with open('api/words.txt', 'rb') as f:
        words_list = pickle.loads(f.read())

    with open('api/words.txt', 'wb') as f:
        to_return = words_list.pop()
        f.write(pickle.dumps(words_list))
        return to_return


@csrf_exempt
def create_jaunt(request):
    if request.method == 'POST':
        params_dict = json.loads(request.body.decode())
        shortcode = get_next_shortcode()
        params_dict['shortcode'] = shortcode
        new_obj = Jaunt.objects.create(**params_dict)
        # TODO: check if jaunt should be live
        add_user_to_jaunt(params_dict['owner'], new_obj)
        db.child('users').child(params_dict['owner']).update({"current_jaunt": new_obj.id})
        return JsonResponse({
            'id': new_obj.id,
            'shortcode': shortcode
        })


def get_jaunt(request, id):
    try:
        obj = Jaunt.objects.get(id=id)
        return JsonResponse(jaunt_serializer(obj))
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Invalid id.'}, status=404)


@csrf_exempt
def join_jaunt(request):
    if request.method == 'POST':
        params_dict = json.loads(request.body.decode())
        try:
            obj = Jaunt.objects.get(shortcode=params_dict['shortcode'])
            add_user_to_jaunt(params_dict['user_id'], obj)
            db.child('users').child(params_dict['user_id']).update({"current_jaunt": obj.id})
            return JsonResponse({'status': 'Successfully added to {}'.format(obj.shortcode)})
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Invalid Shortcode.'}, status=404)
    # TODO: check if jaunt is live


@csrf_exempt
def leave_jaunt(request):
    if request.method == 'POST':
        params_dict = json.loads(request.body.decode())
        try:
            Membership.objects.get(user_id=params_dict['user_id'], jaunt__shortcode=params_dict['shortcode'])
            db.child('users').child(params_dict['user_id']).update({"current_jaunt": -1})
            return JsonResponse({'status': 'Successfully left {}'.format(params_dict['shortcode'])})
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'User isn\'t a part of jaunt {}'.format(params_dict['shortcode'])})


def add_user_to_jaunt(user_id, jaunt):
    obj = Membership.objects.create(user_id=user_id, jaunt=jaunt)
    return obj


@csrf_exempt
def add_photo(request):
    if request.method == 'POST':
        params_dict = json.loads(request.body.decode())
        thumbnail_path = convert_firebase_image_to_square(params_dict['original_path'])
        try:
            jaunt_obj = Jaunt.objects.get(id=params_dict.pop('jaunt_id'))
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Invalid jaunt_id.'})
        except KeyError:
            return JsonResponse({'error': 'Must pass in jaunt_id.'})


        params_dict['jaunt'] = jaunt_obj
        params_dict['thumbnail_path'] = thumbnail_path
        params_dict['taken_at'] = datetime.now()
        params_dict['deleted'] = False

        photo_obj = Photo.objects.create(**params_dict)
        serialized_photo = photo_serializer(photo_obj)
        db.child('jaunt/{}/photos'.format(jaunt_obj.id)).push(serialized_photo)

        return JsonResponse(serialized_photo)


def convert_firebase_image_to_square(firebase_path):
    temp_image_filename = 'temp_file.png'
    temp_thumb_name = 'square_temp_file.png'
    storage.child(firebase_path).download(temp_image_filename)
    thumbnail_path = get_thumbnail_path(firebase_path)
    convert_image_to_square(temp_image_filename, temp_thumb_name)
    storage.child(thumbnail_path).put(temp_thumb_name)
    os.remove(temp_image_filename)
    os.remove(temp_thumb_name)
    return thumbnail_path


def get_thumbnail_path(firebase_path):
    split_path = firebase_path.split('/')
    image_name = split_path[-1]
    split_path.pop()
    image_name = "square_{}".format(image_name)
    split_path.append('square_images')
    split_path.append(image_name)
    return '/'.join(split_path)


def convert_image_to_square(image_name, thumb_name):
    im = Image.open(image_name)
    square_image = im.crop((0, 0, min(im.size), min(im.size)))
    square_image.save(thumb_name)


def get_user(request, user_id):
    if request.method == 'GET':
        user_json = db.child('users').child(user_id).get().val()
        if user_json is None:
            return JsonResponse({'error': 'Invalid User ID'})
        return JsonResponse(user_json)


@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        user_json = json.loads(request.body.decode())
        user_json['current_jaunt'] = -1
        db.child("users").child(user_json['user_id']).set(user_json)
        return JsonResponse(user_json)
