from django.db import models
from django.contrib.sites.models import Site #siteをimport

#siteconfigを作成
class SiteConfig(models.Model):
  site = models.OneToOneField(Site,verbose_name = 'Site',on_delete = models.PROTECT)
  
  #モデルの定義
  meta_title = models.CharField('meta_title',max_length=100)
  meta_description = models.CharField('meta_description',max_length=300)
  meta_keywords = models.CharField('SEOキーワード',max_length=300)
  author = models.CharField('管理者',max_length = 30)
  top_title = models.CharField('Topページタイトル',max_length=100)
  top_subtitle = models.CharField('Topページサブタイトル',max_length=200)

  #モデルのタイトルを戻り値として返す
  def __str__(self):
    return self.meta_title