View-k és template-ek
---------------------

Djangoban a ``view``-k felelnek meg nagyjából az *MVC minta* controllereinek. Tipikusan olyan függvények - vagy függvényként viselkedő objektumok -, amelyekhez hozzá van rendelve valamilyen URL-minta, és ha a felhasználó a böngészőjébe az adott mintának megfelelő URL-t ír be, akkor a ``view`` lefut, az általa visszaadott válasz (általában valami ``HttpResponse`` objektum) pedig a megfelelő formában visszajut a böngészőbe, és ott megjelenik a kívánt tartalom. 


URL kezelés
-----------

Természetesen, hogy milyen URL-minta esetén milyen ``view`` fusson le, azt nekünk kell megadnunk, amit nagyon egyszerűen a projekt könyvtárában található ``urls.py`` fileban tehetünk meg. Az itt található ``urlpatterns`` listát kell bővítgetnünk ``url(regularis kifejezes, view függvény [, egyéb opcionális paraméterek, például a view-nak átadandó argumentumok])`` bejegyzésekkel. (Az ``url`` függvény meghívása helyett használhatunk sima python felsorolásokat (tuple), ez esetben a django maga hívná meg velük az ``url`` függvényt. Én szeretem kiírni.)

A reguláris kifejezés lesz a minta, amire illeszkednie kell az URL-nek, egyébként egy hagyományos python regexp (``r'minta'``), ami ha tartalmaz nevesített illesztéseket (pl. ``(?P<postid>\d+)``), akkor azokat a view függvényünk paraméterként megkapja.

Az egyszerűség kedvéért a view függvény konkrét megadása helyett megadhatjuk csak a pontokkal elválasztott elérési útját, mint stringet (*dotted path*), sőt, ha valamelyik appunk rendelkezik saját ``urls.py``-vel, arra itt hivatkozhatunk az ``include(appneve.urls)`` direktíva segítségével.

Lássunk egy példát az egészre (``urls.py``):

.. sourcecode:: python

  from django.conf.urls.defaults import *
  
  from django.contrib import admin
  admin.autodiscover()

  urlpatterns = patterns('',
    url(r'^/?$', 'app.views.index'),
    url(r'^page/(?P<page_id>\d+)/(?P<slug>[\w-]+)/$', 'app.views.page'),
    url(r'^about/$', 'app.views.page', {'page_id': 1, 'slug': 'about'}),
    url(r'^admin/', include(admin.site.urls)),
  )

A fenti példában a főoldal lekérésekor az ``index`` nevű view fut le, a ``/page/2/valami/`` meglátogatásakor a ``page`` nevű view hívódik meg ``page_id=2`` és ``slug='valami'`` argumentumokkal, a ``/about/`` hatására szintén a ``page`` fut le, de az előre megadott paraméterekkel, míg ha az URL ``/admin/``-nal kezdődik, akkor az ``admin.site.urls`` modul szerint folytatódik a view-feloldás.

  Vannak, akik nem ilyen központosított módon szeretik tárolni az url-szabályaikat, hanem valahogy a view közelében szeretnék a mintát a view-hoz hozzárendelni. Kis trükkel erre is van lehetőség, például itt található `egy dekorátoros megoldás <http://djangosnippets.org/snippets/1671/>`_.

A view-k
--------

Ahogy fentebb írtam, a view-k djangoban egyszerű függvények. Első bemenő paraméterük kötelezően egy ``HttpRequest`` objektum - ezen keresztül jutnak hozzá a GET, POST, session és egyéb hasonló dolgokhoz -, illetve egy HttpResponse objektumot adnak vissza futás után. Nézzünk erre egy egyszerű példát:

.. sourcecode:: python

  from django.http import HttpResponse

  def index(request):
    return HttpResponse('Helló világ!')

Ez így szuper egyszerű, viszont igen rondán nézne ki, ha komplett HTML oldalakat írnánk meg szövegként a view-inkon belül, ezért ezt a megoldást elég ritkán alkalmazzuk. Helyette template-eket használunk, azokban írjuk le a visszaadni kívánt adatok megjelenését, a view-kban ezeket a template-eket renderelejük visszaadható állapotba.

Egyébként a sima ``HttpResponse`` mellett a django rendelkezik még ennek speciális leszármazottaival, melyekkel egyszerűen tudunk szabványos módon átírányítani (``HttpResponseRedirect``), vagy hibaüzeneteket visszaadni (``HttpResponseForbidden``, ``HttpResponseNotFound``). A *Not found (404)* hibaüzenetet egyébként a Http404 exception (*kivétel*) dobásával is elérhetjük, ez sok esetben kényelmesebb.

