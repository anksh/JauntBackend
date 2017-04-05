

def jaunt_serializer(obj):
    jaunt_dict = {
        'start_date': obj.start_date,
        'end_date': obj.end_date,
        'live': obj.live,
        'owner': obj.owner,
        'title': obj.title,
        'shortcode': obj.shortcode
    }

    return jaunt_dict