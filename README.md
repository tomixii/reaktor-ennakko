# CO<sub>2</sub> Emissions Hub

Tämä työkalu on toteutettu Reaktorin kesätöitä varten ennakkotehtävänä. Tällä työkalulla käyttäjä voi tutkia maailman top 20 listaa eniten saastuttavista maista(per asukas) eri vuosilta sekä katsoa mikä on ollu suurvaltojen rooli maapallon hiilidioksidipäästöissä historian aikana. Työkalulla on mahdollista tutkia tilannetta vuodesta 1960 vuoteen 2014. Data työkalua varten on saatu osoitteesta http://www.worldbank.org/. 

Työkalua voi käyttää osoitteessa https://reaktor-ennakko.herokuapp.com

## API

Työkaluun on toteutettu myös yksinkertainen api tiedon hakemista varten.

`/api/co2/<maan nimi>` antaa käyttäjälle kyseisen maan tai alueen hiilidioksidipäästötiedot vuosilta 1960-2014, jos sellaisia on olemassa

`/api/population/<maan nimi>` antaa käyttäjälle kyseisen maan tai alueen asukaslukutiedot vuosilta 1960-2014, jos sellaisia on olemassa

`/api/co2/<maan nimi>/<vuosi>` antaa käyttäjälle kyseisen maan tai alueen hiilidioksidipäästötiedot tietyltä vuodelta, jos sellaisia on olemassa

`/api/population/<maan nimi>/<vuosi>` antaa käyttäjälle kyseisen maan tai alueen asukaslukutiedot tietyltä vuodelta, jos sellaisia on olemassa

## Teknologiat

Työkalun kehityksessä on käytetty backend puolella Python Flaskia ja frontend pyörii Vue.js:n avulla.
