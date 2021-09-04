from django.shortcuts import render
import markdown2
from random import randint
from django import forms  
from . import util


class NewPost(forms.Form):
    post_title = forms.CharField(label="Title", max_length = 200)
    post_body = forms.CharField(widget=forms.Textarea(attrs={'style': 'width:500px; heigth:500px'}))
   

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

def lookup(request):    
    query = request.GET.get('query')
    entries = util.list_entries()
    if query in entries:
        page_html = markdown2.markdown(util.get_entry(query))
        return render(request, "encyclopedia/article.html", {
            "page_content": page_html,
            "page_title": query
        })
    else:
        search_results = []
        for entry in entries:        
            if query in entry:
                search_results.append(entry)
        return render(request, "encyclopedia/lookup.html", {
            "search_results": search_results,
        })

def random(request): 
    entries = util.list_entries()
    r = randint(0, len(entries) - 1)
    rand_ent_title = entries[r]   
    rand_ent = util.get_entry(rand_ent_title) 
    rand_ent_html = markdown2.markdown(rand_ent)
    return render(request, "encyclopedia/article.html", {
        "page_content": rand_ent_html,
        "page_title": rand_ent_title
    })

def article(request, title):
    if util.get_entry(title) == None:
        return render(request, "encyclopedia/404.html", {
        })
    else:
        page_html = markdown2.markdown(util.get_entry(title))
        return render(request, "encyclopedia/article.html", {
            "page_content": page_html,
            "page_title": title
        })

def add(request):
    if request.method == 'GET':
        return render(request, "encyclopedia/add.html", {
        "post_form": NewPost()
    })
    if request.method == 'POST':
        post_title = request.POST.get('post_title')        
        post_body = request.POST.get('post_body')
        existing_entries = util.list_entries()
        warning = "Warning: This entry already exists!"
        if post_title in existing_entries:
            return render(request, "encyclopedia/add.html", {
                "warning": warning,
                "post_form": NewPost()
            })
        else:
            util.save_entry(post_title, post_body)
            new_entry_html = markdown2.markdown(util.get_entry(post_title))
            return render(request, "encyclopedia/article.html", {
                "page_title": post_title,
                "page_content": new_entry_html,
            })

def edit(request, title):
    if request.method == "GET":
        page_md = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "page_md": page_md,
            "title": title
        })
    else:
        post_body = request.POST.get("textarea")
        util.save_entry(title, post_body)
        updated_entry = util.get_entry(title)
        updated_entry_html = markdown2.markdown(updated_entry)
        return render(request, "encyclopedia/article.html", {
            "page_title": title,
            "page_content": updated_entry_html
        })




