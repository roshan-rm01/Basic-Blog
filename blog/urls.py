from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = "blog"

urlpatterns = [
    path('', views.home, name="home"),
    path('login', views.login_user, name="login"),
    path('about', TemplateView.as_view(template_name='../BlogTemplates/about.html'), name="about"),
    path('add_post', views.add_post, name="add_post"),
    path('post_list', views.post_list, name="post_list"),
    path('post/<slug:slug>', views.post_detail, name="post_detail"),
    path('monte_carlo', TemplateView.as_view(template_name='../BlogTemplates/monte-carlo.html'), name="monte_carlo"),
    path('automation', TemplateView.as_view(template_name='../BlogTemplates/automation.html'), name="automation"),
    path('stock_market', TemplateView.as_view(template_name='../BlogTemplates/stock-market.html'), name="stock_market"),
    path('error', TemplateView.as_view(template_name='../BlogTemplates/error.html'), name="error")
]