Egy példa a template használatra:

.. sourcecode :: python
  
  # views.py
  from django.template import Context, loader
  from django.http import HttpResponse

  def hello(request, name='Látogató'):
    if name = 'Sanyi':
      # Sanyit nem szeretjuk, neki nem koszonunk
      return HttpResponseForbidden('Utállak...')

    t = loader.get_template('hello.html')
    c = Context({
      'name': name
    })

    return HttpResponse(t.render(c))

.. sourcecode :: html

  {# hello.html #}
  <html>
  <h1>Hello kedves {{ name }}!</h1>
  <p>Hogy vagy?</p>
  </html>

A rendereléshez szükséges megadni a kontextust, egy ``Context`` objektum formájában, ami kb. egy python *dict*-et tartalmaz, ennek segítségével adhatunk át adatokat a tempalte-nek. Mivel sok app igényli, hogy ``request`` is elérhető legyen a template-ből, ezért én sima ``Context`` helyett ``RequestContext``-et szoktam használni, ami ugyan olyan, csak második argumentumként meg kell neki adni a ``request`` objektumot.

Az utolsó néhány művelet a legtöbb esetben mindig ugyanígy szerepelne a view függvényeinkben, ezért a djangos srácok csináltak rá egy wrapper függvényt, hogy egyszerűsítsék a dolgokat, íme az előző view tömörebben:

.. sourcecode :: python

  # views.py
  from django.shortcuts import render_to_response

  def hello(request, name='Látogató'):

    return render_to_response('hello.html', {'name': name})

A tempalte-ek
-------------

A django template nyelve nem fog sok meglepetést okozni azoknak, akik használtak már valamilyen template nyelvet. A vezérlési szerkezeteket ``{%`` és ``%}`` közé kell tenni, a változók értékét ``{{ valami }}`` módon írathatjuk ki, illetve megjegyzéseket is írhatunk hasonló módon: ``{# megjegyzés #}``.
A template-ekben blokkokat definiálhatunk, leszármazhatunk belőlük - és a leszármazottban felüldefiniálhatjuk a blokkokat, illetve saját template-tageket is tudunk készíteni.

A ``settings.py`` fileban a ``TEMPLATE_DIRS`` listában tudjuk megadni, hogy a django hol keresse a tempalte-eket, emellett a django még benéz a telepített app-ok ``templates`` könyvtárába is, ha valamit nem talál az általunk megadott helyeken.

Vissza a képtárhoz
------------------

Első lépésben amolyan file-browsert akartam csinálni a képtárhoz. Egy (``settings.py``-ben megadott) könyvtár tartalmát böngészhetné a felhasználó, és az itt található képeket nézhetné meg. Csináltam pár általánosabb - djangotól független - függvényt, amiket az ``utils.py`` modulban helyeztem el a ``keptar`` appon belül.

  Az ``utils.py`` tartalma nem témája a tutorialnak, de nyugodtan bele lehet nézni, fileok és könyvtárak listázásra, thumbnail készítésére, és egyéb hasonló dolgokra találhatók benne függvények.

Két view-t definiáltam ebben a lépésben, az egyik egy konkrét kép, a másik pedig egy könyvtár tartalmának megjelenítésére képes (csak a lényeg):

.. sourcecode :: python
  
  # views.py
  from keptar.utils import get_filelist, get_abspath, get_parent, enrich

  def listdir(request, path=""):

      try:
          files = get_filelist(path)
      except:
          return HttpResponseForbidden('Access Forbidden')

      return render_to_response('listdir.html', {
          'path':     path,
          'parent':   get_parent(path),
          'files':    files,
          }, context_instance = RequestContext(request))

  def showfile(request, fname):

      try:
          abspath = get_abspath(fname)
          fdata = enrich([fname])[fname]
      except:
          return HttpResponseForbidden('Access Forbidden')

      return render_to_response('showfile.html', {
          'parent': get_parent(fname),
          'fname': fname,
          'fdata': fdata,
          }, context_instance = RequestContext(request))

.. sourcecode :: html

  {# base.html #}
  <!doctype html>
  <html>
  <head>
    <meta charset="utf-8"/>
    <title>{% block 'title' %}Keptar{% endblock %}</title>
    <link rel="stylesheet" href="/media/css/style.css"/>
  </head>
  <body>
    <div id="container">
      <div id="main">
      {% block 'main' %}
      {% endblock %}
      </div>
    </div>
  </body>
  </html>

.. sourcecode :: html

  {# listdir.html #}
  {% extends 'base.html' %}
  {% block 'main' %}
  <h1>{{ path }}</h1>
  <a href="{% url listdir parent %}">parent{% if parent %} ({{ parent }}){% endif %}</a>

  <ul>
  {% for fname,fdata in files.items %}
    <li><a href="{{ fdata.url }}"><img alt="{{ fname }}" src="{{ fdata.thumb }}"/> {{ fname }}</a></li>
  {% endfor %}
  </ul>
  {% endblock %}

.. sourcecode :: html
  
  {# showfile.html #}
  {% extends 'base.html' %}
  {% block 'main' %}
  <h1>{{ fname }}</h1>
  <a href="{% url listdir parent %}">parent{% if parent %} ({{ parent }}){% endif %}</a>

  <div>
    <img alt="{{ fname }}" src="{{ fdata.direct_url }}"/>
  </div>
  {% endblock %}

Amint látható maguk a viewk nem túl bonyolultak, az ``utils.py`` függvényei segítségével lekértük a file/könyvtár listát, illetve a kép adatokat (*amit jelen esetben felfoghatunk modellnek is*), majd az adatokkal lerendereltettük a megfelelő template-et.

Az ``if`` és a ``for`` tempalte-tageket nem magyaráznám, ellenben említést érdemel az ``url`` tag, ami ``{% url viewneve param1 param2 %}`` módon visszaadja az adott view adott paraméterezéséhez tartozó URL-t az érvényben lévő ``urls.py`` alapján. Ha már szóba került, vegyük fel bele az új view-kat:

.. sourcecode :: python

  urlpatterns = patterns('',
    url(r'^/?$', 'keptar.views.listdir'),
    url(r'^list/(?P<path>.*)$', 'keptar.views.listdir', name='listdir'),
    url(r'^show/(?P<fname>.*)$', 'keptar.views.showfile', name='showfile'),
    url(r'^admin/', include(admin.site.urls)),
  )

..
  
  A ``base.html`` template-ben hivatkozok külső stíluslapra is (``style.css``), amit a django is ki tud szolgálni statikus tartalomként, ehhez fel kell venni az url minták közé az alábbi sort:

  .. sourcecode :: python
    
    url(r'media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

  Természetesen éles üzemben ezt nagyon nem javaslom, a webszerver maga sokkal gyorsabban tud kiszolgálni statikus fileokat, mint a django.

Az extra ``name`` paraméterrel hivatkozhatunk a szabályunkra rövid névvel az ``{% url %}`` tagben.

Ahogy említettem az általam használt paramétereket is a ``settings.py``-ben kell beállítani, így nem kell a felhasználóknak valami extra fileban is turkálniuk, ha az alkalmazásomat ők is használni szeretnék:

.. sourcecode :: python

  KEPTAR_ROOT='/var/www/foto'
  KEPTAR_URL='http://dyuri.horak.hu/foto/'
  KEPTAR_EXTENSIONS=['jpg','jpeg','png']
  KEPTAR_THUMBDIR='.tn'
  KEPTAR_THUMBSIZE=(120,120)
  KEPTAR_SHOW_HIDDEN=False
  KEPTAR_ICONS={
    'dir': 'http://dyuri.horak.hu/keptar/icons/tn_dir.jpg',
  }

A kódból ezeket a változókat egyébként az alábbi módon érhetjük el:

.. sourcecode :: python

  from django.conf import settings
  valami = settings.KEPTAR_ROOT

Elvileg kész is vagyunk, a fejlesztői szervert futtatva (``python manage.py runserver``) böngészhetjük is a ``settings.KEPTAR_ROOT`` könyvtár tartalmát.
Az előző cikkhez hasonlóan a forrás `megtekinthető a bitbucketen <http://bitbucket.org/dyuri/djkeptar/src/cikk2>`_ ``cikk2`` címke alatt. A következő cikkre lehet picit többet kell majd várni, mint erre :)

..

  A cikksorozat részei:
  
  - `Django, egy példán keresztül I. - Az alapok <http://django.hu/2010/10/14/django-egy-peldan-keresztuel-i>`_
  - `Django, egy példán keresztül II. - View-k és template-ek <http://django.hu/2010/10/15/django-egy-peldan-keresztuel-ii>`_

