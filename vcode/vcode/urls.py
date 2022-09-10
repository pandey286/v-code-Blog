from django.contrib import admin
from django.urls import path, include

# To Change the Header for Admin Panel
admin.site.site_header="v/Code Admin"

# To Change the Site Title
admin.site.site_title="v/Code Admin Panel"

# To Change the index from  site administrator to your liking
admin.site.index_title="Welcome to v/Code Admin Panel"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('blog/', include('blog.urls'))
]
