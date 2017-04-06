import json
import pickle

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from api.models import Jaunt
from api.models import Membership
from api.serializers import jaunt_serializer


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
        params_dict = json.loads(request.body)
        shortcode = get_next_shortcode()
        params_dict['shortcode'] = shortcode
        new_obj = Jaunt.objects.create(**params_dict)
        # TODO: check if jaunt should be live
        add_user_to_jaunt(params_dict['owner'], new_obj)
        # TODO: create empty list for pictures and locations
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
        params_dict = json.loads(request.body)
        try:
            obj = Jaunt.objects.get(shortcode=params_dict['shortcode'])
            add_user_to_jaunt(params_dict['user_id'], obj)
            return JsonResponse({'status': 'Successfully added to {}'.format(obj.title)})
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Invalid Shortcode.'}, status=404)
    # TODO: check if jaunt is live


def add_user_to_jaunt(user_id, jaunt):
    obj = Membership.objects.create(user_id=user_id, jaunt=jaunt)
    return obj
