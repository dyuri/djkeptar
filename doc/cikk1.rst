Az alapok
---------

Ahogy korábban már írtam, régebb óta tervezem valami tutorial szerűség megírását, hát végre eljutottam ide - kicsit lassabban, mint terveztem, az utóbbi időszak nem várt eseményei miatt. A teljes tutorial több cikket fog magába foglalni, ez az első rész a django környezet kialakításáról fog szólni.

A folyamatot egy olyan példán keresztül szeretném bemutatni, amit később saját célra használni is fogok, néhány ponton ezért lehet, hogy nem a legegyszerűbb megoldásokat alkalmazom. A problémakört más irányból közelítem meg, mint a `hivatalos django tutorial`_, ezért azt sem árt átnézni, illetve csak ajánlani tudom a `django dokumentációját`_, ami szerintem kifejezetten jó.

.. _`hivatalos django tutorial`: http://docs.djangoproject.com/en/dev/intro/tutorial01/
.. _`django dokumentációját`: http://docs.djangoproject.com/en/


A környezet kialakítása
-----------------------

Mielőtt rátérnénk a djangos környezet kialakítására, mindenkinek ajánlom figyelmébe Gábor barátom nemrégiben publikált `Fejlesztői környezet kialakítása Python alapú fejlesztéshez`_ című írását, én is nagyon hasonlóan szoktam eljárni minden új projektecske esetében. Ebben az esetben is első lépésként létrehoztam egy ``djkeptar`` nevű környezetet, majd ide installáltam a szükséges dolgokat::

  $ mkvirtualenv djkeptar
  $ workon djkeptar
  $ pip install ipython django pysqlite

Az egyszerűség kedvéért ``sqlite`` adatbazist használtam, kisebb dolgokhoz és fejlesztéshez tökéletes, nem kell szenvedni *rendes* adatbázis szerverrel.
Ezután a ``django-admin.py`` parancs segítségével hozhatjuk létre a django projektünket. Én szeretem minden kódomat verziókezelő rendszerben tárolni, így rendszeres commitolgatás mellett nem gond visszatérni valami korábbi állapotra, könnyen meg tudom osztani másokkal, és a modern DVCS-eknek hála több helyre is elküldhetem, hogy biztonságban tudjam. Én magam a `Mercurial`_-t preferálom (python ugyebár), de ugyanolyan jó tapasztalataim vannak a ``git``-tel is, ráadásul aki az egyiket megismeri, az a másikkal is el fog boldogulni.

::

  $ django-admin.py startproject djkeptar
  $ cd djkeptar
  $ hg init
  $ hg add
  $ hg commit -m 'project letrehozasa'

A django egyik alapja a beilleszthető/újrafelhasználható alkalmazások (*pluggable/reusable apps*) rendszere, ami a DRY (*don't repeat yourself*) filozófiát követi, azaz ha már egyszer megcsináltál valamit (esetleg valaki más csinálta meg), akkor felesleges újra megcsinálni, használjuk azt, ami már kész, és valaki már valószínűleg lefutotta azokat a köröket vele, amit nekünk kéne, ha újat csinálnánk. Az interneten kb. végtelen ilyen django appot találunk, vannak közöttük egész jók, tehát mielőtt valami újba belekezdünk, mindenképp érdemes körbenézni - és ha számunkra tökéletes megoldás nem is született még, egy forkolásra megérett verziót nagy valószínűséggel találunk. (Például saját blogot mindenki írt/ír/írni fog djangoban. Tökéletest még nem láttam.)

Mivel minden lényegi munkát ezek az appok csinálnak, ezért bármit szeretnénk csinálni, készítenünk kell hozzá egy appot::

  $ python manage.py startapp keptar

A parancs semmi mást nem csinál, csak létrehoz egy ``keptar`` nevű könyvtárat - ami egy python modul lesz egyébként - és a könyvtárban pár kvázi-üres python filet::

  keptar/
      __init__.py
      models.py
      tests.py
      views.py

A file-ok nevei elég beszédesek, a ``models.py`` fogja tartalmazni az alkalmazásunk modell részét, a ``views.py`` a view-kat, a ``tests.py`` meg a teszteket. Az elnevezésekből már látszik, hogy django egy `MVC-szerű`_ framework, de mivel (szerintem) a webes világra a `hagyományos MVC minta`_ jelenleg csak kicsit erőltetve illeszthető rá, ezért ők ki is mondják, hogy csak valami hasonlót csinálnak.

Beállítások
-----------

A következő lépés a django projektünk konfigurálása, melyet a ``settings.py`` file-on keresztül lehet megtenni. (Illetve a témában az oldalon is született már `néhány <http://django.hu/2010/10/8/settings-modul-egy-jobb-megkozelites>`_ `bejegyzés <http://django.hu/2010/8/17/eltero-kornyezetek-beallitasainak-kezelese-djangoval>`_.)

Itt mindenképpen állítsuk be az adatbázishoz kapcsolódó paramétereket, illetve adjuk hozzá a készülő alkalmazásunkat és az admin alkalmazást az ``INSTALLED_APPS`` listához (csak a lényeg, ami nem maradt alapértelmezetten):

.. sourcecode:: python

  import os.path
  PROJECT_DIR = os.path.dirname(__file__)
  DATABASES = { 'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(PROJECT_DIR, 'keptar.sqlite'),
  }}
  MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')
  TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates'),
  )
  INSTALLED_APPS = (
    # nehany default, azokat ne bantsuk
    'django.contrib.admin',
    'keptar',
  )

