"""my_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.urls import path
from myapp.views import (
    create_view,
    start_automation,
    searchTxtAndDownload,
    searchFaaAndDownload,
    faaDownload,
    line_chart_json,
    directFaaDownload,
    getPlotimage,
    getPlotly2D,
    draw_plot,
secondgraph,
getPlotly2D_2,
next_prev,
draw_plot_graph_1,
faafile_downloader,
thirdgraph,
draw_plot_graph_3
)

from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', create_view),
    path('start_automation/', start_automation, name='start_automation'),
    path('searchTxtAndDownload/', searchTxtAndDownload, name='search_txt'),
    path('searchFaaAndDownload/', searchFaaAndDownload, name='search_faa'),
    path('faaDownload/<int:id>/', faaDownload, name='download_faa'),
    path('directFaaDownload/', directFaaDownload, name='direct_faa_download'),
    path('line_chart_json', line_chart_json, name='line_chart_json'),
    path('getPlotimage', getPlotimage, name='get_plot_image'),
    path('getplotly2d',  getPlotly2D, name='get_plotly2d'),
    path('draw_plot2d', draw_plot, name='draw_plot2d'),
    path('getplotly2d2',  getPlotly2D_2, name='get_plotly2d2'),
    path('secgraph$', secondgraph, name='secondgraph'),
    path('nextprev$', next_prev, name='nextprev'),
    path('third', thirdgraph, name='third'),
    path('draw_plot2d_2', draw_plot_graph_3, name='draw_plot2d_2'),
    path('draw_plot2d_1', draw_plot_graph_1, name='draw_plot2d_1'),
    path('faafile_downloader_fc', faafile_downloader, name='faafile_downloader_fc'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

