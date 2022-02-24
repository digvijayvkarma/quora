from multiprocessing import context
from django.shortcuts import redirect, render
from django.http import HttpResponse
from mysqlx import Session
from .models import Question,User,Answer,Like
from .forms import QuestionForm,AnswerForm,LoginForm,SignUpForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session


# Create your views here.
def post_question(request,id=0):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            m = Question()
            m.question = form.cleaned_data['question']
            m.user = User.objects.get(id=request.session.get('user_id'))
            m.save()
            message="Your Question has been posted successfully. please check your homepage"
            return render(request, 'question.html', {'form': form,'message':message})
        else:
            form = QuestionForm()
            return render(request, 'question.html', {'form': form})
    else:
        form = QuestionForm()
        return render(request, 'question.html', {'form': form})

def post_answer(request,id=0):
    def liked(request, id):
        number_of_likes = Like.objects.filter(user__id__contains=request.session.get('user_id'), answer__id__contains=id).count()
        if number_of_likes > 0:
            return True 
        else:
            return False 
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            m = Answer()
            m.answer = form.cleaned_data['answer']
            m.question = Question.objects.get(pk = id)
            m.user = User.objects.get(id=request.session.get('user_id'))
            m.save()
            form = AnswerForm()
            q=Question.objects.filter(pk=id)
            a=Answer.objects.filter(question__id__contains=id)
            message="Your Answer has been posted successfully"
            # return render(request, 'answer.html', {'form': form,'question':q[0],'answer':a})
            return redirect('/answer/'+ str(id))
        else:
            form = AnswerForm()
            a=Answer.objects.filter(question__id__contains=id)
            message="Please type valid information"
            return render(request, 'answer.html', {'form': form,'question':q[0],'answer':a})
    else:
        q=Question.objects.filter(pk=id)
        a=Answer.objects.filter(question__id__contains=id)
        c=list(a)
        answer_list= []
        for ans in c:
            already_liked=liked(request,id=ans.id)
            nlikes=Like.objects.filter(answer__id__contains=ans.id).count()
            x={
                "id":ans.id,
                "answer": ans.answer,
                "question": ans.question,
                "user": ans.user,
                "nlikes": nlikes,
                "already_liked":already_liked
            }
            answer_list.append(x)
        form = AnswerForm()
        return render(request, 'answer.html', {'form': form,'question':q[0],'answer':answer_list,'like':like})

def login(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'loginpage.html',{'form': form})
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            userName = form.cleaned_data['login_id']
            password = form.cleaned_data['password']
            q=User.objects.filter(login_id=userName, password=password)
            if q.count()>0:
                request.session['user']= q[0].firstName
                request.session['login_id']= q[0].login_id
                request.session['user_id']= q[0].id
                request.user=q[0]
                return redirect('/home/')
            else:
                message = "Wrong Credential!"
                return render(request, 'loginpage.html', context={'form':form,'message':message})
        else:
            message = "Invalid Form"
            return render(request, 'loginpage.html', context={'message':message})
    else:
        return redirect('/')

def logout(request):
    Session.objects.all().delete()
    request.session['user_id']= None
    message = "logout succesffully"
    return render(request, 'index.html',{'message':message})
        

def home_page(request):
    if request.session['user_id'] is not None:
        firstname=request.session['user']
        q=Question.objects.filter()
        return render(request, 'home_page.html', context={'firstname':firstname, 'questionlist':q})
    else:
        message = "Please Login first!"
        return render(request, 'index.html', context={'message':message})


def index(request):
    return render(request, 'index.html')

def like(request,id,qid):
    
    new_like, created = Like.objects.get_or_create(user_id=request.session.get('user_id'),answer_id=id)
    if not created:
        Like.objects.get(user_id=request.session.get('user_id'),answer_id=id).delete()
        return redirect('/answer/'+ str(qid))
    else:
        return redirect('/answer/'+ str(qid))
            
    


def SignUp(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            m = User()
            m.login_id = form.cleaned_data['login_id']
            m.firstName = form.cleaned_data['firstName']
            m.lastName = form.cleaned_data['lastName']
            m.password = form.cleaned_data['password']
            m.save()
            form = SignUpForm()
            message = "Signed Up Successfully!"
            return render(request, 'signup.html', {'form': form,'message':message})
        else:
            form = SignUpForm()
            return render(request, 'signup.html', {'form': form})

    else:
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})
