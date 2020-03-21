from django.shortcuts import redirect

def is_owner(model):
    def model_type(func):
        def wrapper(request, pk, *args, **kwargs):
            obj = model.objects.get(id=pk)
            if obj.user.id == request.user.id:
                return func(request, pk)
            else:
                return redirect('/permission_denied')
        return wrapper
    return model_type

