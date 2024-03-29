from django.urls import path 
from core.apps.blog.views.dashboard.author.dashboard_views import home

# Core Django imports.
from django.urls import path

# Blog application imports.
from core.apps.blog.views.blog.article_views import (
    ArticleListView,
    ArticleDetailView,
    ArticleSearchListView,
    TagArticlesListView,
)

from core.apps.blog.views.blog.category_views import (
    CategoryArticlesListView,
    # CategoriesListView,
    CategoryCreateView,
    CategoryUpdateCreateView,
)

from core.apps.blog.views.blog.author_views import (
    AuthorArticlesListView,
    AuthorsListView,
)

# from core.apps.blog.views.blog.comment_views import (
#     CommentCreateView,
#     ArticleCommentList
# )

from core.apps.blog.views.dashboard.author.dashboard_views import (
    ArticleWriteView,
    ArticleUpdateView,
    ArticleDeleteView,
    ArticlePublishView,
    AuthorWrittenArticlesView,
    AuthorPublishedArticlesView,
    AuthorDraftedArticlesView,
    AuthorDeletedArticlesView,
)

from core.apps.blog.views.dashboard.author.author_profile_views import (
    AuthorProfileUpdateView,
    AuthorProfileView,
)

app_name = "blog"


urlpatterns = [
    
  path('',ArticleListView.as_view(), name = "home"),
      # /search/?q=query/
    path(
        'search/',
        ArticleSearchListView.as_view(),
        name='article_search_list_view'

     ),

    # ARTICLE URLS #

    # /ho
    # path(
    #     route='',
    #     view=ArticleListView.as_view(),
    #     name='home'
    # ),

    # /article/<str:slug>/
    path(
        route='<str:slug>/',
        view=ArticleDetailView.as_view(),
        name='article_detail'

    ),



    # /tag/<str:tag_name>/
    path(
        route='tag/<str:tag_name>/articles',
        view=TagArticlesListView.as_view(),
        name="tag_articles"
    ),


    # AUTHORS URLS #

    # /authors-list/
    path(
        route='authors/list/',
        view=AuthorsListView.as_view(),
        name='authors_list'
    ),

    # /author/<str:username>/
    path(
        route='author/<str:username>/articles',
        view=AuthorArticlesListView.as_view(),
        name='author_articles'
     ),


    # CATEGORY URLS #

    # category-articles/<str:slug>/
    path(
        route='<str:slug>/articles',
        view=CategoryArticlesListView.as_view(),
        name='category_articles'
    ),

    # /categories-list/
    # path(
    #     route='categories/list/',
    #     view=CategoriesListView.as_view(),
    #     name='categories_list'
    # ),

    # /category/new/
    path(
        route='category/create/',
        view=CategoryCreateView.as_view(),
        name="category_create"
    ),

    # /category/<str:slug>/update/
    path(
        route='category/<str:slug>/update/',
        view=CategoryUpdateCreateView.as_view(),
        name="category_update"
    ),




    # COMMENT URLS #

    # # /comment/new/
    # path(
    #     route='comment/new/<str:slug>/',
    #     view=CommentCreateView.as_view(),
    #     name="comment_create"
    # ),

    # # /<str:slug>/comments/
    # path(
    #     route='<str:slug>/comments/',
    #     view=ArticleCommentList.as_view(),
    #     name="article_comments"
    # ),




   



    # author/profile/details
    path(
        route='author/profile/details/',
        view=AuthorProfileView.as_view(),
        name='author_profile_details'
    ),

    # author/profile/update/
    path(
        route='author/profile/update/',
        view=AuthorProfileUpdateView.as_view(),
        name='author_profile_update'
    ),

    # author/article/write
    path(
        route='author/article/create/',
        view=ArticleWriteView.as_view(),
        name="article_write"
    ),

    # me/article/<str:slug>/update/
    path(
        route='article/<str:slug>/update/',
        view=ArticleUpdateView.as_view(),
        name="article_update"
    ),

    # /article/<str:slug>/delete/
    path(
        route='article/<str:slug>/delete/',
        view=ArticleDeleteView.as_view(),
        name="article_delete"
    ),

    # /me/<str:slug>/publish/
    path(
        route="article/<str:slug>/publish/",
        view=ArticlePublishView.as_view(),
        name="publish_article"
    ),

    # /me/articles/written/
    path(
        route="articles/written/",
        view=AuthorWrittenArticlesView.as_view(),
        name="written_articles"
    ),

    # /articles/published/
    path(
        route="articles/published/",
        view=AuthorPublishedArticlesView.as_view(),
        name="published_articles"
    ),

    # /articles/drafted/
    path(
        route="articles/drafts/",
        view=AuthorDraftedArticlesView.as_view(),
        name="drafted_articles"
    ),

    # /articles/deleted/
    path(
        route="articles/deleted/",
        view=AuthorDeletedArticlesView.as_view(),
        name="deleted_articles"
    ),



]
