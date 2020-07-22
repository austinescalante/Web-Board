from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404,redirect
from .models import Board,Topic,Post
from django.contrib.auth.models import User
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

    if request.method == 'POST':
        subject = request.POST['subject']
        message = request.POST['message']

        user = User.objects.first()  # TODO: get the currently logged in user
        #Created a Topic Instance
        topic = Topic.objects.create(
            subject=subject,
            #we set the board field in Topic model, which is a ForeignKey(Board). 
            #Board instance is aware that it has an Topic instance associated with it.
            board=board,
            starter=user
        )

        post = Post.objects.create(
            message=message,
            topic=topic,
            created_by=user
        )

        return redirect('board_topics', pk=board.pk)  # TODO: redirect to the created topic page

    return render(request, 'new_topic.html', {'board': board})

