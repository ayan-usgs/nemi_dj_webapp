
''' This module contains the url conf for the nemi search pages.
'''

from django.conf.urls.defaults import patterns, url
import views;

urlpatterns = patterns("", 
        url(r'^general/$',
            views.GeneralSearchView.as_view(),
            name='search-general'),
        url(r'^general_tsv/$',
            views.ExportGeneralSearchView.as_view(),
            {'export' : 'tsv'},
            name='search-general_export_tsv'),
        url(r'^general_xls/$',
            views.ExportGeneralSearchView.as_view(),
            {'export' : 'xls'},
            name='search-general_export_xls'),
        url(r'^method_summary/(?P<method_id>\d+)/$',
            views.MethodSummaryView.as_view(),
            name='search-method_summary'),
        url(r'^method_analyte_export/(?P<method_id>\w+)/$',
            views.ExportMethodAnalyte.as_view(),
            name='search-method_analyte_export'),
        url(r'^analyte/$', 
            views.AnalyteSearchView.as_view(),
            name='search-analyte'),
        url(r'^analyte_tsv/$',
            views.ExportAnalyteSearchView.as_view(),
            {'export' : 'tsv'},
            name='search-analyte_export_tsv'),
        url(r'^analyte_xls/$',
            views.ExportAnalyteSearchView.as_view(),
            {'export' : 'xls'},
            name='search-analyte_export_xls'),
        url(r'^analyte_select/$',
            views.AnalyteSelectView.as_view(),
            name='search-analyte_select'),
        url(r'^keyword/$',
            views.KeywordSearchView.as_view(),
            name='search-keyword'),
        url(r'^microbiological/$',
            views.MicrobiologicalSearchView.as_view(),
            name='search-microbiological'),
        url(r'^biological/$',
            views.BiologicalSearchView.as_view(),
            name='search-biological'),
        url(r'^biological_method_summary/(?P<method_id>\d+)/$',
            views.BiologicalMethodSummaryView.as_view(),
            name='search-biological_method_summary'),
        )