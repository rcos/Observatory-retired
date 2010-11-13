from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from dashboard.models import Blog, Project, Repository
from dashboard.forms import ProjectForm

# list the rankings
def index(request):
  return render_to_response('index.html', {
    'projects': Project.objects.all()
  })

def show_project(request, project_id):
  return render_to_response('show-project.html', {
    'project': get_object_or_404(Project, id = int(project_id))
  })

def add_project(request):
  return render_to_response('add-project.html', {
    'form': ProjectForm()
  }, context_instance = RequestContext(request))

def modify_project(request, project_id):
  project = get_object_or_404(Project, id = int(project_id))
  
  return render_to_response('modify-project.html', {
    'project': project,
    'form': ProjectForm(project)
  }, context_instance = RequestContext(request))

def create_project(request):
  # create the blog object
  blog = Blog(url = request.POST['blog'])
  blog.save()
  
  # create the repo object
  repo = Repository(url = request.POST['repo'])
  repo.save()
  
  # create the project object
  project = Project(title = request.POST['title'],
                    website = request.POST['website'],
                    wiki = request.POST['wiki'],
                    active = request.POST['active'],
                    description = request.POST['description'],
                    repository_id = repo.id,
                    blog_id = blog.id)
  project.save()
  
  # redirect to the show page for the new project
  return HttpResponseRedirect(reverse('dashboard.views.show_project',
                                      args = (project.id,)))

def update_project(request, project_id):
  project = get_object_or_404(Project, id = int(project_id))
  
  # update the project
  project.title = request.POST['title']
  project.website = request.POST['website']
  project.blog.url = request.POST['blog']
  project.repository.url = request.POST['repository']
  project.wiki = request.POST['wiki']
  project.active = request.POST['active']
  
  # save the project
  project.save()
  project.blog.save()
  project.repository.save()