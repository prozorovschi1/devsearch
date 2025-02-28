from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project,Tag
from .forms import ProjectForm, ReviewForm
from django.shortcuts import render
from .utils import searchProjects, paginateProjects
from django.shortcuts import render, get_object_or_404, redirect

 


def projects(request):
    projects, search_query = searchProjects(request)
    custom_range, projects = paginateProjects(request,projects,6)

    context = {'projects': projects, 'search_query': search_query,'custom_range': custom_range}
    return render(request, 'projects/projects.html', context)


def project(request, pk):
    projectObj = get_object_or_404(Project, id=pk)
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            # Verifică dacă utilizatorul a lăsat deja o recenzie
            existing_review = projectObj.review_set.filter(owner=request.user.profile).exists()
            if existing_review:
                messages.error(request, 'You have already submitted a review for this project.')
            else:
                review = form.save(commit=False)
                review.project = projectObj
                review.owner = request.user.profile
                review.save()

                # Actualizează voturile proiectului
                projectObj.getVoteCount

                messages.success(request, 'Your review was successfully submitted!')
                return redirect('project', pk=projectObj.id)

    context = {'project': projectObj, 'form': form}
    return render(request, 'projects/single-project.html', context)


@login_required(login_url="login")
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('account')



    context = {'form': form}
    return render(request, "projects/project_form.html", context)

@login_required(login_url="login")
def updateProject(request, pk):
   profile = request.user.profile
   project = profile.project_set.get(id=pk)
   project = Project.objects.get(id=pk)
   form = ProjectForm(instance=project)

   if request.method == 'POST':
       form = ProjectForm(request.POST, request.FILES, instance=project)
       if form.is_valid():
           form.save()
           return redirect('account')


   context = {'form': form}
   return render(request, "projects/project_form.html", context)


@login_required(login_url="login")
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete ()
        return redirect('projects')
    context = {'object': project}
    return render(request, 'delete_template.html', context)

def home(request):
    return render(request,'home.html')

