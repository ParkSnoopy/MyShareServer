from django.shortcuts import render, redirect
from django.conf import settings
from django.http import FileResponse

APH = settings.MY_ACCESS_PERMISSION_HANDLER

from localutils.hasher import my_hash, pw_check
from localutils.filename_validator import safe_global_filename

from .models import SecretFile

# Create your views here.


def lightfileshare_home(request):
    
    SecretFile.objects.remove_not_exist()
    SecretFile.objects.remove_expired()
    
    return render(request, 'lightfileShare/index.html', {
        'objs': SecretFile.objects.all().values('id', 'title', 'posted_by')
    })

def lightfileshare_details(request):
    if request.method == 'GET':
        
        pk = request.GET.get('id')
        try:
            secretfile = SecretFile.objects.get(pk=pk)
            
            if secretfile.password:
                
                has_perm = APH.check_perm(
                    request.session.session_key, 
                    secretfile
                )
                if not has_perm:
                    return redirect(f'/lightfile/details/verify?id={pk}')
            
            path = settings.MEDIA_ROOT / secretfile.content.name
            return FileResponse( open( path, 'rb' ) )
        
        except SecretFile.DoesNotExist:
            pass
        except:
            pass
    
    return redirect('/lightfile/')

def lightfileshare_details_pwcheck(request):
    
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
    
    return render(
        request, 
        'lightfileShare/failure.html', 
        {
            'redirect': f'details?id={pk}', 
            'fail_reason': 'Password Mismatch', 
            'fail_explain': '', 
        }
    )

def lightfileshare_create(request):
    if request.method == 'POST' and request.FILES:
        
        content = request.FILES['file']
        
        posted_by = request.POST.get('posted_by') or 'AnonymousUser'
        password = request.POST.get('password')
        title = request.POST.get('title') or content.name
        
        filename, unsafe_word = safe_global_filename(filename=str(content.name))
        
        if not filename:
            return render(
                request, 
                'lightfileShare/failure.html', 
                {
                    'redirect': 'create', 
                    'fail_reason': f"filename '{content.name}' is considered an important system file", 
                    'fail_explain': f"please consider replace '{unsafe_word}' to other common word", 
                }
            )
        
        if title and content:
            SecretFile.objects.create(
                password = my_hash(password) if password else None, 
                title=title, 
                content=content, 
                posted_by=posted_by
            )
        return redirect('/lightfile/')
    return render(request, 'lightfileShare/create.html')
