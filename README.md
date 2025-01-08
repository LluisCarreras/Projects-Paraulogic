# Paraulògic

En aquesta pàgina es mostra la solució del <a href="https://www.vilaweb.cat/paraulogic/">Paraulògic</a> del dia actual. I què es el Paraulògic? Bé, es tracta d'un joc ligüistic que s'actualitza cada dia i en le qual el jugador disposa de set lletres (encara que a vegades només son sis), que es mostren en sis hexàgons blaus i un de vermell, col·locats com si fossin les cel·les d'un rusc, amb l'hexàgon vermell al mig. L'objectiu del joc és trobar totes les paraules possibles a partir d'aquestes lletres, amb la condició de que sempre han de contenir la lletra de l'hexàgon central del rusc (el de color vermell), i poguent-se repetir les lletres tantes vegades com calgui. Això sí, només s'admeten les paraules  que tenen un mínim de tres lletres, i només s'accepten les paraules que figuren al Diccionari de la llengua catalana de l'Institut d'Estudis Catalans (DIEC).

Aquest projecte ha suposat a la vegada una mena de divertiment i un repte de programació pel seu autor. De cap manera intenta privar del gaudi que suposa intentar resoldre per un mateix el Paraulògic, i el propi autor s'absté de fer-lo servir per resoldre'l, ja que l'objectiu final d'aquest joc és passar una bona estona a la vegada que es fa una mena de gimnàsia mental. 

Els reptes tècnics que han sorgit en el desenvolupament del projecte es poden resumir en la següent llista:

- Per trobar les paraules que formen part de la solució del Paraulògic és necessari tenir les paraules del DIEC, i això no ha estat possible d'una manera formal. Per tant, s'hagut de fer una tasca prèvia de scrapping de la pàgina web del DIEC per poder obtenir aquesta llista de paraules.
- Al Paraulògic les paraules s'introdueixen sense signes d'accentuació, dièresi, punts volats de les eles geminades ni guions. Per tant, a la llista de paraules original obtinguda amb scrapping se li han hagut d'aplicar uns processos de neteja per adaptar-les al format que admet el Paraulògic.
- Cada dia el Paraulògic s'actualitza amb un joc nou, el que suposa que canvien les lletres amb que es juga. Ha calgut fer una tasca de scrapping amb Selenium, ja que les dades de les lletres en joc es mostren a la pàgina del Paraulògic a partir d'una pàgina dinàmica.
- S'ha hagut de desenvolupar un algoritme eficaç i eficient per trobar les paraules contingudes a la llista que suposen una solució a partir de les lletres que es proposen.
- Per automatitzar aquestes tasques s'ha fet servir una Gitgub Action, amb la que s'obté la solució actualitzada del Paraulògic del dia actual.
- La solució es mostra en una web de GitHub, que es pot veure a [Solució del Paraulògic](https://lluiscarreras.github.io/Projects-Paraulogic/paraulogic.html).






