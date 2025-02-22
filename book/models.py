# モデルを作るためのじゅんび
# モデル = データベースの設計図
from django.db import models
from .consts import MAX_RATE
RATE_CHOICES = [(x, str(x)) for x in range(0, MAX_RATE + 1)]
# カテゴリの選択肢を定義
CATEGORY = (
    ('business', 'ビジネス'),
    ('life', '生活'),
    ('hobby', '趣味'),
    ('other', 'その他'),
)

# データベースのテーブルをつくっている
# Shelfは本棚で***Shelf***というモデルを作ることができる
class Shelf(models.Model):
    # models.CharFieldは短いタイトルの文字列を保存するフィールド
    title = models.CharField(max_length=100)
    # models.TextFieldは長い文章を保存するフィールド
    text = models.TextField()
    # Shelfモデルに画像を扱うためのフィールドを追加
    thumbnail = models.ImageField(null=True, blank=True)
    # models.CharFieldは短いカテゴリの文字列を保存
    category = models.CharField(
        max_length=100,
        # 事前に定義したカテゴリしか選べない(うえで定義したモデルのカテゴリ)
        choices = CATEGORY,
        )
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    # タイトルを表示するということで __str__は表示する
    def __str__(self):
        return self.title

class Review(models.Model):
    book = models.ForeignKey(Shelf, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField()
    rate = models.IntegerField(choices=RATE_CHOICES)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    def __str__(self):
        pass
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    published_date = models.DateField()

    def __str__(self):
        return self.title
