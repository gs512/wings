from threading import local

_user = local()


class CurrentUserMiddleware(object):
	def process_request(self, request):
		_user.value = request.user
		_user.groups = request.user.groups.values_list('name',flat=True)
		_user.is_superuser = request.user.is_superuser

def get_current_user():
	if hasattr(_user,"value"):return _user.value
	else: return -1

def get_current_user_groups():
	if hasattr(_user,"groups"):return _user.groups
	else: return []
	
def get_current_user_is_super():
	if hasattr(_user,"is_superuser"):return _user.is_superuser
	else:return False