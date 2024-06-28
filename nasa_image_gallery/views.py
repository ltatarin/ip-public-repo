# capa de vista/presentación
# si se necesita algún dato (lista, valor, etc), esta capa SIEMPRE se comunica con services_nasa_image_gallery.py

from django.shortcuts import redirect, render
from .layers.services import services_nasa_image_gallery
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

# función que invoca al template del índice de la aplicación.
def index_page(request):
    return render(request, 'index.html', {'current_page': 'index'})

# auxiliar: retorna 2 listados -> uno de las imágenes de la API y otro de los favoritos del usuario.
def getAllImagesAndFavouriteList(request, page, limit, input=None):
    images = services_nasa_image_gallery.getPaginatedImages(page, limit, input)
    favourite_list = services_nasa_image_gallery.getAllFavouritesByUser(request)

    return images, favourite_list

# función principal de la galería.
def home(request):
    # llama a la función auxiliar getAllImagesAndFavouriteList() y obtiene 2 listados: uno de las imágenes de la API y otro de favoritos por usuario*.
    # (*) este último, solo si se desarrolló el opcional de favoritos; caso contrario, será un listado vacío [].
    page = request.GET.get('page', '')
    limit = request.GET.get('limit', '')

    if (page and limit):
        images, favourite_list = getAllImagesAndFavouriteList(request, page, limit)
        return render(request, 'page.html', {'images': images, 'favourite_list': favourite_list})
    else:  
        return render(request, 'home.html', {'current_page': 'home'} )

# función utilizada en el buscador.
def search(request):
    # si el usuario no ingresó texto alguno, debe refrescar la página; caso contrario, debe filtrar aquellas imágenes que posean el texto de búsqueda.
    page = request.GET.get('page', '')
    limit = request.GET.get('limit', '')
    search_msg = request.POST.get('query', '')

    if search_msg != '':
        if (page and limit):
            images, favourite_list = getAllImagesAndFavouriteList(request, page, limit, search_msg)
            return render(request, 'page.html', {'images': images, 'favourite_list': favourite_list} )
        else:  
            return render(request, 'home.html', {'current_page': 'home', 'search_msg': search_msg} )
    else:
        return redirect('home')

def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')

    return render(request, 'registration/login.html', {'current_page': 'login'})

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Usuario en uso')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email en uso')
        else:
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.save()
            login(request, user)
            return redirect('home')
            
    return render(request, 'registration/register.html', {'current_page': 'register'})
    
# las siguientes funciones se utilizan para implementar la sección de favoritos: traer los favoritos de un usuario, guardarlos, eliminarlos y desloguearse de la app.
@login_required
def getAllFavouritesByUser(request):
    favourite_list = services_nasa_image_gallery.getAllFavouritesByUser(request)
    return render(request, 'favourites.html', {'favourite_list': favourite_list, 'current_page': 'favourites'})


@login_required
def saveFavourite(request):
    services_nasa_image_gallery.saveFavourite(request)
    return redirect('home')

@login_required
def deleteFavourite(request):
    services_nasa_image_gallery.deleteFavourite(request)
    return redirect('favoritos')

@login_required
def exit(request):
    logout(request)
    return redirect('home')