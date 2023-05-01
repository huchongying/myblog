from urllib import request

from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from django.db.models import Q, F
from django.views.decorators.csrf import csrf_exempt

from blog.models import Category, Post


@csrf_exempt
# Create your views here.
def index(request):
    # 首页
    post_list = Post.objects.all()   # 查询到所有的文章,queryset
    # 分页方法
    paginator = Paginator(post_list, 2)  # 第二个参数2代表每页显示几个
    page_number = request.GET.get('page')   # http://assas.co/?page=1 (页码)
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, 'blog/index.html', context)


@csrf_exempt
def category_list(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    # 获取当前分类下的所有文章
    posts = category.post_set.all()
    context = {'category': category, 'post_list': posts}
    return render(request, 'blog/list.html', context)


@csrf_exempt
def post_detail(request, post_id):
    # 文章详情页
    post = get_object_or_404(Post, id=post_id)

    # 用文章id来实现的上下篇
    prev_post = Post.objects.filter(id__lt=post_id).last()  # 上一篇
    next_post = Post.objects.filter(id__gt=post_id).first()  # 下一篇

    Post.objects.filter(id=post_id).update(pv=F('pv') + 1)  # 更新阅读量
    # 用发布日期来实现上下篇
    # date_prev_post = Post.objects.filter(add_date__lt=post.add_date).last()
    # date_next_post = Post.objects.filter(add_date__gt=post.add_date).first()

    context = {'post': post, 'prev_post': prev_post, 'next_post': next_post}
    return render(request, 'blog/detail.html', context)


@csrf_exempt
def search(request):
    """ 搜索视图 """
    keyword = request.GET.get('keyword')  # 获取表单中输入的值

    # 没有搜索默认显示所有文章
    if not keyword:
        post_list = Post.objects.all()
    else:
        # 包含查询的方法，用Q对象来组合复杂查询，title__icontains 他两个之间用的是双下划线（__）链接
        post_list = Post.objects.filter(
            Q(title__icontains=keyword) | Q(desc__icontains=keyword) | Q(content__icontains=keyword))

    context = {
        'post_list': post_list
    }
    return render(request, 'blog/index.html', context)


@csrf_exempt
def archives(request, year, month):
    # 文章归档列表页
    post_list = Post.objects.filter(add_date__year=year, add_date__month=month)
    context = {'post_list': post_list, 'year': year, 'month': month}
    return render(request, 'blog/archives_list.html', context)

