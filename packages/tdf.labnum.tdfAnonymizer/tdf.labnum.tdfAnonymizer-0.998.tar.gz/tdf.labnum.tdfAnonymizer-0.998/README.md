# Tests du package tdf.labnum.tdfAnonymizer

1. Positionnement dans le répertoire de test

`cd tests`

2. Installation des requirements

`python -m pip install -r requirements.txt`

3. Installation du modèle spacy pour le module de NLP

`python -m spacy download fr_core_news_sm`

4. Modification du fichier de données à anonymiser => data.txt (en utf-8)

<pre>
1. Résumé de l'incident :
     
    A 12h50 le 11/12/2023 - Roger TAYLOR (stephane.rigaux@gmail.com) et Pierre ARDITI (responsable du site web https://www.google.com) de la cellule AGCP ont détecté que le boitier iqoya de ORANGE était en erreur. 
    Cela a mise dans le noir 350 utilisateurs sur le réseau en France. La valeur seuil était de 34.67°C en Occitanie

2. Chronologie des faits :
   11/12/2023 - 21 : 50 : tests2 en fin de traitement chez BOUYGUES à Marseille
   12/12/2023 - 11: 59: test3 qui va s'arréter à partir de 03:34 sur paris. test4 n'a plus d'avenir vers 23: 34 depuis que C8 a déposé le bilan à Brest et ailleurs
    => CR FINAL Transmis ;code cloture =[ENT7 - IT - Probl. de mise en place] 
   - Com: 19/12/2023 11h45 : [Constat à l'arrivée]='Erreur de config détectée' décalage dans la séquence de démarrage des opérations. La reprogrammation des paramètres a permis de résoudre le problème.!!!... 

    Temps d'arrêt : 30 minutes. Tests de validation : OK. ENT7: 100% CPU, 8GB RAM, 250GB stockage dispo. Le système est maintenant opérationnel et stable. CR FINAL Transmis ;code cloture =[ENT8 - ADM - Probl. d'accès aux données] - Com: 05/11/2022 09h20 : [Constat à l'arrivée]='Erreur config réseau' problème d'authentification avec le serveur. La réinitialisation du MDP et la mise à jour des paramètres de connexion ont permis de résoudre le problème.!!!... 
    Tous les utilisateurs peuvent désormais accéder aux données sans aucun problème.**
</pre>





5. Exemple de lancement de l'anonymisation

`python launcher_anonymisation.py`


<pre>
<details><summary>Click to expand</summary>
====================================================================================================
Texte initial
====================================================================================================
1. Résumé de l'incident :

    A 12h50 le 11/12/2023 - Roger TAYLOR (stephane.rigaux@gmail.com) et Pierre ARDITI (responsable du site web https://www.google.com) de la cellule AGCP ont détecté que le boitier iqoya de ORANGE était en erreur.
    Cela a mise dans le noir 350 utilisateurs sur le réseau en France. La valeur seuil était de 34.67°C en Occitanie

2. Chronologie des faits :
   11/12/2023 - 21 : 50 : tests2 en fin de traitement chez BOUYGUES à Marseille
   12/12/2023 - 11: 59: test3 qui va s'arréter à partir de 03:34 sur paris. test4 n'a plus d'avenir vers 23: 34 depuis que C8 a déposé le bilan à Brest et ailleurs
    => CR FINAL Transmis ;code cloture =[ENT7 - IT - Probl. de mise en place]
   - Com: 19/12/2023 11h45 : [Constat à l'arrivée]='Erreur de config détectée' décalage dans la séquence de démarrage des opérations. La reprogrammation des paramètres a permis de résoudre le problème.!!!...

    Temps d'arrêt : 30 minutes. Tests de validation : OK. ENT7: 100% CPU, 8GB RAM, 250GB stockage dispo. Le système est maintenant opérationnel et stable. CR FINAL Transmis ;code cloture =[ENT8 - ADM - Probl. d'accès aux données] - Com: 05/11/2022 09h20 : [Constat à l'arrivée]='Erreur config réseau' problème d'authentification avec le serveur. La réinitialisation du MDP et la mise à jour des paramètres de connexion ont permis de résoudre le problème.!!!...
    Tous les utilisateurs peuvent désormais accéder aux données sans aucun problème.


====================================================================================================
Texte anonymisé
====================================================================================================
1. Résumé de l'incident :

A 12h50 le 11/12/2023 - Trudi Philippa (fakemail1@mabal.fr) et Pierre ARDITI (responsable du site web fakewebsite1@monsite.fr) de la cellule DC ont détecté que le boitier codecaudio de ORANGE était en erreur.
Cela a mise dans le noir 350 utilisateurs sur le réseau en France. La valeur seuil était de 34.67°C en Occitanie

2. Chronologie des faits :
11/12/2023 - 21h50 : tests2 en fin de traitement chez AFNOR à Marbeuf
12/12/2023 - 11h59 : test3 qui va s'arréter à partir de 03h34 sur paris. test4 n'a plus d'avenir vers 23h34 depuis que CNEWS a déposé le bilan à Rebreuviette et ailleurs
=> CR FINAL Transmis ;code cloture =[ENT7 - RRI - Probl. de mise en place]
- Com: 19/12/2023 11h45 : [Constat à l'arrivée]='Erreur de config détectée' décalage dans la séquence de démarrage des opérations. La reprogrammation des paramètres a permis de résoudre le problème. !!!...

Temps d'arrêt : 30 minutes. Tests de validation : OK. ENT7: 100% CPU, 8GB RAM, 250GB stockage dispo. Le système est maintenant opérationnel et stable. CR FINAL Transmis ;code cloture =[ENT8 - ADM - Probl. d'accès aux données] - Com: 05/11/2022 09h20 : [Constat à l'arrivée]='Erreur config réseau' problème d'authentification avec le serveur. La réinitialisation du MDP et la mise à jour des paramètres de connexion ont permis de résoudre le problème. !!!...
Tous les utilisateurs peuvent désormais accéder aux données sans aucun problème.


====================================================================================================
Texte desanonymisé
====================================================================================================
1. Résumé de l'incident :

A 12h50 le 11/12/2023 - Roger TAYLOR (stephane.rigaux@gmail.com) et Pierre ARDITI (responsable du site web https://www.google.com) de la cellule AGCP ont détecté que le boitier iqoya de ORANGE était en erreur.
Cela a mise dans le noir 350 utilisateurs sur le réseau en France. La valeur seuil était de 34.67°C en Occitanie

2. Chronologie des faits :
11/12/2023 - 21h50 : tests2 en fin de traitement chez BOUYGUES à Marseille
12/12/2023 - 11h59 : test3 qui va s'arréter à partir de 03h34 sur paris. test4 n'a plus d'avenir vers 23h34 depuis que C8 a déposé le bilan à Brest et ailleurs
=> CR FINAL Transmis ;code cloture =[ENT7 - IT - Probl. de mise en place]
- Com: 19/12/2023 11h45 : [Constat à l'arrivée]='Erreur de config détectée' décalage dans la séquence de démarrage des opérations. La reprogrammation des paramètres a permis de résoudre le problème. !!!...

Temps d'arrêt : 30 minutes. Tests de validation : OK. ENT7: 100% CPU, 8GB RAM, 250GB stockage dispo. Le système est maintenant opérationnel et stable. CR FINAL Transmis ;code cloture =[ENT8 - ADM - Probl. d'accès aux données] - Com: 05/11/2022 09h20 : [Constat à l'arrivée]='Erreur config réseau' problème d'authentification avec le serveur. La réinitialisation du MDP et la mise à jour des paramètres de connexion ont permis de résoudre le problème. !!!...
Tous les utilisateurs peuvent désormais accéder aux données sans aucun problème.
====================================================================================================


====================================================================================================
Tables de traduction
====================================================================================================
===== Détail de TRANSLATION ======
___ Anonymisation ___
Source = iqoya => destination = codecaudio
Source = iqoyas => destination = codecsaudio
Source = Roger => destination = trudi
Source = TAYLOR => destination = philippa
Source = AGCP => destination = DC
Source = Occitanie => destination = occitanie
Source = BOUYGUES => destination = AFNOR
Source = Marseille => destination = marbeuf
Source = C8 => destination = CNEWS
Source = Brest => destination = rebreuviette
Source = IT => destination = RRI
___ Desnonymisation ___
Source = codecaudio => destination = iqoya
Source = codecsaudio => destination = iqoyas
Source = trudi => destination = Roger
Source = philippa => destination = TAYLOR
Source = DC => destination = AGCP
Source = occitanie => destination = Occitanie
Source = AFNOR => destination = BOUYGUES
Source = marbeuf => destination = Marseille
Source = CNEWS => destination = C8
Source = rebreuviette => destination = Brest
Source = RRI => destination = IT
</details>
</pre>


6. Log de traitement

<pre>
====================================================================================================
Log de traitement dans ./log_anonymyzer_20240314_215517.log
====================================================================================================
</pre>





