from django.shortcuts import render, HttpResponse, redirect
from PrimeraApp import models
from .forms import Form_Experiencia, CreateUserForm, SearchForm, SettingsForm, CursosForm, FormularioForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated, allowed_users, authenticated
from django.contrib.auth.models import Group, User
from django.contrib.auth import get_user_model
from django.http import Http404

#@login_required(login_url="login")
#@allowed_users(allowed_roles=["Admin", "Customers"])
def home(request):
    
    experiencias = models.Profile_Experiencias.objects.all()

    print(experiencias, "salida de experiencias")

    lista_exp = []
    for i in experiencias:
        if i.experiencia.evaluacion == "bueno":#sólo las exps buenas son visibles
            lista_exp.append(i)
    return render(request, "PrimeraApp/home.html", {"experiencias":lista_exp})

@unauthenticated
def registerPage(request):  

    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()

            username = form.cleaned_data.get("username")

            group = Group.objects.get(name = "Customers") 
            user.groups.add(group)

            messages.success(request, "el usuario " + username + " fue creado " +
            " y agregado al grupo: " +
            group.name)
            
           
            return redirect("login")        

    return render(request, "PrimeraApp/register.html", {"form":form})


     
@unauthenticated
def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect("home")

        else:
            messages.info(request, "password o username incorrecto")

    return render(request, "PrimeraApp/login.html", {})


def logout_page(request):
    logout(request)
    return redirect("login")

@authenticated
def contanos_experiencia(request):
    
    if request.method == "POST":
        formulario = Form_Experiencia(request.POST)   
        if formulario.is_valid():
            profile = str(request.user)
            busco_profile = models.Profile.objects.filter(usuario = profile)
            for x in busco_profile:
                busco_profile = x
        if not busco_profile:#el profile no existe  
            usuario = models.Profile.objects.create(usuario = str(request.user))
            usuario.save()

            experiencia = models.Experiencias.objects.create(mensaje = request.POST["mensaje"], evaluacion = request.POST["evaluacion"]) 
            experiencia.save()

            objeto = models.Profile_Experiencias.objects.create(usuario = usuario, experiencia = experiencia)
            objeto.save()
            messages.success(request, "experiencia cargada con éxito")
            return redirect("home") #este es el caso en el que no hay perfil creado


        else:#si busco_profile halla ese perfil:
        #debo revisar si existe en la clase relacional, esto ocurre, si tiene experiencia cargada
        #busco_profile en clase relacional.

            busco_profile_id = busco_profile.id #id del usuario que está logueado. Lo paso como parametro para filtrar en clase relacional
        
            busqueda_clase_relacional = models.Profile_Experiencias.objects.filter(usuario_id = busco_profile_id) #para verificar si hay ya un usuario con experiencia
            #cargada, lo filtro por id del usuario. Luego itero esa salida, ya que filter devuelve objeto query.
            for x in busqueda_clase_relacional:
                busqueda = x
            if busqueda_clase_relacional:
                messages.success(request, "ya hay experiencia cargada aunque puedes borrar la anterior y agregar otra")
                return redirect("experiences")
            else:
                experiencia = models.Experiencias.objects.create(mensaje = request.POST["mensaje"], evaluacion = request.POST["evaluacion"]) 
                experiencia.save()

                objeto = models.Profile_Experiencias.objects.create(usuario = busco_profile, experiencia = experiencia)
                objeto.save()
                messages.success(request, "nueva experiencia cargada")
                return redirect("home")
    else:
        formulario = Form_Experiencia()

    return render(request, "PrimeraApp/formulario.html", {"formulario":formulario})

@login_required(login_url="login")
#@allowed_users(allowed_roles=["Admin"])
def profile(request, name = None):    #agregar más con django form
    usuarios = models.User.objects.all()
    form = SearchForm()
    name = request.GET.get("name")

    if name:
        usuarios = models.User.objects.filter(username = name)
    contexto = {"usuarios":usuarios, "form":form}


    return render(request,"PrimeraApp/profile.html", contexto)

