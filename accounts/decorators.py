from django.shortcuts import redirect, get_object_or_404
from accounts.models import User

def is_owner(func):
    def wrapper(request, pk, *args, **kwargs):
        user = get_object_or_404(User, pk=pk)
        print(request.user.id)
        print(user.id)
        if request.user.id == user.id:
            return func(request, pk)
        else:
            return redirect('/permission_denied')
    return wrapper


