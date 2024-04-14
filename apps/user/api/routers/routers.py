from rest_framework.routers import DefaultRouter

from apps.user.api.views.views_users import UserViewSet
from apps.user.api.views.views_manage_accounts import ManageAccount
from ..views.views_login import Login

router = DefaultRouter()
router.register('', UserViewSet, basename="user")
router.register('', ManageAccount, basename="ManageAccount")
# router.register('',userRetrieveViewSet, basename= "change")
urlpatterns = router.urls
