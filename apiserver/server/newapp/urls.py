from django.urls import path, include

from rest_framework.authtoken.views import obtain_auth_token

from .views import UserViewSet, RegisterUserViewSet, UserProfileViewSet, DuelViewSet, ItemViewSet, ResultViewSet, PopularDuelsViewSet, ProgressViewSet, MessageViewSet

urlpatterns = [
    path("user", UserViewSet.as_view({
        "get":"list",
        "put":"edit",
        "delete":"destroy",
        #"post":"create",
        })),
        path("registar", RegisterUserViewSet.as_view({
            "post":"create",
        })),
        path("profile", UserProfileViewSet.as_view({
            "get":"list",
        })),
    path("duel", DuelViewSet.as_view({
        "get":"list",
        "post":"create",
        "put":"edit",
        "delete":"destroy",
    })),
    path("item", ItemViewSet.as_view({
        "get":"list",
        "post":"create",
        "put":"edit",
        "delete":"destroy",
    })),
    path("progress", ProgressViewSet.as_view({
        "get":"list",
        "post":"create",
        "put":"edit",
        "delete":"destroy",
    })),
    path("result", ResultViewSet.as_view({
        "get":"list",
        "post":"create",
    })),
    path("popular", PopularDuelsViewSet.as_view({
        "get":"list",
    })),
    path("message", MessageViewSet.as_view({
        "get":"list",
    })),
    path("auth", obtain_auth_token, name='api_token_auth'),
    #path("gauth", GoogleAuthViewSet.as_view({"post":"get_id_token"}), name='google_auth'),
]