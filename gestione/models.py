from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

class Segreteria(models.Model):
    id_segreteria = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    cognome = models.CharField(max_length=100)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=128)

    class Meta:
        db_table = 'uni_segreteria'
        verbose_name = 'Membro Segreteria'
        verbose_name_plural = 'Membri Segreteria'

    def __str__(self):
        return f"{self.cognome} {self.nome} (Segreteria)"


class Dipartimento(models.Model):
    POLI_CITTA = [
        ('Roma', 'Roma'),
        ('Milano', 'Milano'),
        ('Napoli', 'Napoli'),
    ]

    id_dipartimento = models.AutoField(primary_key=True)
    citta = models.CharField(max_length=20, choices=POLI_CITTA)
    indirizzo = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    segreteria = models.ForeignKey(
        Segreteria, 
        on_delete=models.CASCADE, 
        related_name='dipartimenti',
        db_column='id_segreteria'
    )

    class Meta:
        db_table = 'uni_dipartimento'
        verbose_name = 'Dipartimento'
        verbose_name_plural = 'Dipartimenti'

    def __str__(self):
        return f"Dipartimento {self.citta} - {self.indirizzo}"


class Utente(AbstractUser):
    RUOLI_CHOICES = [
        ('Studente', 'Studente'),
        ('Docente', 'Docente'),
    ]

    id_utente = models.AutoField(primary_key=True)
    ruolo = models.CharField(max_length=20, choices=RUOLI_CHOICES, default='Studente')
    matricola = models.CharField(max_length=20, null=True, blank=True)
    ruolo_accademico = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'uni_utente'
        verbose_name = 'Utente'
        verbose_name_plural = 'Utenti'

    def clean(self):
        super().clean()
        if self.ruolo == 'Studente' and not self.matricola:
            raise ValidationError({'matricola': 'La matricola è obbligatoria per il ruolo Studente.'})
        if self.ruolo == 'Docente' and not self.ruolo_accademico:
            raise ValidationError({'ruolo_accademico': 'Il ruolo accademico è obbligatorio per i Docenti.'})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.ruolo})".strip() or self.username


class Studente(models.Model):
    utente = models.OneToOneField(Utente, on_delete=models.CASCADE, related_name='studente', primary_key=True)
    matricola = models.CharField(max_length=20, unique=True)
    anno_iscrizione = models.PositiveIntegerField()

    class Meta:
        db_table = 'uni_studente'
        verbose_name = 'Studente'
        verbose_name_plural = 'Studenti'

    def __str__(self):
        return f"{self.utente.get_full_name()} ({self.matricola})"


class Docente(models.Model):
    utente = models.OneToOneField(Utente, on_delete=models.CASCADE, related_name='docente', primary_key=True)
    codice_docente = models.CharField(max_length=50, unique=True)
    ambito_ricerca = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'uni_docente'
        verbose_name = 'Docente'
        verbose_name_plural = 'Docenti'

    def __str__(self):
        return f"{self.utente.get_full_name()} ({self.codice_docente})"


class Corso(models.Model):
    id_corso = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    descrizione = models.TextField()
    cfu = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    anno_erogazione = models.PositiveIntegerField()

    class Meta:
        db_table = 'uni_corso'
        verbose_name = 'Corso di Insegnamento'
        verbose_name_plural = 'Corsi di Insegnamento'

    def __str__(self):
        return f"{self.nome} ({self.cfu} CFU)"


