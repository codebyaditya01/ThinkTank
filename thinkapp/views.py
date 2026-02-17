from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login as auth_login  # Renamed to avoid conflict
from django.db.models import Count  # Added import for Count


# Create your views here.


def usersignup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'thinkapp/signup.html', {'form': form})



# Removed @login_required decorator from login view to prevent infinite loop
def userlogin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)  # Changed from login to auth_login
            return redirect('list')
    return render(request, "thinkapp/login.html")



def addquestion(request):
    form = QuestionForm()
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user 
            question.save()  
            return redirect('details', id=question.id)
    else:
        form = QuestionForm()
    return render(request, 'thinkapp/addques.html', {"form":form})



@login_required
def updateques(request, id):
    question = get_object_or_404(Questiondbase,id=id,user=request.user)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance = question)
        if form.is_valid():
            form.save()
            return redirect('details', id = question.id)
    else:
        form = QuestionForm(instance = question)
    return render(request, 'thinkapp/updateques.html', {"form":form, "question":question})



@login_required
def updateans(request, id):
    answer = get_object_or_404(Answerdbase, id = id, user=request.user)
    if request.method == "POST":
        form = AnswerForm(request.POST, instance = answer)
        if form.is_valid():
            form.save()
            return redirect('details', id = answer.question.id)
    else:
        form = AnswerForm(instance = answer)
    return render(request, 'thinkapp/updateans.html', {"form":form, "answer":answer})



@login_required
def deleteques(request, id):
    deleteques = get_object_or_404(Questiondbase, id = id, user=request.user)
    if request.method == "POST":
        deleteques.delete()
        return redirect('list')
    return render(request, 'thinkapp/deleteques.html', {"deleteques":deleteques})



@login_required
def deleteans(request, id):
    deleteans = get_object_or_404(Answerdbase, id = id, user=request.user)
    if request.method == "POST":
        deleteans.delete()
        return redirect('list')
    return render(request, 'thinkapp/deleteques.html', {"deleteans":deleteans})



def homelistpage(request):
    # Fixed: Used Count directly instead of models.Count
    all_data = Questiondbase.objects.all().order_by('-created_at').annotate(answerscount = Count('answers'))
    return render(request, 'thinkapp/homelistpage.html', {"all_data":all_data})


def details(request, id):
    question = Questiondbase.objects.get(id = id)
    answers = question.answers.all()
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            new_answer = form.save(commit=False)
            new_answer.user = request.user
            new_answer.question = question
            new_answer.save()
            return redirect('details', id=question.id)  # redirect to same page
    else:
        form = AnswerForm()

    context = {
        'question': question,
        'answers': answers,
        'form': form
    }
    return render(request, 'thinkapp/details.html', context)


@login_required
def comments(request, quesid, ansid):
    answer = Answerdbase.objects.get(id = ansid)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.answer = answer
            comment.save()
            form = CommentForm()
    else:
        form = CommentForm()
    all_comments = answer.comments.all().order_by("-commented_at")
    # Fixed: Changed template path from 'libraryapp/comment.html' to 'thinkapp/comment.html'
    return render(request, 'thinkapp/comments.html', {
        'form': form,
        'answer': answer,
        'all_comments': all_comments,
        'quesid': quesid
    })


@login_required
def delete_comment(request, quesid, ansid, comment_id):
    comment = get_object_or_404(
        Commentdbase,
        id=comment_id,
        user=request.user
    )

    if request.method == "POST":
        comment.delete()

    return redirect('comments', quesid=quesid, ansid=ansid)


@login_required
def voting(request):
    if request.method == "POST":
        answer_id = request.POST.get('id')
        value = int(request.POST.get('value'))
        answer = get_object_or_404(Answerdbase, id = answer_id)
        vote, created = Votingdbase.objects.get_or_create(user=request.user, answer=answer)
        vote.value = value
        vote.save()
        
        # Alag se upvotes aur downvotes calculate karna
        upvotes = answer.votes.filter(value__gt=0).count()     # value > 0 = upvote
        downvotes = answer.votes.filter(value__lt=0).count()   # value < 0 = downvote
        
        return JsonResponse({
            'upvotes': upvotes,
            'downvotes': downvotes,
        })
    else:
        return JsonResponse({'error': 'POST request required'}, status=400)
    


@login_required
def profile_view(request):
    try:
        # Try to get existing profile
        profile = Profiledbase.objects.get(user=request.user)
        is_update = True  # profile exists

        # Handle updating profile
        if request.method == "POST":
            form = ProfileForm(request.POST, instance=profile)
            if form.is_valid():
                form.save()
                return redirect('profileview')
        else:
            form = ProfileForm(instance=profile)

    except Profiledbase.DoesNotExist:
        profile = None
        is_update = False  # no profile exists

        # Handle creating profile
        if request.method == "POST":
            form = ProfileForm(request.POST)
            if form.is_valid():
                new_profile = form.save(commit=False)
                new_profile.user = request.user
                new_profile.save()
                return redirect('profileview')
        else:
            form = ProfileForm()

    # Stats for the profile (if it exists)
    total_questions = Questiondbase.objects.filter(user=request.user).count() if profile else 0
    total_answers = Answerdbase.objects.filter(user=request.user).count() if profile else 0

    context = {
        'profile': profile,
        'form': form,
        'is_update': is_update,
        'total_questions': total_questions,
        'total_answers': total_answers
    }

    return render(request, 'thinkapp/displayprofile.html', context)