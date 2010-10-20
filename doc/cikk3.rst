A modell
--------

Egy MVC jellegű alkalmazás legfontosabb része a modell, a legelső dolog, amit meg kell terveznünk, el kell készítenünk. (Bár én a végére hagytam, vegyük észre, hogy eddig is volt modell a példában, mégpedig az ``utils.py`` modulon keresztül elért filerendszer.)

A modellünket természetesen nem írja meg helyettünk a django, de rendelkezik egy elég jó `ORM`_-mel, segít a validációban, és ugye van egy automatikusan generált admin felülete, ahol végül is a modellünket piszkálhatjuk.

.. _`ORM`: http://en.wikipedia.org/wiki/Object-relational_mapping


A modellünket - nem meglepő módon - az appunk ``models.py`` moduljában kell definiálnunk. Semmi trükköset nem kell elképzelni, hagyományos python osztályokat kell létrehoznunk, annyi megkötéssel, hogy az osztályoknak a ``django.db.models.Model`` osztályból kell származniuk, illetve az adatbázisban eltárolandó mezőket előre definiálnunk kell.

A képárba szerettem volna egy foto-blog szerű funkciót, ami annyit tesz, hogy a filerendszer böngészése közben megjelölhetnék képeket, amik aztán a megjelölés dátumának sorrendjében jelennének meg a *"blogban"*. A bejegyzéseknek szeretnék egy címet és címkéket adni.

Mivel a django alapból nem rendelkezik címke mezővel, ezért két lehetőségünk van: vagy mi magunk csinálunk valami hasonlót, vagy keresünk egy kész megoldást django app formájában, és azt használjuk. Én utóbbi mellett döntöttem - főként azért, hogy megmutassam hogyan kell egy külső django appot használni a projektünkben -, és `Alex Gaynor django-taggit <http://github.com/alex/django-taggit>`_ nevű munkáját választottam. Ahhoz, hogy elérhetővé váljon a modelljeink számára telepíteni kell (``pip install django-taggit``) és hozzáadni a ``settings.py`` modulunk ``INSTALLED_APPS`` listájához.
Ha ezzel kész vagyunk, készítsük el a modell definíciónkat a ``keptar`` appunk ``models.py`` moduljában:

.. sourcecode :: python

  class PBlogEntry(models.Model):

      path = models.CharField(max_length=1000, unique=True)
      title = models.CharField(max_length=200)
      user = models.ForeignKey(User)
      mark_date = models.DateTimeField('date marked', auto_now_add=True)
      tags = TaggableManager()

      class Meta:
          verbose_name = 'PBlog bejegyzes'
          verbose_name_plural = 'PBlog bejegyzesek'

      def is_valid(self):
          """ellenorzi, hogy a 'path' utvonalon levo file letezik-e"""  
          abspath = get_abspath(self.path)
          return os.path.isfile(abspath)

      @property
      def fdata(self):
          """a fizikai filehoz tartozo adatok"""
          return enrich([self.path])[self.path]

      def __unicode__(self):
          return u"%s (%s)" % (self.title, self.path)

Első körben a modell mezőit definiáljuk:
- ``path``: A kép elérési útja, ahogy listázáskor is hivatkozunk rá. Egyedi, azaz egy képet csak egyszer jelölhetünk meg blogbejegyzésnek.
- ``title``: A bejegyzésünk címe.
- ``user``: A felhasználó, aki megjelölte a képet. A ``ForeignKey`` adattípuson keresztül hivatkozhatunk más modell-objektumokra.
- ``mark_date``: A megjelölés dátuma. Az ``auto_now_add`` paraméter miatt ezt a django majd automatikusan kitölti nekünk.
- ``tags``: Az előbb installált ``django-taggit`` *varázs* mezője, ami a címkézést végzi.

Az adatmezőkön kívül más dolgok is helyet kaptak az osztályban, ne felejtsük el a modell nem csak a perzisztencia réteget, de az üzleti logikát is jelenti (bár jelen példát igen erős túlzás üzleti logikának nevezni :), annyit szerettem volna mondani ezzel, hogy nyugodt szívvel használjunk itt értelmes metódusokat, és ne a view-inkban manipulálgassuk a modell-objektumainkat valami varázs függvényekkel):

