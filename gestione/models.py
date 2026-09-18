from django.db import models



class Dipartimento(models.Model):
    codice_dipartimento = models.CharField(max_length=10, primary_key=True)
    nome_dipartimento = models.CharField(max_length=100)

    def __str__(self):
        return self.nome_dipartimento


class Corsodilaurea(models.Model):
    codiceCDL = models.CharField(max_length=10, primary_key=True)
    nomecdl = models.CharField(max_length=100)
    livello = models.IntegerField()  
    codice_dipartimento = models.ForeignKey(
        Dipartimento, on_delete=models.CASCADE
    )

    def __str__(self):
        return self.nomecdl


# 3. Persona
class Persona(models.Model):
    idpersona = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    cognome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    data_nascita = models.DateField()
    codice_fiscale = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return f"{self.nome} {self.cognome}"


# 4. Docente
class Docente(Persona):
    stipendio = models.IntegerField()
    ruolo = models.CharField(max_length=50)
    codice_dipartimento = models.ForeignKey(
        Dipartimento, on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.nome} {self.cognome} - Ruolo: {self.ruolo}"


# 5. Studente
class Studente(Persona):
    matricola = models.CharField(max_length=20, unique=True)
    annoiscrizione = models.IntegerField()
    codiceCDL = models.ForeignKey(Corsodilaurea, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nome} {self.cognome} - Matricola: {self.matricola}"


# 6. Corso 
class Corso(models.Model):
    codicecorso = models.CharField(max_length=10, primary_key=True)
    nomecorso = models.CharField(max_length=100)
    cfu = models.IntegerField()
    annoaccademico = models.CharField(max_length=20)
    iddocente = models.ForeignKey(Docente, on_delete=models.CASCADE)
    codiceCDL = models.ForeignKey(Corsodilaurea, on_delete=models.CASCADE)

    def __str__(self):
        return self.nomecorso


# 7. Verbalizzazione 
class Verbalizzazione(models.Model):
    idverbalizzazione = models.AutoField(primary_key=True)
    voto = models.IntegerField()
    lode = models.BooleanField(default=False)
    data = models.DateField()
    idstudente = models.ForeignKey(Studente, on_delete=models.CASCADE)
    codicecorso = models.ForeignKey(Corso, on_delete=models.CASCADE)

    class Meta:
        # Uno studente non può verbalizzare due volte lo stesso corso
        unique_together = ("idstudente", "codicecorso")

    def __str__(self):
        return f"{self.idstudente.matricola} - {self.codicecorso.nomecorso} : {self.voto}"
    
