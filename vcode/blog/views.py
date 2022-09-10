from email import message
from multiprocessing import context, parent_process
from pyexpat.errors import messages
from django.contrib import messages
from urllib import request
from django.shortcuts import render, HttpResponse, redirect
from blog.models import Post, BlogComment
from blog.templatetags import extras

# Create your views here.
def blogHome(request):
    allPosts = Post.objects.all()
    context = {'allPosts':allPosts}
    return render(request, 'blog/blogHome.html', context)
    

def blogPost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    post.views = post.views + 1
    post.save()

    comments = BlogComment.objects.filter(post=post, parent=None)
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict={}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]
        else:
            replyDict[reply.parent.sno].append(reply)

    # print(replyDict)
    # print(comments,replies )

    context = {'post': post, 'comments':comments, 'user':request.user, 'replyDict':replyDict}
    return render(request, 'blog/blogPost.html', context)

def postComment(request):
    if request.method=='POST':
        comment = request.POST.get("comment")
        user = request.user
        postSno = request.POST.get("postSno")
        post = Post.objects.get(sno=postSno)
        parentSno =  request.POST.get("parentSno")
        
        if parentSno == "":
            comment = BlogComment(comment=comment, user=user, post=post)
            comment.save()
            messages.success(request, "Your Comment has been add successfully")
        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comment = BlogComment(comment=comment, user=user, post=post,parent=parent)
            comment.save()
            messages.success(request, "Your reply has been add successfully")
    return redirect(f"/blog/{post.slug}") # here f means refresh the page