Amint látható egy apro trükköt alkalmaztam a direkt elérési úttal megadandó dolog helyének megállapításához, mégpedig hogy a file elején megállapítom az ő helyét a filerendszeren, és ehhez képest relatív módon adom meg a többit (pl. ``MEDIA_ROOT`` vagy ``TEMPLATES_DIR``).

Szinte kész is vagyunk, az ``urls.py`` file-ban (*erről bővebben majd később*) engedélyezzük az admin elérését:

.. sourcecode:: python

  from django.conf.urls.defaults import *
  from django.contrib import admin
  admin.autodiscover()

  urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
  )

Szinkronizáljuk az adatbázist az appjaink modelljeivel::

  $ python manage.py syncdb

Erre azért van szükség, mert - bár mi magunk még nem készítettünk semmi olyat, aminek adatbázisban a helye - az admin felülethez, illetve a felhasználok kezeléséhez alapból tartoznak modellek. Első futtatáskor rá is kérdez az első *admin* felhasználó adataira.
Később, ha új appot adunk a rendszerhez, vagy változik a modellünk(*), akkor a ``syncdb`` management parancs újbóli futtatása szinkronizálja a változásokat.

  (*): Ez azért sajnos nem ennyire egyszerű, ha egy már beszinkronizált modellünk sémája változik, azt az alap django nem tudja kezelni. 
  Azonban erre is van megoldás, mégpedig a `south`_, amit én előre látó módon a példa projektben el is helyeztem, de most nem szeretnék róla írni, mert külön cikket érdemel.

Ha minden jól ment, akkor a környezet létrehozásával kész is vagyunk, a fejlesztői szervert futtatva ellenőrizhetjük, hogy minden rendben működik-e::

  $ python manage.py runserver
  Validating models...
  0 errors found

  Django version 1.2.3, using settings 'djkeptar.settings'
  Development server is running at http://127.0.0.1:8000/
  Quit the server with CONTROL-C.

A fejlesztői szervert más porton (illetve publikus IP címen) is elindíthatjuk, simán paraméterként ``[[ip/host:]port]`` módon megadva, pl::

  $ python manage.py runserver djkeptar.hu:5000

Kész is vagyunk a környezet létrehozásával, sőt, a böngészőnkbe beírva a ``http://localhost:8000/`` URL-t egy szép 404-es hibaüzenet fogad minket, mellyel akkor találkozhatunk, ha a ``settings.py``-ben a ``DEBUG`` változó értéke ``True``. (Éles rendszeren ez szigorúan tilos!)

A hibaüzenetben látszik, hogy bár az üres (``/``) címen nincs semmi, de a ``/admin/`` címen van valami. Ezt megnézve a djangotól *"ingyen"* kapott admin felülettel találkozhatunk, ahol jelen pillanatban felhasználókat tudunk csak kb. létrehozni. Érdemes ismerkedni vele, nagyon hasznos dolog, fejlesztés kezdeti szakaszában tökéletesen használható, sőt van annyira flexibilis, hogy az esetek nagy részében sikerül a megrendelő kívánságainak megfelelően testre szabni, és így megspórolhatjuk egy teljesen új admin felület létrehozását.

Összegzés
---------

Létrehoztunk tehát egy django projektet, ami már képes a futásra, használ adatbázist, felhasználókat kezel, de egyébként semmire nem jó :)

Látható, hogy még így management parancsokkal megtámogatva is sok olyan lépes van, amit minden egyes új projektünknél végre kéne hajtani - bár valószínűleg nem készítünk naponta többtíz ilyet, ezt mégis fel lehet picit gyorsítani, pl. ha egy közepesen felkonfigurált django projektet eltárolunk kedvenc verziókezelőnkben, majd azt vesszük alapul a következőknél. (pl. íme `Gábor saját django-boilerplate-je <http://github.com/nyuhuhuu/django-boilerplate>`_)

A tutorialnak természetesen még nincs vége - ennek a cikknek viszont igen -, ígérem rövidesen folytatom majd a *view*-k és *template*-ek témakörével.
Addig is a példám forrása elérhető a `bitbucketen <http://bitbucket.org/dyuri/djkeptar>`_, konkrétan az ehhez a cikkhez tartozó állapot a `cikk1 címke <http://bitbucket.org/dyuri/djkeptar/src/cikk1>`_ alatt tekinthető meg. Kis segítség::

  $ hg clone http://bitbucket.org/dyuri/djkeptar
  $ cd djkeptar
  $ hg co cikk1

.. _`Fejlesztői környezet kialakítása Python alapú fejlesztéshez`: http://weblabor.hu/blog/20100831/python-fejlesztoi-kornyezet
.. _`Mercurial`: http://mercurial.selenic.com/
.. _`MVC-szerű`: http://docs.djangoproject.com/en/dev/faq/general/#django-appears-to-be-a-mvc-framework-but-you-call-the-controller-the-view-and-the-view-the-template-how-come-you-don-t-use-the-standard-names
.. _`hagyományos MVC minta`: http://en.wikipedia.org/wiki/Model%E2%80%93View%E2%80%93Controller
.. _`south`: http://south.aeracode.org/

