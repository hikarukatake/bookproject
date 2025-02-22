# URLとビューを結びつけるために使う
# つまり下にあるurlと画面を結びつけるためのかんすう
from django.urls import path
# 同じアプリ内のファイルをインポート つまりviewsをインポートしてそのなかにあるListBookViewを使えるようにしている
from . import views
from .views import IndexList
# urlに対応する画面を表示するためにやってる
# 'book/'はhttp://127.0.0.1:8000/book/ にアクセスしたときにどこを写すかをかいている
# views.ListBookView.as_view()これがうえでインポートしてきたviews.pyにあるListBookViewを実行している
# nameは名前をつけている
urlpatterns = [
    path('', views.ListBookView.as_view(), name='list-book'),
    path('list-book-form/', IndexList.as_view(), name='list-book-form'),
    path('book/<int:pk>/detail/', views.DetailBookView.as_view(), name='detail-book'),
    path('book/create/', views.CreateBookView.as_view(), name='create-book'),
    path('book/<int:pk>/delete/', views.DeleteBookView.as_view(), name='delete-book'),
    path('book/<int:pk>/update/', views.UpdateBookView.as_view(), name='update-book'),
    path('book/<int:book_id>/review/', views.CreateReviewView.as_view(), name='review'),
]
