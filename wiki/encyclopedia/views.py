from django.shortcuts import render, redirect
from django.http import HttpResponse
import markdown2
import random
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
    
def titles(request, title):
    entries = util.list_entries()
    
    matched_title = next((e for e in entries if e.lower() == title.lower()), None)
    
    if matched_title is None:
        return HttpResponse(f"{title} page not found.")
    
    entry = util.get_entry(matched_title)
    html = markdown2.markdown(entry)
    return render(request, "encyclopedia/entry.html", {"title": matched_title, "content": html})

    
def search(request):
    query = request.GET.get("q")
    entries = util.list_entries()
    if query in entries:
        return redirect("titles", title=query)
    results = [entry for entry in entries if query.lower() in entry.lower()]
    return render(request, "encyclopedia/search.html", {
        "results": results,
        "query": query
    })

def create(request):
    if request.method == "GET":
        return render(request, "encyclopedia/create.html")
    elif request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        content_with_heading = f"# {title}\n\n{content}"
        util.save_entry(title, content_with_heading)
        return redirect("titles", title=title)

def edit(request, title,):
    entry = util.get_entry(title)
    if request.method == "GET":
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": entry
        })
    elif request.method == "POST":
        content = request.POST.get("content")
        util.save_entry(title, content)
        return redirect("titles", title=title)
    
def random_page(request):
    entries = util.list_entries()
    random_title = random.choice(entries)
    return redirect("titles", title=random_title)