from django.urls import include, path

from utilities.urls import get_model_urls

from . import models, views  # noqa: F401 — views must be imported to trigger @register_model_view

urlpatterns = [
    # SSHKey
    path('ssh-keys/', include(get_model_urls('netbox_ssh_keys', 'sshkey', detail=False))),
    path('ssh-keys/<int:pk>/', include(get_model_urls('netbox_ssh_keys', 'sshkey'))),
]
