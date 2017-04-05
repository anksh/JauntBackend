import pickle

from django.http import JsonResponse

from api.models import Jaunt


def get_next_shortcode():
    with open('words.txt', 'rb') as f:
        words_list = pickle.loads(f.read())

    with open('words.txt', 'wb') as f:
        to_return = words_list.pop()
        f.write(pickle.dumps(words_list))
        return to_return


def create_jaunt(request):
    if (request.method == 'POST'):
        params_dict = request.POST
        params_dict['shortcode'] = get_next_shortcode()
        new_obj = Jaunt.objects.create(params_dict)
        return JsonResponse({'id': new_obj})

