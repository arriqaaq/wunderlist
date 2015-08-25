from django.shortcuts import render
from wunderlist.models import Category
from wunderlist.models import Item
from wunderlist.forms import CategoryForm, PageForm, CommentForm
from django.shortcuts import redirect
from django.core.context_processors import csrf
from django.shortcuts import redirect, render_to_response, get_object_or_404
from taggit.models import Tag
import unicodedata


def index(request):

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    category_list = Category.objects.all()
    context_dict = {'categories' : category_list}
    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.

    return render(request, 'wunderlist/index.html', context_dict)

def category(request, category_name_slug):

    # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {}

    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name

        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.
        pages = Item.objects.filter(category=category)

        # Adds our results list to the template context under name pages.
        context_dict['pages'] = pages
        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = category
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass

    # Go render the response and return it to the client.
    return render(request, 'wunderlist/category.html', context_dict)

def page(request, category_name_slug, page_name_slug):

    # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {}

    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises an exception.
        page = Item.objects.get(title=page_name_slug)
        #if request.method=='POST':
        #p.category = request.POST.get('category',"")
         #   page.title = request.POST.get('title'," ")
          #  page.subtask = request.POST.get('subtask'," ")
           # page.notes = request.POST.get('notes'," ")
            #page.dueDate = request.POST.get('dueDate',"")
            #page.tags = request.POST.get('tags'," ")
            #print "finally: ",request.POST.get('tags'," ")
            #page.taskDone = request.POST.get('taskDone'," ")
        
        context_dict['page'] = page
        context_dict['tags'] = Tag.objects.all()
        post = get_object_or_404(Item, title=page_name_slug)
        form = CommentForm(request.POST or None)
        context_dict['post'] = post
        context_dict['form'] = form
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect(request.path)
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template displays the "no category" message for us.
        pass
    # Go render the response and return it to the client.
    return render(request, 'wunderlist/page.html', context_dict)




def add_category(request):
    if request.method=='POST':
        form=CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)

            return index(request)

        else:
            print form.errors

    else:
        form=CategoryForm()

    return render(request, 'wunderlist/add_category.html',{'form': form})

def add_Item(request):
    #try:
     #   cat = Category.objects.get(slug=category_name_slug)
    #except Category.DoesNotExist:
     #           cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            form.save(commit=True)

            return index(request)
        else:
            print form.errors
    else:
        form = PageForm()

    context_dict = {'form':form} #'category': cat}

    return render(request, 'wunderlist/add_Item.html', context_dict)


def test(request, person_id):
    total=[]
    tags_str=''
    p=Item.objects.get(pk=person_id)
    #print p.tags
    #print "yay!!!", request.POST.get()
    #is_private = request.POST.get('is_private', False)
    if request.method=='POST':
        #p.category = request.POST.get('category',"")
        p.title = request.POST.get('title'," ")
        print "entereeeeeeeeeeeeeeeedddddddd"
        p.subtask = request.POST.get('subtask'," ")
        p.notes = request.POST.get('notes'," ")
        p.dueDate = request.POST.get('dueDate',"")
        k=request.POST.get('tags'," ").encode('ascii','ignore')
        tags_str+=k
        total=tags_str.split(",")
        print total
        for i in total:
            p.tags.add(i)

        p.taskDone = request.POST.get('taskDone'," ")
        p.save()
    context_dict = {'person': p}   
    return render(request, 'wunderlist/edit.html')
    #return index(request)
    #return redirect('/wunderlist/')

def view_post(request, slug):
    post = get_object_or_404(Item, slug=slug)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        return redirect(request.path)
    return render_to_response('wunderlist/page.html',
                              {
                                  'post': post,
                                  'form': form,
                              },
                              context_instance=RequestContext(request))


def search(request):
    if 'q' in request.GET:
        cns=request.GET['q']
    else:
        cns=' '
    context_dict={}
    print "CNS: ", cns
    try:
        pages=Item.objects.filter(tags__name__in=[cns])
        print pages
        context_dict['pages']=pages
    except:
        pass

    return render(request, 'wunderlist/search.html', context_dict)