- ``is_valid``: Ellenőrzi, hogy a kép fizikailag megtalálható-e.
- ``fdata``: Egy olyan `property <http://django.hu/2010/9/1/a-descriptorok>`_, ami a fizikai filehoz tartozó infókat adja vissza.
- ``__unicode__``: Az objektum ``unicode`` reprezentációja, amikor valahol ``unicode``-dá (illetve stringgé) kell konvertálni az objektumot, akkor ez hívódik meg. A legegyszerűbb ilyen eset a ``print objektum`` parancs.

Természetesen attól az adatbázisunkba nem kerül bele az új modell sémája, mert beleírtuk a ``models.py`` fileba, ki kell ehhez adnunk pár parancsot::

  $ python manage.py validate
  0 errors found
  $ python manage.py syncdb
  ...

Ha mindezzel kész vagyunk, akkor parancssorból ki is tudjuk próbálni a modellünket. Ehhez a django szintén nyújt támogatást a ``shell`` management parancs formájában:

.. sourcecode :: python

  >>> from keptar.models import PBlogEntry
  >>> from django.contrib.auth.models import User
  >>> import datetime
  >>> e = PBlogEntry(path='proba/kep.jpg', title='Proba Kep', mark_date=datetime.datetime.now(), user=User.objects.get())
  >>> e.save() # ez menti el az adatbazisba
  >>> e.tags.add('proba')
  >>> e.tags.add('kep')
  >>> masike = PBlogEntry.objects.get() # mar az adatbazisbol szerdjuk ki a legelso PBlogEntry objektumot
  >>> masike.tags.all()
  [<Tag: proba>, <Tag: kep>]
  >>> print masike
  Proba Kep (proba/kep.jpg)

Ha az admin felületen is látni és piszkálni szeretnénk a modellünket, akkor ahhoz regisztrálnunk kell őt az admin appnál. Ezt a regisztációt elvileg bárhol megtehetnénk - pl. magában a ``models.py``-ben is, de érdemes az appunk gyökerébe egy ``admin.py`` nevű fileban megtenni, az admin app ezeket behúzza. A regisztráció maga egy ``admin.site.register(PBlogEntry)`` paranccsal megoldható lenne, de lehetőségünk van kicsit testre szabni az admin által generált listát, illetve formot, például:

.. sourcecode :: python

  from keptar.models import PBlogEntry
  from django.contrib import admin

  class PBlogEntryAdmin(admin.ModelAdmin):

      # a listaban metodusokat is szerepeltethetunk
      list_display = ('path', 'title', 'user', 'mark_date', 'is_valid')
      search_fields = ['path', 'title']
      date_hierarchy = 'mark_date'
      list_filter = ['user']

  admin.site.register(PBlogEntry, PBlogEntryAdmin)

Ha kész vagyunk, a fejlesztői szervert elindítva már láthatjuk is az új modellünket az admin oldalon, sőt az előbb felvett ``proba/kep.jpg`` elemünk is megvan, amiről látszik is a listában, hogy nem valid (javaslom ezért a törlését, mert csak bekavar később).

Űrlapok
-------

Gondolhatnánk, hogy ha már a django az admin felületre képes a modelleinkhez űrlapokat generálni, akkor miért ne lenne képes erre a műveletre a mi kérésünkre. És valóban, amellett, hogy a ``django.forms`` modul elemeiből kézzel készítenénk űrlapokat, az adminos mókához hasonlóan a modellekhez képes a django is űrlapot generálni (én ezeket szintén külön, a ``forms.py`` modulba szoktam elhelyezni):

.. sourcecode :: python

  from django import forms
  from keptar.models import PBlogEntry

  class PBlogEntryForm(forms.ModelForm):
      class Meta:
          model = PBlogEntry
          exclude = ('user')
          widgets = {
              'path': forms.HiddenInput(),
          }

Amint látható annyi a dolgunk, hogy leszármazunk a ``django.forms.ModelForm`` osztályból, és a belső ``Meta`` osztályon belül mondhatjuk meg, hogy pl. melyik modellhez szeretnénk űrlapot (``model = ModelClass``), illetve közölhetünk olyan dolgokat még a generátorral, hogy milyen mezők maradjanak ki (``exclude``), vagy hogy ha valami mezőt nem az alapértelmezett widgettel (*ez mi magyarul? építőelem?*) szeretnénk megjeleníteni (``widgets``).

