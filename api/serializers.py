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


def photo_serializer(obj):
    photo_dict = {
        'id': obj.id,
        'owner': obj.owner,
        'original_path': obj.original_path,
        'thumbnail_path': obj.thumbnail_path,
        'latitude': obj.latitude,
        'longitude': obj.longitude,
        'deleted': obj.deleted
    }

    return photo_dict