from multiprocessing.context import assert_spawning
from django.contrib import admin
from PrimeraApp.models import Experiencias, Profile, Cursos, Profile_Experiencias, Formulario



admin.site.register(Experiencias)
admin.site.register(Profile)
admin.site.register(Profile_Experiencias)
admin.site.register(Formulario)

class AdminCursos(admin.ModelAdmin):
    readonly_fields = ("id", )

admin.site.register(Cursos, AdminCursos)

