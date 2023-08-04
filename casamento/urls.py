from django.urls import path, include
from rest_framework.routers import SimpleRouter

from casamento.views import GalleryViewSet, PhotoViewSet, CommentViewSet, LikeViewSet, UserUploadViewSet, UnapprovedPhotoViewSet


router = SimpleRouter()

router.register('galleries', GalleryViewSet, basename='galleries')
router.register('photos', PhotoViewSet, basename='photos')
router.register(r'unapproved-photos', UnapprovedPhotoViewSet, basename='unapproved-photos')
router.register('comments', CommentViewSet, basename='comments')
router.register('likes', LikeViewSet, basename='likes')
router.register('upload', UserUploadViewSet, basename='upload')

urlpatterns = [
    path('', include(router.urls)),
]
