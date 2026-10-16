from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .models import Utente, Studente, Docente


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        return render(request, 'login.html', {'error_message': 'Credenziali non valide.'})
    return render(request, 'login.html')


def register_view(request):
    if request.method == 'POST':
        ruolo = request.POST.get('ruolo')
        email = request.POST.get('email')
        password = request.POST.get('password')
        nome = request.POST.get('nome') or ''
        cognome = request.POST.get('cognome') or ''
        username = email.split('@', 1)[0] if email else f"utente_{Utente.objects.count() + 1}"

        user = Utente.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=nome,
            last_name=cognome,
            ruolo=ruolo,
        )

        if ruolo == 'Studente':
            user.matricola = request.POST.get('matricola') or ''
            user.ruolo_accademico = None
            user.save()
            Studente.objects.create(
                utente=user,
                matricola=user.matricola,
                anno_iscrizione=2024,
            )
        elif ruolo == 'Docente':
            user.matricola = request.POST.get('matricola') or ''
            user.ruolo_accademico = request.POST.get('ruolo_accademico') or ''
            user.save()
            Docente.objects.create(
                utente=user,
                codice_docente=user.matricola,
                ambito_ricerca=user.ruolo_accademico,
            )

        login(request, user)
        return redirect('/')

    return render(request, 'register.html')
