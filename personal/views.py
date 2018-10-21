from django.shortcuts import render
from django.template import Context
from personal.forms import ReserveForm
from personal.forms import CancelForm
from personal.forms import DateForm
from personal.models import Reserve
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views.generic import View
from personal.utils import render_to_pdf
from django.template.loader import get_template

def index(request):
    return render(request, 'personal/FL.html')

def reserve(request):
    if request.POST:
        form = ReserveForm(request.POST)
        if form.is_valid():
            request.session['roll'] = form.cleaned_data['Rollno']
            form.save()
        create = request.session.get('roll')
        if create :
            Reserve.objects.filter(Rollno=create).update(Instrument=request.session.get("instrument"))
            Reserve.objects.filter(Rollno=create).update(Date=request.session.get("date"))
            Reserve.objects.filter(Rollno=create).update(Time=request.session.get("time"))
        return HttpResponseRedirect('I1.html')
    return render(request, 'personal/R.html')

def cancel(request):
    if request.POST:
        if Reserve.objects.filter(Rollno = request.POST.get("Rollno") , Pin = request.POST.get("Pin")) :
            Reserve.objects.filter(Rollno = request.POST.get("Rollno") , Pin = request.POST.get("Pin")).delete()
            return HttpResponseRedirect('C2.html')
        else:
            return render(request, 'personal/C1.html')
    return render(request, 'personal/C.html')

def items(request):
    if request.POST:
        request.session["instrument"] = request.POST.get("Instrument")
        return HttpResponseRedirect('D.html')
    return render(request, 'personal/I.html')

def dates(request):
    if request.POST:
        request.session['date'] = request.POST.get("Date")
        return HttpResponseRedirect('S.html')
    return render(request, 'personal/D.html')

def slot(request):
    i = request.session.get("instrument")
    d = request.session.get("date")
    count = 0
    s = ['8:30 - 9:30','9:30 - 10:30','10:30 - 11:30','11:30 - 12:30','12:30 - 1:30','1:30 - 2:30','2:30 - 3:30','3:30 - 4:30']
    a = ['success','success','success','success','success','success','success','success','submit','submit','submit','submit','submit','submit','submit','submit']

    for tt in s :
        print(count)
        if Reserve.objects.filter(Date = d, Instrument = i, Time = s[count]) :
            a[count] = 'danger'
            a[count+8] = 'button'
        count = count + 1

    if request.POST:
        request.session['time'] = request.POST.get("Time")
        return HttpResponseRedirect('R.html')
    return render(request,'personal/S.html',{'name':a})

def about(request):
    return render(request, 'personal/A.html')

def itemsuccess(request):
    return render(request, 'personal/I1.html')

def cancelsuccess(request):
    return render(request, 'personal/C2.html')

class GeneratePDF(View):
     def get(self, request, *args, **kwargs):
         template = get_template('personal/T.html')
         Roll = request.session.get('roll')
         obj  = Reserve.objects.get(Rollno = Roll)
         context = {
             "Rollno": obj.Rollno,
             "First": obj.First,
             "Last": obj.Last,
             "Email": obj.Email,
             "Phone": obj.Phone,
             "Date": obj.Date,
             "Time":obj.Time,
             "Pin": obj.Pin,
             "Instrument": obj.Instrument,
         }
         html = template.render(context)
         pdf = render_to_pdf('personal/T.html', context)
         if pdf:
             response = HttpResponse(pdf, content_type='personal/pdf')
             filename = "Slot_Booking.pdf"
             content = "inline; filename='%s'" %(filename)
             download = request.GET.get("download")
             if download:
                 content = "attachment; filename='%s'" %(filename)
             response['Content-Disposition'] = content
             return response
         return HttpResponse("Not found")
