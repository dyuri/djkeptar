Djkeptar
========

Django alapu keptar, valami tutorial szerunek kezdtem, a `django.hu <http://www.django.hu>`_ oldalra. Aztan remelem majd tulnovi magat :)

PDF generalas
-------------

  rst2pdf full.rst -o djkeptar.pdf -s freetype-serif

Google closure compiler
-----------------------

Ha a javascriptet le szeretnenk forditani google closure compilerrel, akkor azt igy kell:

  python2 djkeptar/media/keptar/js/closure-library/closure/bin/build/closurebuilder.py \
  --namespace=djkeptar.init \
  --root=media/keptar/js \
  --output_mode=compiled \
  --compiler_jar=compiler.jar \
  > compiled.js