def settings(request):
    form = SettingsForm(request.POST)
    if request.method == "POST":
        form = request.POST["seccion"]
        if form == "Experiencias":
            return redirect("experiences")
        elif form == "Users":
            return redirect("profile")
        elif form == "Cursos":
            return redirect("cursos")

    contexto = {"form":form}
    return render(request,"PrimeraApp/settings.html", contexto)


def config_experiences(request):
    experiencia = models.Experiencias.objects.all()
    if request.POST:
        experiencia = models.Experiencias.objects.filter(id=request.POST["id"])
        experiencia.delete()
        return redirect('home')
    return render(request,"PrimeraApp/experiences_config.html", {"experiences":experiencia})


def update(request, pk):
    usuario = models.User.objects.get(id=pk)
    form = CreateUserForm(instance=usuario)

    if request.method == "POST":
        form = CreateUserForm(request.POST, instance=usuario)
        if form.is_valid():
            user = form.save()
            return redirect('profile')
    return render(request,"PrimeraApp/profile.html", {"form":form})

def delete(request, pk): 
    usuario = models.User.objects.get(id=pk)
    nombre_usuario = usuario.username
    profile = models.Profile.objects.filter(usuario = nombre_usuario)
    for i in profile:
        perfil = i
    contexto = {"form":usuario}
    if request.POST:
        usuario.delete()
        perfil.delete()
        return redirect("profile")
    return render(request, "PrimeraApp/delete.html", contexto)

def delete_curso(request, cursos_id=None):

        curso = models.Cursos.objects.get(id=cursos_id)
        curso.delete()
        return redirect("cursos")

def update_curso(request, cursos_id):
    curso = models.Cursos.objects.get(id=cursos_id)
    form = CursosForm(instance=curso)

    if request.POST:
        
        curso = CursosForm(request.POST, request.FILES, instance=curso)
        if curso.is_valid():
            curso.save()
        return redirect("cursos")

    else:
        return render(request, "PrimeraApp/update_curso.html", {"form":form})


def cursos_settings(request):

    cursos = models.Cursos.objects.all()
    form = CursosForm()
    if request.method == "POST":
        form = CursosForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            
            form = models.Cursos.objects.filter(título = request.POST["título"])
            for object in form:
                object.autor = str(request.user)
                object.save()

            return redirect("cursos")

    return render(request,"PrimeraApp/cursos_config.html", {"cursos":cursos, "form":form})

def mostrar_cursos(request):

    objetos= models.Cursos.objects.all()

    return render(request, "PrimeraApp/cursos.html", {"objetos":objetos})

@unauthenticated
def formulario_inscripcion(request, cursos_id=None):
    if cursos_id:
        curso = models.Cursos.objects.get(id = cursos_id) 
        form = FormularioForm(initial={"curso":curso})
    else:
        form = FormularioForm()
        
    if request.POST:
        form = FormularioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "la información ha sido enviada. Te contactaremos en breve")
            return redirect("home")
    contexto = {"form":form}
    return render(request, "PrimeraApp/formulario_inscripcion.html", contexto)


def test_ingles(request):
    if request.method == "POST":

        aciertos = 0
        if (request.POST["pregunta1"]) == "am":
            aciertos +=1

        if (request.POST["pregunta2"]) == "am": 
            aciertos +=1

        if (request.POST["pregunta3"]) == "is":
            aciertos +=1

        if (request.POST["pregunta4"]) == "are":
            aciertos +=1
        
        if aciertos < 2 :
            aciertos = "curso básico"
        elif aciertos == 2:
            aciertos = "curso intermedio"
        else:
            aciertos = "curso avanzado"

        messages.success(request, aciertos)
        return redirect("mostrar_curso")    

    return render(request, "PrimeraApp/test_ingles.html")
     
    

