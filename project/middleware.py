def isGuest(request):
    if request.session.get("project") != None:
        return False
    else:
        return True
