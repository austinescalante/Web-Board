from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404,redirect
from .models import Board,Topic,Post
from django.contrib.auth.models import User
from .forms import NewTopicForm
# Create your views here.

def home(request):
    boards= Board.objects.all()
    return render(request, 'home.html', {'boards':boards })

#Because we used the (?P<pk>\d+) regex, the keyword argument in the board_topics must be named pk.

#Django has a shortcut to try to get an object, or return a 404 with the object does not exist.
def board_topics(request,pk):
    board = get_object_or_404(Board, pk=pk)
    return render(request, 'topics.html', {'board': board})

def new_topic(request,pk):
    board = get_object_or_404(Board, pk=pk)
    user = User.objects.first()  # TODO: get the currently logged in user

    #First we check if the request is a POST or a GET. If the request came from a POST, it means the user is submitting some data to the server. 
    # So we instantiate a form instance passing the POST data to the form: form = NewTopicForm(request.POST).
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
    #we ask Django to verify the data, check if the form is valid if we can save it in the database: if form.is_valid():. 
    # If the form was valid, we proceed to save the data in the database using form.save(). 
    # The save() method returns an instance of the Model saved into the database. 
    # So, since this is a Topic form, it will return the Topic that was created: topic = form.save(). 
    # After that, the common path is to redirect the user somewhere else, both to avoid the 
    # user re-submitting the form by pressing F5 and also to keep the flow of the application.
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user
            )
            return redirect('board_topics', pk=board.pk)  # TODO: redirect to the created topic page
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})


