import datetime
import json

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import View
from django.http import HttpResponse

from comp.utils import File2Json

from comp.models import CompanyStats, CompanyMonthlyRating, Company
from stats.models import Months

class Dashboard(View):
    def get(self, request):
        return render(request, 'index.html',)


class UploadStats(View):
    def get(self, request):
        return render(
            request, 'uploadstats.html')

    def post(self, request):
        _file = request.FILES["file"]
        file_extn = _file.name.split('.')[-1]
        # writing file physically in /tmp location
        file_path = '/tmp/%s.%s' % (
            datetime.datetime.now().strftime('%Y-%m-%d_%H-%M'), file_extn)
        new_file = open(file_path, 'wb+')
        for chunk in _file.chunks():
            new_file.write(chunk)
        new_file.close()
        data = File2Json(file_path).convert()
        months = data.keys()
        for month in months:
            CompanyStats.create_data(month, data[month])
        return render(
            request, 'uploadstats.html', {
                "message": "Successfully uploaded company stats !"})

class Stats(View):
    def get(self, request):
        stats = CompanyMonthlyRating.objects.all()
        return render(
            request, 'stats.html', {"stats": stats})


class CompanyMatrix(View):
    def get(self, request):
        companies = Company.objects.all()
        if request.is_ajax(): 
            company = request.GET.get("company")
            months = Months.objects.all().order_by("id")
            crs_details = {}
            for month in months:
                crs = CompanyMonthlyRating.crs(month.code, company)
                crs_details[month.code] = crs
            labels = list(months.values_list("code", flat=True))
            data = {
                "labels": list(months.values_list("code", flat=True)),
                "data": crs_details}
            return HttpResponse(json.dumps(data), content_type="application/json")
        return render(
            request, 'barchart.html', {"companies": companies})