A ``shell`` management parancs segítségével meg is nézhetjük, hogy hogyan néz ki a generált formunk, egyszerűen annyit kell tennünk, hogy példányosítjuk az osztályt:

.. sourcecode :: python

  >>> from keptar.forms import PBlogEntryForm
  >>> f = PBlogEntryForm()
  >>> print f.as_p() # ha siman kiiratjuk, akkor tr/td elemeket hasznal, amit en nem szeretek
  <p><label for="id_title">Title:</label> <input id="id_title" type="text" name="title" maxlength="200" /></p>
  <p><label for="id_tags">Tags:</label> <input type="text" name="tags" id="id_tags" /> A comma-separated list of tags.
  <input type="hidden" name="path" id="id_path" /></p>

Tehát ahhoz, hogy a form megjelenjen az oldalunkon, elég annyit tennünk, hogy a view-nkban létrehozunk egy ``PBlogEntryForm`` objektumot, ennek esetleg adunk néhány alapértelmezett értéket (pl. ``path``), ezt átadjuk a context objektumon keresztül a template-nek, ahol egy ``<form>`` tag-en belül kiíratjuk.

Helyezzük el hát az űrlapot a kép nézet oldalon, közvetlen a kép fölött, csak akkor, ha belépett felhasználó nézi az oldalt. Ehhez módosítani kell a ``showfile`` nevű view-nkat:

.. sourcecode :: python

  # reszlet a keptar/views.py filebol
  def showfile(request, fname):

      try:
          abspath = get_abspath(fname)
          fdata = enrich([fname])[fname]
      except:
          return HttpResponseForbidden('Access Forbidden')
      
      # ha be van lepve valaki, akkor beteheti a kepet a photoblogba
      if request.user.is_authenticated:
          try:
              # ha az elem mar szerepel az adatbazisban, akkor a formban az o
              # adatait szeretnenk latni
              form = PBlogEntryForm(instance=PBlogEntry.objects.get(path=fname))
          except PBlogEntry.DoesNotExist:
              # ha nem szerepel, akkor uj, ures formot szeretnenk
              form = PBlogEntryForm(initial={'path': fname})
      else:
          # nincs belepve senki, nem kell urlap
          form = None

      return render_to_response('showfile.html', {
          'pbform': form, # a template-nek pbform neven adjuk at az urlapot
          'parent': get_parent(fname),
          'fname': fname,
          'fdata': fdata,
          }, context_instance = RequestContext(request))

Illetve a ``templates/showfile.html`` template-ünkben is helyezzük el az űrlapot:

  Annyit tennék még hozzá, hogy a django alapértelmezetten bekapcsolt `CSRF <http://en.wikipedia.org/wiki/Cross-site_request_forgery>`_ védelemmel érkezik, azaz a ``settings.py`` modulban a ``MIDDLEWARE_CLASSES`` listában szerepel a ``django.middleware.csrf.CsrfViewMiddleware`` osztály. Ezesetben az összes űrlapunknál használni kell a ``{% csrf_token %}`` template-taget, ami egy ``hidden`` mezőben tartalmazni fogja a felhasználó biztonsági kódját, ami nélkül az űrlap érvénytelen.

.. sourcecode :: html

  {% extends 'base.html' %}

  {% block 'main' %}
  <h1>{{ fname }}</h1>
  <a href="{% url listdir parent %}">parent{% if parent %} ({{ parent }}){% endif %}</a>

  {% if pbform %}
  <form action="{% url submitpbentry %}" method="post">
    {% csrf_token %}
    {{ pbform.as_p }}
    <p><input type="submit" name="submitpbe" value="Ok" /></p>
  </form>
  {% endif %}

  <div>
    <img alt="{{ fname }}" src="{{ fdata.direct_url }}"/>
  </div>
  {% endblock %}

A ``form`` ``action`` paraméterének egy külön view-t adtam meg, ami az űrlap hibáinak kezelése szempontjából (*amit a django szintén ügyesen támogat, de most nem foglalkoznék vele*) nem feltétlen előnyös, viszont én szeretem külön tudni a form kezelő view-kat, leválasztva őket a tisztán megjelenítésért felelő részekről (kicsit controller-view jellegű szétválasztás, de ne erőltessük), illetve így könnyebb az űrlapot több különböző oldalon is használni. Az űrlap feldolgozó view ilyenkor egy átirányítással továbbítja a célhelyre a böngészőt, aminek az az előnye is megvan, hogy a böngésző *újratöltés* gombjának hatására nem küldi el újra az űrlapot. Lássuk hát az űrlap feldolgozó view-nkat:

