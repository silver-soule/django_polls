from django.http import HttpResponseRedirect, HttpResponse,JsonResponse,HttpRequest
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from .models import Question,Choice,Comments
from django.utils import timezone
from .forms import DetailForm,SignupForm,LoginForm,CommentForm,PasswordResetForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from mysite.tasks import sendmail

@login_required
def index(request):
    co=Choice.objects.all()
    valid_question_list=[]
    final_list=[]
    valid_questions_by_time=Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:]
    for c in co:
        if  c.question not in valid_question_list:
            valid_question_list.append(c.question)
    length_of_valid_question_list=len(valid_question_list) 
    for question in valid_questions_by_time:
        if question in valid_question_list:
            final_list.append(question)
    latest_question_list = final_list
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

@login_required
def detail(request, question_id):
    form=DetailForm(question_id,request.POST)
    question = get_object_or_404(Question.objects.filter(pub_date__lte=timezone.now()), pk=question_id)
    return render(request, 'polls/detail.html', {'question': question,'form':form})

@login_required
def results(request, question_id):
    question = get_object_or_404(Question.objects.filter(pub_date__lte=timezone.now()), pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        if request.method=='POST':
            form=DetailForm(question_id,request.POST)
            if form.is_valid():
                print(form.cleaned_data['choice_field'])
                choice_id=form.cleaned_data['choice_field']  
        selected_choice = question.choice_set.get(pk=choice_id)
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a valid choice.",
            'form':form
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def signup(request):
    form=SignupForm()
    return render(request,'polls/signup.html',{'form':form})


def signedin(request):
    if request.method=='POST':
        form=SignupForm(request.POST)
        if form.is_valid():
            person=form.person_save()
            url=reverse('polls:login')
            return JsonResponse({'success':url})
        jsonerror=form.errors
        return JsonResponse({'failiure':jsonerror})

def login(request):
    form=LoginForm()

    return render(request,'polls/login.html',{'form':form})

def loggedin(request):
    if request.method=='POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            user=form.person_validate()
            if user is not False:
                auth.login(request, user)
                url=reverse('polls:index')
                return JsonResponse({'success':url})
            else:
                return JsonResponse({'invalid data':'Invalid username or password'})
        jsonerror=form.errors
        return JsonResponse({'failiure':jsonerror})

@login_required
def loggedout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('polls:signup'))

def imageview(request):
    data={'1':'http://media.caranddriver.com/images/media/51/25-cars-worth-waiting-for-lp-ford-gt-photo-658253-s-original.jpg',
          '2':'http://media.caranddriver.com/images/media/51/25-cars-worth-waiting-for-lp-mclaren-p14-photo-658259-s-original.jpg'}
    return JsonResponse(data)

def loadui(request):
    result=add.delay(4,4)
    return render(request,'polls/imageview.html')

@csrf_exempt
def getcomments(request):
    comment_list=[]
    for comment in Comments.objects.all():
        comment_list.append({'id':comment.id,
                            'author':comment.author,
                            'text':comment.comment_text})
        print(comment.id)
    return JsonResponse({'stuff':comment_list})

@csrf_exempt
def comments(request):
    if request.method=='POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            comment=form.store_comment()
            print("successful save")
            return JsonResponse({'success!':'yay'})
    else:
        return render(request,'polls/comments.html')

@csrf_exempt
def password_reset(request):
    if request.method=='POST':
        print("a")
        form=PasswordResetForm(request.POST)
        if form.is_valid():
            print("b")
            sendmail.delay(form.cleaned_data['email_id'])
            return render(request,'polls/login.html')
    else:
        return render(request,'polls/password-reset.html')







