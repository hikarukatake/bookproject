# renderはHTMLを表示するときに使う関数
from django.shortcuts import render
# ListViewなどの便利なビュー基礎クラスを使えるようにしている
# データの一覧を表示をDjango側で簡単に***generic***がやってくれる処理
from django.views import generic
# reverse_lazyはlist-bookというurlを探しています
# ふォーム送信後、このURLにリダイレクトという
# この処理をいつでも探すのがreverse_lazy(クラスベースビュー)
# 即時解決させようとするのがreverse(関数ベースびゅー)
from django.urls import reverse, reverse_lazy
# データベースからShelfモデルをインポートしてデータを使える用にしている
from .models import Shelf, Review
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg
from django.core.paginator import Paginator
from django.views.generic import UpdateView
from django.views.generic import ListView
from django.db.models import Q # get_queryset()用に追加
from django.contrib import messages #　検索結果のメッセージのため追加
from django.shortcuts import render
from .models import Book

#  一覧ページを汎用ビューを使って表示するための処理
#  ListBookViewというクラスを作成
#  レンダリングを行うための処理   ***レンダリングとはデータを視覚的な状態で表示するためのプロセス(作業)
class ListBookView(generic.ListView):
    # urls.pyのパスどうりに/bookにアクセスしたらListBookViewが処理をおこなうとurls.pyに書いてある
    template_name = 'book/book_list.html'
    model = Shelf
    # 変数名をShelfにしている
    context_object_name = 'Shelf'
    queryset = Shelf.objects.all().order_by('-id')  # 登録順（降順）に並べ替え

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # レビュー平均でソートして上位3冊を取得
        ranking_list = (
            Shelf.objects.annotate(avg_rating=Avg('review__rate')).order_by('-avg_rating')[:3]
        )
        context['ranking_list'] = ranking_list
        return context
class DetailBookView(generic.DetailView):
    template_name = 'book/book_detail.html'
    model = Shelf
    context_object_name = 'Shelf'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 本に関連するレビューを取得
        reviews = Review.objects.filter(book=self.object).order_by('-id')  # 最新のレビュー順
        paginator = Paginator(reviews, 3)  # 1ページに3件表示
        page_number = self.request.GET.get('page')
        context['reviews'] = paginator.get_page(page_number)
        return context

class CreateBookView(LoginRequiredMixin, generic.CreateView):
    template_name = 'book/book_create.html'
    model = Shelf
    context_object_name = 'Shelf'
    fields = ('title', 'text', 'category', 'thumbnail')
    success_url = reverse_lazy('list-book')

    def form_valid(self, form):
        form.instance.user = self.request.user  # ログイン中のユーザーを設定
        return super().form_valid(form)

class DeleteBookView(LoginRequiredMixin, generic.DeleteView):
    template_name = 'book/book_confirm_delete.html'
    model = Shelf
    context_object_name = 'Shelf'
    success_url = reverse_lazy('list-book')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            raise PermissionDenied('削除権限がありません。')
        return super(DeleteBookView, self).dispatch(request, *args, **kwargs)

class UpdateBookView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'book/book_update.html'
    model = Shelf
    context_object_name = 'Shelf'
    fields = ('title', 'text', 'category', 'thumbnail')
    success_url = reverse_lazy('list-book')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            raise PermissionDenied('編集権限がありません。')
        return super(UpdateView, self).dispatch(request, *args, **kwargs)

class CreateReviewView(LoginRequiredMixin, generic.CreateView):
    model = Review
    fields = ('book', 'title', 'text', 'rate')
    template_name = 'book/review_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = Shelf.objects.get(pk=self.kwargs['book_id'])
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('detail-book', kwargs={'pk':self.object.book.id})

from django.views.generic import ListView
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render
from .models import Shelf

class IndexList(ListView):
    template_name = 'report/book_list-form.html'
    model = Shelf
    context_object_name = 'Shelf'

    def get_queryset(self):
        query = self.request.GET.get('q', '')  # 検索キーワードを取得
        if query:
            return Shelf.objects.filter(Q(title__icontains=query)).order_by('-id')
        return Shelf.objects.all().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '')  
        if query:
            messages.info(self.request, f"「{query}」の検索結果")
        return context

