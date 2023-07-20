from django.shortcuts import render, redirect
from django.conf import settings
APH = settings.MY_ACCESS_PERMISSION_HANDLER

from localutils.hasher import my_hash, pw_check

from .models import SecretClipboard

# Create your views here.


def clipboardshare_home(request):
    
    # print(f"{request.session.__dict__ = }")
    # print(f"{request.session.get('session_key') = }")
    SecretClipboard.objects.remove_expired()
    
    return render(request, 'clipboardShare/index.html', {
        'objs': SecretClipboard.objects.all().values('id', 'title', 'posted_by')
    })

def clipboardshare_details(request):
    if request.method == 'GET':
        # print(f"{request.session.get('session_key') = }")
        pk = request.GET.get('id')
        try:
            secretclipboard = SecretClipboard.objects.get(pk=pk)
            
            if secretclipboard.password:
                
                has_perm = APH.check_perm(
                    request.session.session_key, 
                    secretclipboard
                )
                # print(f"\n  {has_perm = }\n")
                if not has_perm:
                    return redirect(f'/clipboard/details/verify?id={pk}')
            
            return render(request, 'clipboardShare/details.html', {
                'obj': secretclipboard, 
                'content': secretclipboard.content.split('\r\n')
            })
                
        
        except SecretClipboard.DoesNotExist:
            pass
    return redirect('/clipboard/')

def clipboardshare_details_pwcheck(request):
    # print(f"{request.POST = } // {request.GET = }")
    
    pk = request.GET.get('id')
    if not pk:
        return redirect('/clipboard/')
    
    try:
        secretclipboard = SecretClipboard.objects.get(pk=pk)
    except SecretClipboard.DoesNotExist:
        return redirect('/clipboard/')
    
    if request.method == 'POST':
        password = request.POST.get('password')
        
        is_pw_correct = pw_check(
            password, 
            secretclipboard.password
        )
        # print(f"\n  {is_pw_correct = }\n")
        if is_pw_correct:
            APH.set_perm(
                request.session.session_key, 
                secretclipboard
            )
            return redirect(f'/clipboard/details?id={pk}')
        else:
            return redirect(f'/clipboard/details/verify/failure?id={pk}')
    
    return render(request, 'clipboardShare/details_verify.html', {'title': secretclipboard.title})

def clipboardshare_details_fail(request):
    pk = request.GET.get('id')
    if not pk:
        return redirect('/clipboard/')
    
    return render(request, 'clipboardShare/failure.html', {'id': pk})

def clipboardshare_create(request):
    if request.method == 'POST':
        # print(f"{request.POST = }")
        posted_by = request.POST.get('posted_by') or 'anonymousUser'
        password = request.POST.get('password')
        title = request.POST.get('title')
        content = request.POST.get('content')
        
        if title and content:
            SecretClipboard.objects.create(
                password = my_hash(password) if password else None, 
                title=title, 
                content=content, 
                posted_by=posted_by
            )
        
        return redirect('/clipboard/')
    return render(request, 'clipboardShare/create.html')