.. sourcecode :: python

  def submitpbentry(request):

    # ha nincs belepve, akkor nem szabad
    if not request.user.is_authenticated:
        return HttpResponseForbidden('Access Forbidden')
    try:
        # ha az adott kep mar szerepel az adatbazisban, akkor az o adatait szeretnenk frissiteni
        f = PBlogEntryForm(request.POST, instance=PBlogEntry.objects.get(path=request.POST['path']))
    except PBlogEntry.DoesNotExist:
        # ha nem szerepel, akkor uj elemet hozunk letre a form alapjan
        f = PBlogEntryForm(request.POST)

    # ha a felhasznalot nem raknank hozza, akkor siman menthetnkenk,
    # igy viszont kulon kell menteni a kapcsolodo adatokat is (tag)
    pbe = f.save(commit=False)
    pbe.user = request.user
    pbe.save()
    # kapcsolodo adatok (tag-ek) mentese
    f.save_m2m()

    return HttpResponseRedirect(reverse('showfile', args=[pbe.path]))

Kicsit bonyolultabb eset ez annál, amivel kezdeni kellene (érdemes megnézni a jóval egyszerűbb `hivatalos django tutorial ide vonatkozó részét <http://docs.djangoproject.com/en/dev/intro/tutorial04/>`_), de jó példa arra, hogy adhatunk a beérkező űrlaphoz olyan adatokat, amit nem szeretnénk semmiképp a felhasználóra bízni. Természetesen az urljeink közé is fel kell venni az új view-t, amit az ``urls.py`` modulban az alábbi módon tehetünk meg:

.. sourcecode :: python

  urlpatterns = patterns('',
      # sokminden ...
      url(r'^submitpbe$', 'keptar.views.submitpbentry', name='submitpbentry'),
  )

Ezek után bőszen jelölgethetjük a képeinket, amiket utána az admin oldalon szerkeszthetünk is. Már csak egy új view/tempalte párosra van szükségünk, hogy blog szerűen nézegethessük a megjelölt képeket:

.. sourcecode :: python

  # keptar/views.py

    def pblog(request, id=None, slug=None):

      try:
          # ha az id nincs megadva, akkor a legutolsot jelenitjuk meg
          if id is None:
              pbe = PBlogEntry.objects.latest('mark_date')
          else:
              pbe = PBlogEntry.objects.get(pk=id)
      except PBlogEntry.DoesNotExist:
          # hibas id volt megadva, vagy nincs meg bejegyzes
          return render_to_response('pblog.html', 
              {}, 
              context_instance = RequestContext(request))

      # elozo es kovetkezo elem meghatarozasa idorendi sorrendben
      next = PBlogEntry.objects.filter(mark_date__gt=pbe.mark_date).order_by('mark_date')[:1]
      # python 2.6+ eseten ez sokkal szebb lenne: 
      # next = next[0] if len(next) > 0 else None
      if next:
          next = next[0]
      prev = PBlogEntry.objects.filter(mark_date__lt=pbe.mark_date).order_by('-mark_date')[:1]
      if prev:
          prev = prev[0]

      return render_to_response('pblog.html', {
          'pbe': pbe,
          'next': next,
          'prev': prev,
          }, context_instance = RequestContext(request))

