from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


class Segreteria(models.Model):
    id_segreteria = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    cognome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    class Meta:
        db_table = 'segreteria'

    def __str__(self):
        return f"{self.cognome} {self.nome}"


class Dipartimento(models.Model):
    id_dipartimento = models.AutoField(primary_key=True)
    citta = models.CharField(max_length=50)
    indirizzo = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    id_segreteria = models.ForeignKey(
        Segreteria, 
        on_delete=models.CASCADE, 
        db_column='id_segreteria'
    )

    class Meta:
        db_table = 'dipartimento'

    def __str__(self):
        return f"Dipartimento di {self.citta} - {self.indirizzo}"


class Utente(AbstractUser):
    RUOLI = [
        ('Studente', 'Studente'),
        ('Docente', 'Docente'),
    ]

    id_utente = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    cognome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    ruolo = models.CharField(max_length=20, choices=RUOLI, default='Studente')
    matricola = models.CharField(max_length=20, null=True, blank=True)
    ruolo_accademico = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'utente'

    def __str__(self):
        return f"{self.cognome} {self.nome} ({self.ruolo})"


class Corso(models.Model):
    id_corso = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    cfu = models.IntegerField()
    descrizione = models.TextField()
    anno_erogazione = models.IntegerField()

    class Meta:
        db_table = 'corso'

    def __str__(self):
        return f"{self.nome} ({self.cfu} CFU)"


class AppelloEsame(models.Model):
    id_appello = models.AutoField(primary_key=True)
    titolo = models.CharField(max_length=100)
    data_appello = models.DateField()
    descrizione = models.CharField(max_length=255)
    luogo = models.CharField(max_length=255)
    posti_disponibili = models.IntegerField()

    class Meta:
        db_table = 'appello_esame'

    def __str__(self):
        return f"{self.titolo} - {self.data_appello}"


class StrutturaAula(models.Model):
    id_aula = models.AutoField(primary_key=True)
    capienza = models.IntegerField()
    id_corso = models.ForeignKey(
        Corso, 
        on_delete=models.CASCADE, 
        db_column='id_corso'
    )
    id_dipartimento = models.ForeignKey(
        Dipartimento, 
        on_delete=models.CASCADE, 
        db_column='id_dipartimento'
    )

    class Meta:
        db_table = 'struttura_aula'

    def __str__(self):
        return f"Aula {self.id_aula} (Capienza: {self.capienza})"


class ValutazioneCorso(models.Model):
    id_valutazione = models.AutoField(primary_key=True)
    testo = models.TextField()
    punteggio = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    id_utente = models.ForeignKey(
        Utente, 
        on_delete=models.CASCADE, 
        db_column='id_utente'
    )
    id_corso = models.ForeignKey(
        Corso, 
        on_delete=models.CASCADE, 
        db_column='id_corso'
    )

    class Meta:
        db_table = 'valutazione_corso'

    def __str__(self):
        return f"Valutazione {self.id_corso.nome}: {self.punteggio}/5"


class Carriera(models.Model):
    STATI = [
        ('Attivo', 'Attivo'),
        ('Sospeso', 'Sospeso'),
        ('Laureato', 'Laureato'),
    ]
    TIPI_LAUREA = [
        ('Triennale', 'Triennale'),
        ('Magistrale', 'Magistrale'),
        ('Ciclo Unico', 'Ciclo Unico'),
    ]

    id_carriera = models.AutoField(primary_key=True)
    data_immatricolazione = models.DateField()
    stato = models.CharField(max_length=20, choices=STATI, default='Attivo')
    tipo_laurea = models.CharField(max_length=20, choices=TIPI_LAUREA)
    id_utente = models.ForeignKey(
        Utente, 
        on_delete=models.CASCADE, 
        db_column='id_utente'
    )
    id_dipartimento = models.ForeignKey(
        Dipartimento, 
        on_delete=models.CASCADE, 
        db_column='id_dipartimento'
    )

    class Meta:
        db_table = 'carriera'

    def __str__(self):
        return f"Carriera {self.id_carriera} - {self.id_utente.cognome}"


class Iscrizione(models.Model):
    STATI = [
        ('confermato', 'Confermato'),
        ('annullato', 'Annullato'),
        ('attesa', 'In Attesa'),
    ]

    id_iscrizione = models.AutoField(primary_key=True)
    stato = models.CharField(max_length=20, choices=STATI, default='attesa')
    id_utente = models.ForeignKey(
        Utente, 
        on_delete=models.CASCADE, 
        db_column='id_utente'
    )
    id_appello = models.ForeignKey(
        AppelloEsame, 
        on_delete=models.CASCADE, 
        db_column='id_appello'
    )

    class Meta:
        db_table = 'iscrizione'

    def __str__(self):
        return f"Iscrizione {self.id_utente.cognome} -> {self.id_appello.titolo}"


class DettaglioCarriera(models.Model):
    id_dettaglio = models.AutoField(primary_key=True)
    id_carriera = models.ForeignKey(
        Carriera, 
        on_delete=models.CASCADE, 
        db_column='id_carriera'
    )
    id_corso = models.ForeignKey(
        Corso, 
        on_delete=models.CASCADE, 
        db_column='id_corso'
    )
    voto = models.IntegerField(
        validators=[MinValueValidator(18), MaxValueValidator(30)]
    )
    lode = models.BooleanField(default=False)

    class Meta:
        db_table = 'dettaglio_carriera'

    def __str__(self):
        return f"{self.id_corso.nome}: {self.voto}"