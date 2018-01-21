from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect
from django.urls import reverse

from ..models import School
from ..forms import SchoolForm


@permission_required('store.can_maintain_schools')
def manage_school_list(request):
    school_queryset = School.objects.all()
    data = {}

    if request.GET.get('query', False):
        school_queryset = school_queryset.filter(name__icontains=request.GET['query'])
        data['query'] = request.GET.get('query', False)
    
    data['schools'] = school_queryset

    return render(request, 'store/manage/manage_school_list.html', data)


@permission_required('store.can_maintain_schools')
def manage_school_add(request):
    if request.method == 'POST':

        form = SchoolForm(request.POST)
        if form.is_valid():
            school = form.save()
            return HttpResponseRedirect(reverse('manage-school-list'))
    
    else:
        form = SchoolForm()
    
    return render(request, 'store/manage/manage_school_form.html', {
        'title_message': 'Add new school',
        'submit_message': 'Add',
        'form': form
    })


@permission_required('store.can_maintain_schools')
def manage_school_update(request,pk):
    
    school_object = get_object_or_404(School, school_id=pk)

    if request.method == 'POST':

        form = SchoolForm(request.POST, instance=school_object)
        if form.is_valid():
            school = form.save()
            return HttpResponseRedirect(reverse('manage-school-list'))
    
    else:
        form = SchoolForm(instance=school_object)
    
    return render(request, 'store/manage/manage_school_form.html', {
        'title_message': 'Update school',
        'submit_message': 'Update',
        'form': form
    })


@permission_required('store.can_delete_schools')
def manage_school_delete(request,pk):

    school_object = get_object_or_404(School, school_id=pk)
    school_object.delete()

    return HttpResponseRedirect(reverse('manage-school-list'))