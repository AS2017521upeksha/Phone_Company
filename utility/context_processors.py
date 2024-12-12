from store .models import Category, CartItem, Profile
from django.conf import settings

def categories(request):
    categories = Category.objects.all()
    return {'categories': categories}

def user_profile_image(request):
    if request.user.is_anonymous:
        return {'user_profile_image':f"{settings.MEDIA_URL}uploads/profiles/avatar1.png"}
    else:
        try:
            user_profile_image = Profile.objects.get(user=request.user).image.url
            return {'user_profile_image': user_profile_image}
        except:
            return {'user_profile_image':  f"{settings.MEDIA_URL}uploads/profiles/avatar1.png"}

def cart_items_context(request):
    if request.user.is_authenticated:
        cart_items_count = CartItem.objects.filter(user=request.user).count()
        return {'cart_items_count': cart_items_count}
    else:
        return {'cart_items_count': 0}
