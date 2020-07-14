from django.views.generic import ListView, DetailView
from bookmark.models import Bookmark


class BookmarkLV(ListView):
    model = Bookmark


# 리스트 뷰로부터 받아오겠다. 쓸 수 있는 것은


class BookmarkDV(DetailView):
    model = Bookmark

