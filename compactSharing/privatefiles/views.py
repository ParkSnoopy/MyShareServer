from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from django.http import HttpResponse, FileResponse, Http404

from localutils.filename_validator import safe_filename

from pathlib import Path

# Create your views here.


@user_passes_test(lambda user: user.is_superuser)
def privatefiles(request):
    
    if not settings.USE_PRIFILES:
        raise Http404()

    filepath = Path( request.GET.get('filepath') )
    
    is_safe_filename, _ = safe_filename(filename=str(filepath), is_superuser=True)
    
    if not is_safe_filename:
        return HttpResponse("Your input filepath is considered an important system file, or unsafe url. Not available on this route.")
    
    
    if not filepath.exists():
   		raise Http404()
   
    if filepath.is_file():
   		return FileResponse( open( Path( filepath ) , 'rb' ) )
   
    if filepath.is_dir():
   		buffer = ">> ls<br><br>"
   		for d in filepath.iterdir():
   			buffer += f"{d}<br>"
   		return HttpResponse(buffer)
   
    return HttpResponse("Input filepath not exist. Please correct filepath.")
