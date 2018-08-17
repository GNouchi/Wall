from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
# USER ID SHOULD ALWAYS BE IN SESSION

# ------ INDEX ------ #
def wall(request):
    if 'user_id' not in request.session or 'instance' not in request.session:
        return redirect ('/')
    current_user=User.objects.get(id = request.session['user_id'])
    all_messages = Message.objects.all()
    all_comments = Comment.objects.all()
    # print(all_comments)
    if request.session['instance'] == 'registration' :
        dis = "Welcome newly Registered User " +current_user.first_name 
    elif request.session['instance'] == 'login':
        dis = "Welcome back " + current_user.first_name
    context=  {
        'current_user':  current_user,
        'instance' : dis,
        'all_messages' : all_messages,
        'all_comments':all_comments,
    }    
    test_message = Message.objects.get (id =1)
    test_User = User.objects.get (id =1)
    # print(type(test_message) == Message)
    # print(type(test_User) == User)
    return render(request, 'wall.html',context)

# ------ start Create methods ------ #

def message(request):
    print("HELLO THIS IS MESSAGE")
    result = Message.objects.validateStr(request.POST)
    print("*"*50)
    if len(result['errors']) > 0:
        print(" ERRORS are : ",  result['errors'], "**********")
        for error in result:
            messages.error(request,result[error] )
        print("*"*50)
        return redirect('/wall')  
# erase after dev
    else:
        print("no errors")    
        print("*"*50)
    return redirect('/wall')

def comment(request):
    print("HELLO THIS IS COMMENT")
    result = Comment.objects.validateStr(request.POST)
    print("*"*50)
    if len(result['errors']) > 0:
        print(" ERRORS are : ",  result['errors'], "**********")
        for error in result:
            messages.error(request,result[error] )
        print("*"*50)
        return redirect('/wall')  
# erase after dev
    else:
        print("no errors")    
        print("*"*50)
    return redirect('/wall')


# ------start Destroy methods ------ #

def destroycomment(request):
    if request.method != 'POST':
        return redirect('/wall')
    else:
        owner = Comment.objects.get(id = request.POST['comment_id'])
        # print(owner.user.id)
        # print(request.session['user_id'])
        # print (owner.user.id == request.session['user_id'])
        if owner.user.id == request.session['user_id']:
            owner.delete()
        else:
            messages.error(request, "YOU DONT OWN THAT" )
        # print("owner type ", type(owner.id))
        # print("form type ", type(request.session['user_id']))
        return redirect('/wall')

def destroymessage(request):
    if request.method != 'POST':
        return redirect('/wall')
    else:
        owner = Message.objects.get(id = request.POST['message_id'])
        print (owner.user.id)
        print(request.session['user_id'])
        print (owner.user.id == request.session['user_id'])
        if owner.user.id == request.session['user_id']:
            owner.delete()
        else:
            messages.error(request, "YOU DONT OWN THAT" )
        print("owner type ", type(owner.id))
        print("form type ", type(request.session['user_id']))
        return redirect('/wall')

# ----------------------------------------------------------------------------------------------------------
# ----------------------------------------------LOGIN AND REG-----------------------------------------------
# ----------------------------------------------------------------------------------------------------------

def index(request):
    request.session.clear()
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        print("-----------------------------at LOGIN----------------------------")
        result = User.objects.LoginValidator(request.POST)
        if len(result['errors']) > 0:
            print("errors are  : ",  result['errors'])
            for error in result['errors']:
                messages.error(request, error)
            return redirect('/')
        else:
            request.session['user_id']  = result['user_id']
            request.session['instance'] = 'login'
            return redirect('/success')
    else:
        return redirect('/')
    return redirect('/')

def register(request):
    if request.method == 'POST':
        print("-----------------------------at REGISTER----------------------------")
        result = User.objects.validateUser(request.POST)
        if len(result['errors']) > 0:
            print("errors are  : ",  result['errors'])
            for error in result['errors']:
                messages.error(request, error)
            return redirect('/')
        else:
            request.session['user_id']  = result['user_id']
            request.session['instance'] = 'registration'
            return redirect('/success')
    else:
        return redirect('/')

def success(request):
    if 'user_id' not in request.session or 'instance' not in request.session:
        return redirect ('/')
    return redirect('/wall')

def logout(request):
    request.session.clear()
    return redirect ('/')