.. sourcecode :: html

  {# templates/pblog.html #}
  {% extends 'base.html' %}

  {% block 'main' %}
  {% if pbe %}
  <h1>{{ pbe.title }}</h1>
  <div class="nav">
    {% if prev %}<a href="{% url pblog prev.id prev.title|slugify %}">Previous</a>{% endif %}
    <a href="{% url showfile pbe.path %}">Browse</a>
    {% if next %}<a href="{% url pblog next.id next.title|slugify %}">Next</a>{% endif %}
  </div>

  <h2 class="tags">Tags: 
    {% for tag in pbe.tags.all %}
    <span class="tag">{{ tag }}</span>{% if not forloop.last %}, {% endif %}
    {% endfor %}
  </h2>

  <div>
    <img alt="{{ pbe.title }}" src="{{ pbe.fdata.direct_url }}"/>
  </div>
  {% else %}
  <h1>The photoblog is still empty...</h1>
  {% endif %}
  {% endblock %}

.. sourcecode :: python

  # urls.py reszlet
  urlpatterns = patterns('',
      url(r'^pblog/(?P<id>\d+)/(?P<slug>[\w-]*)/$', 'keptar.views.pblog', name='pblog'),
      url(r'^pblog/(?P<id>\d+)/$', 'keptar.views.pblog'),
      url(r'^/?$', 'keptar.views.pblog'),
      # ...
  )

A sima ``/pblog/<id>/`` és a főoldal (``/``) url-én kívül legelső helyen egy olyan mintát adtam meg, ami az azonosító után egy *slugot* vár, ami egy betűkből, számokból és kötőjelből álló valami. Ezt is letárolhatnám a modellemben, de értelme leginkább azért van, hogy *szebbek* legyenek az url-ek, az ilyesmit a keresők is jobb helyre szokták sorolni, és az emberek is szívesebben kattintanak rá. Ezt a slugot a template-en belül a ``sulgify`` szűrővel készíthetjük el.

Elindítjuk, és **örülünk**!

  Időközben rájöttem, hogy finoman szólva buta dolog, hogy a ``settings.py``-be beledrótoztam a saját gépemen lévő képek elérési útját, ezért elnézést kérek, a `relimgdir <https://bitbucket.org/dyuri/djkeptar/src/relimgdir/>`_ mercurial címke alatt elérhető az a verzió, ahol azt átalakítottam egy relatív eléréssé, ami a projekt ``images`` könyvtára, illetve ide el is helyeztem két képet. Szóval, ha valaki csak úgy letölti és elindítja, akkor ez a verzió jó eséllyel produkál valami értelmes eredményt.

Konklúzió
---------

Mit is ad nekünk a django? Egy MVC jellegű keretrendszert, modell oldalon okos ORM támogatással, egy jól használható, kibővíthető template nyelvet, űrlap kezelést, URL routingot, middleware (*köztesréteg-modul? omg*) rendszert, egy meglepően jól használható automatikusan generált admin felületet, illetve ami szerintem a legnagyobb ereje - főként új project induláskor -, azok a könnyedén beépíthető alkalmazások rendszere. Mindemellett nagy előny, hogy nem köti meg a kezünket, a felsorolt dolgok közül semmit sem kötelező használnunk. Nem tetszik a template nyelv? Sebaj, használhatunk bármi más (python) template nyelvet, pl. `Jinjat <http://www.pocoo.org/projects/jinja2/>`_. Nem tetszik az űrlap kezelés (ez mondjuk meglepne), csinálhatunk sajátot, vagy ott van a `WTForms <http://wtforms.simplecodes.com/>`_. Az ORM a szűk keresztmetszet? Hát nem kötelező használni, használhatunk tisztán SQL-t, vagy akár valami nem relációs adatbázist is, pl. ott a `mongoengine <http://mongoengine.org/>`_ (*ez esetben mondjuk az automatikusan generált admin felülettől is el kell búcsúznunk*).

Próbáltam minél teljesebb képet adni, mégis most úgy érzem, hogy csak a felszínt karcolgattam. De hát ha nem lenne már miről írni, akkor az oldalra sem lenne szükség tovább :) Mindenkinek örömteli ismerkedést kívánok a djangoval, és ha kérdésetek van, ne tartsátok magatokban! Természetesen a projekt messze nincs még kész, ha időm engedi folytatni fogom, és ha valami érdekeset csinálok, akkor arról megpróbálok beszámolni. Egyébként meg az egész fent van a `bitbucketen <http://bitbucket.org/dyuri/djkeptar/>`_, szabad forkolni, és szívesen veszem a *pull-requesteket* :)

..

  A cikksorozat részei:
  
  - `Django, egy példán keresztül I. - Az alapok <http://django.hu/2010/10/14/django-egy-peldan-keresztuel-i>`_
  - `Django, egy példán keresztül II. - View-k és template-ek <http://django.hu/2010/10/15/django-egy-peldan-keresztuel-ii>`_
  - `Django, egy példán keresztül III. - A modell <http://django.hu/2010/10/20/django-egy-peldan-keresztuel-iii>`_

  A teljes projekt szabadon elérhető a `bitbucketen <http://bitbucket.org/dyuri/djkeptar/>`_.

