def isGuest(request):
    if request.session.get("project") is not None:
        return False
    else:
        return True
