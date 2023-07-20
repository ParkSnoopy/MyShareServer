from django.shortcuts import render, redirect
from django.conf import settings
from django.http import FileResponse

APH = settings.MY_ACCESS_PERMISSION_HANDLER

from localutils.hasher import my_hash, pw_check

from .models import SecretFile

# Create your views here.


def lightfileshare_home(request):
    
    # print(f"{request.session.__dict__ = }")
    # print(f"{request.session.get('session_key') = }")
    SecretFile.objects.remove_not_exist()
    SecretFile.objects.remove_expired()
    
    return render(request, 'lightfileShare/index.html', {
        'objs': SecretFile.objects.all().values('id', 'title', 'posted_by')
    })

def lightfileshare_details(request):
    if request.method == 'GET':
        # print(f"{request.session.get('session_key') = }")
        pk = request.GET.get('id')
        try:
            secretfile = SecretFile.objects.get(pk=pk)
            
            if secretfile.password:
                
                has_perm = APH.check_perm(
                    request.session.session_key, 
                    secretfile
                )
                # print(f"\n  {has_perm = }\n")
                if not has_perm:
                    return redirect(f'/lightfile/details/verify?id={pk}')
            
            path = settings.MEDIA_ROOT / secretfile.content.name
            return FileResponse( open( path, 'rb' ) )
        
        except SecretFile.DoesNotExist:
            pass
    return redirect('/lightfile/')

def lightfileshare_details_pwcheck(request):
    # print(f"{request.POST = } // {request.GET = }")
    
    pk = request.GET.get('id')
    if not pk:
        return redirect('/lightfile/')
    
    try:
        secretfile = SecretFile.objects.get(pk=pk)
    except SecretFile.DoesNotExist:
        return redirect('/lightfile/')
    
    if request.method == 'POST':
        password = request.POST.get('password')
        
        is_pw_correct = pw_check(
            password, 
            secretfile.password
        )
        # print(f"\n  {is_pw_correct = }\n")
        if is_pw_correct:
            APH.set_perm(
                request.session.session_key, 
                secretfile
            )
            return redirect(f'/lightfile/details?id={pk}')
        else:
            return redirect(f'/lightfile/details/verify/failure?id={pk}')
    
    return render(request, 'lightfileShare/details_verify.html', {'title': secretfile.title})

def lightfileshare_details_fail(request):
    pk = request.GET.get('id')
    if not pk:
        return redirect('/lightfile/')
    
    return render(request, 'lightfileShare/failure.html', {'id': pk})

def lightfileshare_create(request):
    if request.method == 'POST' and request.FILES:
        # print(f"{request.POST = }")
        # print(f"{request.FILES = }")
        content = request.FILES['file']
        
        posted_by = request.POST.get('posted_by') or 'anonymousUser'
        password = request.POST.get('password')
        title = request.POST.get('title') or content.name
        
        # with open("some/file/name.txt", "wb+") as destination:
        #     for chunk in f.chunks():
        #         destination.write(chunk)
        
        if title and content:
            SecretFile.objects.create(
                password = my_hash(password) if password else None, 
                title=title, 
                content=content, 
                posted_by=posted_by
            )
        return redirect('/lightfile/')
    return render(request, 'lightfileShare/create.html')