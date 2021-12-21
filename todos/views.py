from django.http.request import HttpRequest
from django.shortcuts import render, redirect
from django.http import HttpRequest
from .models import Todo
from django.conf import settings
template = {1: '\nNew Todo: \n', 2: '\nDelete Todo: \n', 3: '\nUpdate Todo: \n'}

# To list all todo items
def list_todo_items(request):
    context = { 'todo_list': Todo.objects.all()}
    return render(request, 'todos/todo_list.html', context)

# To add a todo item to the list
def insert_todo_item(request: HttpRequest):
    content = request.POST['content']
    todo = Todo(content = content, is_complete = False)
    todo.save()

    # Send message Alert to user using TWILIO API
    alert_user(1,content)
    return redirect('/todos/list/')

# To delete existing todos with ID
def delete_todo_item(request, todo_id):
    todo_to_delete = Todo.objects.get(id = todo_id)
    todo_to_delete.delete()

    # Send message Alert to user using TWILIO API
    alert_user(2,todo_to_delete.content)
    return redirect('/todos/list/')

# To update existing todo item with ID
def update_todo_item(request, todo_id):
    todo_to_update = Todo.objects.get(id = todo_id)
    todo_to_update.is_complete = not todo_to_update.is_complete
    todo_to_update.save()

    # Send message Alert to user using TWILIO API
    complt_status = 'Complete'
    if not todo_to_update.is_complete:
        complt_status = 'Incomplete'
    alert_user(3,todo_to_update.content + '\n' + 'Marked as ' + complt_status)
    return redirect('/todos/list/')

def alert_user(which_template, content):
    settings.TWILIO_CLIENT.messages \
        .create(
                body=template[which_template] + content,
                from_=settings.TWILIO_FROM,
                to='+918800669070'
                )