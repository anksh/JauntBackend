from copy import copy
import json
import pickle

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from api.models import Jaunt


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
        return JsonResponse({
            'id': new_obj.id,
            'shortcode': shortcode
        })