class Carriera(models.Model):
    STATI_CARRIERA = [
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
    stato = models.CharField(max_length=20, choices=STATI_CARRIERA, default='Attivo')
    tipo_laurea = models.CharField(max_length=20, choices=TIPI_LAUREA)
    dipartimento = models.ForeignKey(
        Dipartimento, 
        on_delete=models.CASCADE, 
        related_name='carriere',
        db_column='id_dipartimento'
    )
    utente = models.ForeignKey(
        Utente, 
        on_delete=models.CASCADE, 
        related_name='carriere',
        db_column='id_utente'
    )

    class Meta:
        db_table = 'uni_carriera'
        verbose_name = 'Carriera'
        verbose_name_plural = 'Carriere'

    def __str__(self):
        return f"Carriera #{self.id_carriera} - {self.utente.cognome} ({self.stato})"


class AppelloEsame(models.Model):
    id_appello = models.AutoField(primary_key=True)
    titolo = models.CharField(max_length=100)
    data_appello = models.DateField()
    descrizione = models.TextField()
    luogo = models.CharField(max_length=255)
    posti_disponibili = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        db_table = 'uni_appello_esame'
        verbose_name = 'Appello Esame'
        verbose_name_plural = 'Appelli Esame'

    def __str__(self):
        return f"{self.titolo} - {self.data_appello}"


class DettaglioCarriera(models.Model):
    id_dettaglio = models.BigAutoField(primary_key=True)
    voto = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(18), MaxValueValidator(30)]
    )
    lode = models.BooleanField(default=False)
    carriera = models.ForeignKey(
        Carriera, 
        on_delete=models.CASCADE, 
        related_name='esami_sostenuti',
        db_column='id_carriera'
    )
    corso = models.ForeignKey(
        Corso, 
        on_delete=models.CASCADE, 
        related_name='verbalizzazioni',
        db_column='id_corso'
    )

    class Meta:
        db_table = 'uni_dettaglio_carriera'
        verbose_name = 'Dettaglio Carriera'
        verbose_name_plural = 'Dettagli Carriera'
        unique_together = ('carriera', 'corso')

    def clean(self):
        if self.lode and self.voto != 30:
            raise ValidationError({'lode': 'La lode può essere assegnata solo con votazione pari a 30.'})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class Iscrizione(models.Model):
    STATI_ISCRIZIONE = [
        ('confermato', 'Confermato'),
        ('annullato', 'Annullato'),
        ('attesa', 'In Attesa'),
    ]

    id_iscrizione = models.AutoField(primary_key=True)
    stato = models.CharField(max_length=20, choices=STATI_ISCRIZIONE, default='attesa')
    utente = models.ForeignKey(
        Utente, 
        on_delete=models.CASCADE, 
        related_name='iscrizioni_esami',
        db_column='id_utente'
    )
    appello = models.ForeignKey(
        AppelloEsame, 
        on_delete=models.CASCADE, 
        related_name='iscritti',
        db_column='id_appello'
    )

    class Meta:
        db_table = 'uni_iscrizione'
        verbose_name = 'Iscrizione Appello'
        verbose_name_plural = 'Iscrizioni Appelli'
        unique_together = ('utente', 'appello')


class StrutturaAula(models.Model):
    id_aula = models.AutoField(primary_key=True)
    capienza = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    dipartimento = models.ForeignKey(
        Dipartimento, 
        on_delete=models.CASCADE, 
        related_name='aule',
        db_column='id_dipartimento'
    )
    corso = models.ForeignKey(
        Corso, 
        on_delete=models.CASCADE, 
        related_name='aule_assegnate',
        db_column='id_corso'
    )

    class Meta:
        db_table = 'uni_struttura_aula'
        verbose_name = 'Struttura Aula'
        verbose_name_plural = 'Strutture Aule'


class ValutazioneCorso(models.Model):
    id_valutazione = models.AutoField(primary_key=True)
    testo = models.TextField()
    valutazione = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    utente = models.ForeignKey(
        Utente, 
        on_delete=models.CASCADE, 
        related_name='recensioni_corsi',
        db_column='id_utente'
    )
    corso = models.ForeignKey(
        Corso, 
        on_delete=models.CASCADE, 
        related_name='valutazioni',
        db_column='id_corso'
    )

    class Meta:
        db_table = 'uni_valutazione_corso'
        verbose_name = 'Valutazione Corso'
        verbose_name_plural = 'Valutazioni Corsi'