from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from django.http import HttpResponse, FileResponse, Http404
from django.shortcuts import redirect

from pathlib import Path

# Create your views here.


@user_passes_test(lambda user: user.is_superuser)
def privatefiles(request):

	if not settings.USE_PRIFILES:
		raise Http404()

	filepath = Path( request.GET.get('filepath') )

	if not filepath.exists():
		raise Http404()

	if filepath.is_file():
		return FileResponse(
	        open( Path(filepath) , 'rb' )
	    )

	if filepath.is_dir():
		buffer = ">> ls<br><br>"
		for d in filepath.iterdir():
			buffer += f"{d}<br>"
		return HttpResponse(buffer)

	return HttpResponse(f"GET {filepath = }, but not existing file, nor existing directory. Please correct filepath.")
