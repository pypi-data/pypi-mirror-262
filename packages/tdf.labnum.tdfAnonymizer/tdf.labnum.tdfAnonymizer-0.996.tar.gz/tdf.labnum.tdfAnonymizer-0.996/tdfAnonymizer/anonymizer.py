from pydantic import BaseModel
from faker import Faker
import os
import csv
import pandas as pd
import random
import re
from datetime import datetime
import pkg_resources
import glob
import time
import logging
import unidecode

########################################## H E L P E R S ##########################################

faker = Faker(["fr_FR"])

########################################## V A R I A B L E S ########################################## 

# Ressources
dict_path = pkg_resources.resource_filename(__name__, 'resources')
word_path = pkg_resources.resource_filename(__name__, 'resources/words.csv')
name_path = pkg_resources.resource_filename(__name__, 'resources/Prenoms.csv')
unit_path = pkg_resources.resource_filename(__name__, 'resources/units.csv')
liste_pays_path = pkg_resources.resource_filename(__name__, 'resources/liste_pays.txt')
regions_france_metropolitaine_path = pkg_resources.resource_filename(__name__, 'resources/regions_france_metropolitaine.txt')
departements_france_path = pkg_resources.resource_filename(__name__, 'resources/departements_france.txt')
villes_path = pkg_resources.resource_filename(__name__, 'resources/villes.txt')
acronymes_path = pkg_resources.resource_filename(__name__, 'resources/acronymes.txt')
clients_path = pkg_resources.resource_filename(__name__, 'resources/clients.txt')
chaines_path = pkg_resources.resource_filename(__name__, 'resources/chaines.txt')

# Données externes
liste_pays=[]
regions_france_metropolitaine = []
departements_france = []
villes=[]
acronymes = []
clients=[]
chaines=[]
prenoms=[]
units=[]

# dictionaires
dictionaries={}

# formats de dates qui sont autorisés
formatDatesForCheck=["%d-%m-%Y","%d/%m/%Y","%y-%m-%Y","%Y/%m/%d"]

# cache nlp
nlp=None
doc=None

# translation des anonymisations / desanonymisation
translation = None
voyelles=["a","e","i","o","u","y"]

# Logger
logger = None

########################################## C L A S S E S ##########################################

class Translation:
    def __init__(self):
        self.anonymisations={}
        self.desanonymisations={}
        self.listExcludedWords=[]

        self.villes = []
        self.clients = []
        self.noms = []
        self.chaines = []
        self.acronymes = []

    def __str__(self) -> str:
        string=""
        string+="===== Détail de TRANSLATION ======\n"
        string+="___ Anonymisation ___\n"
        for key in self.anonymisations.keys():
            string+=f"Source = {key} => destination = {self.anonymisations[key]}\n"
        string+="___ Desnonymisation ___\n"
        for key in self.desanonymisations.keys():
            string+=f"Source = {key} => destination = {self.desanonymisations[key]}\n"
        return string

    def setVilles(self,villes:list):
        if villes != None:
            self.villes = villes
    
    def setClients(self,clients:list):
        if clients != None:
            self.clients = clients

    def setPrenoms(self,prenoms:list):
        if prenoms != None:
            self.prenoms = prenoms

    def setChaines(self,chaines:list):
        if chaines != None:
            self.chaines = chaines

    def setAcronymes(self,acronymes:list):
        if acronymes != None:
            self.acronymes = acronymes

    # on alimente les 2 hashmaps anonymisations et desanonymisations avec les valeurs source <-> cible de remplacements
    # /!\ ATTENTION /!\ cette méthode remplace les valeurs des 2 hashmaps
    def setRemplacements(self,remplacements:pd.DataFrame):
        df=remplacements

        # on enleve les doublons dans la colonne remplacement
        df.drop_duplicates(["remplacement"], keep='first', inplace=True)

        # on enleve les doublons dans la colonne texte
        df.drop_duplicates(["texte"], keep='first', inplace=True)

        ### hashmap anonymisations ###
        self.anonymisations = df.groupby('texte')['remplacement'].agg(list).to_dict()
        for key in self.anonymisations.keys():
            self.anonymisations[key]=self.anonymisations[key][0]

        ### hashmap desanonymisations ###
        self.desanonymisations = df.groupby('remplacement')['texte'].agg(list).to_dict()
        for key in self.desanonymisations.keys():
            self.desanonymisations[key]=self.desanonymisations[key][0]

    def actionAnonymisationVilles(self,value,action="add"):
        return self.actionAnonymisation(self.villes,value,action)
    
    def actionAnonymisationClients(self,value,action="add"):
        return self.actionAnonymisation(self.clients,value,action)
    
    def actionAnonymisationPrenoms(self,value,action="add"):
        return self.actionAnonymisation(self.prenoms,value,action)
    
    def actionAnonymisationChaines(self,value,action="add"):
        return self.actionAnonymisation(self.chaines,value,action)
   
    def actionAnonymisationAcronymes(self,value,action="add"):
        return self.actionAnonymisation(self.acronymes,value,action)
    
    def actionAnonymisation(self,liste:list,value,action):
        anonymisation = None

        if action == "add":

            log(f"Recupération de la valeur anonymisée pour {value}",loglevel=logging.DEBUG)

            if liste != None and len(liste) > 0 :
                if value in self.anonymisations.keys():
                    anonymisation = self.anonymisations[value] 
                else:
                    foundValue = False
                    # on cherche tant que la valeur de remplacement est identique à la valeur initiale
                    while not foundValue:
                        indexChoix=random.randint(0,len(liste)-1)
                        if liste[indexChoix] != value and not self.isInListExcludedWords(liste[indexChoix]):
                            foundValue = True

                    # on enlève la valeur de la liste des valeurs disponibles 
                    anonymisation=liste.pop(indexChoix)
            else:
                # si pas de liste, on renvoie la valeur à anonymiser
                anonymisation = value

            # on ajoute la valeur à l'anonymisation et desanonymisation
            self.anonymisations[value]=anonymisation
            self.desanonymisations[anonymisation]=value
            
            return anonymisation
            
        if action == "remove":

            log(f"Suppression de la valeur anonymisée pour {value}",loglevel=logging.DEBUG)

            if liste != None and len(liste) > 0 :

                if value in self.anonymisations.keys():
                    anonymisation = self.anonymisations[value] 
                # on enleve des valeurs anonymisées
                self.anonymisations.pop(value)
                # on enleve des valeurs desanonymisées
                self.desanonymisations.pop(anonymisation)
                # on rajoute à la liste pour disponibilité
                liste.append(value)

       
        
    def getDesanonymisation(self,value:str):
        if value == None:
            return None
        
        desanonymisation = None
        # https://www.tutorialspoint.com/python-program-to-compare-two-strings-by-ignoring-case
        for key in self.desanonymisations.keys():
            if value.lower() == key.lower():
                desanonymisation = self.desanonymisations[key]
        return desanonymisation

    # recherche une valeur dans le cache de translation pour éviter de rechercher à nouveau
    def getAnonymisation(self,value:str):
        if value == None:
            return None
        
        anonymisation = None
        # https://www.tutorialspoint.com/python-program-to-compare-two-strings-by-ignoring-case
        for key in self.anonymisations.keys():
            if value.lower() == key.lower():
                anonymisation = self.anonymisations[key]
        return anonymisation

    def isInListExcludedWords(self,word):
        return word in self.listExcludedWords

    def addExcludedWord(self,word):
        if not word in self.listExcludedWords:
            self.listExcludedWords.append(word)

    def displayListExcludedWords(self):
        log("",loglevel=logging.DEBUG)
        log(f"======== Liste mots exclus ========",loglevel=logging.DEBUG)
        for item in self.listExcludedWords:
            log(item,loglevel=logging.DEBUG)
        log("",loglevel=logging.DEBUG)
        




class Configuration:
    def __init__(self,acronyme=False, ville=False,chaine=False,nom=False,date=False,heure=False,nombre=False,pays=False,entreprise=False,lien=False,flagAmeliorationBasiqueTexte=False):
        self.ville = ville
        self.chaine = chaine
        self.nom = nom
        self.date = date
        self.heure = heure
        self.nombre = nombre
        self.pays = pays
        self.entreprise = entreprise
        self.lien = lien
        self.acronyme = acronyme
        self.flagAmeliorationBasiqueTexte = flagAmeliorationBasiqueTexte
        

    ville: bool
    chaine: bool
    nom: bool
    date: bool
    heure: bool
    nombre: bool
    pays: bool
    entreprise: bool
    lien: bool
    flagAmeliorationBasiqueTexte: bool


class textAnonyms(BaseModel):
    originalText: str
    textFormat: str

########################################## F O N C T I O N S ###########################################

def log(text:str,loglevel:int = logging.info):
   
    if logger != None:
        if loglevel == logging.DEBUG:
            print(text)
            logger.debug(text)
        if loglevel == logging.INFO:
            logger.info(text)



def setupLogger(logfilename:str,loggername:str,loglevel:int):

    if logfilename == None or logfilename.strip() == "" or loggername == None or loggername.strip() == "":
        return

    try:
        log_dir=os.path.dirname(logfilename)  
        if not os.path.exists(log_dir):
            os.makedirs(log_dir) 

        # create logger
        global logger
        logger = logging.getLogger(loggername)
        logger.setLevel(loglevel)

        # create console handler and set level to debug
        ch = logging.FileHandler(logfilename,mode="w",encoding='utf-8')
        ch.setLevel(loglevel)

        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(ch)

        # Ajout d'une entete de log
        log(f"------------ Log avec le niveau {logging.getLevelName(loglevel)} ------------",loglevel=loglevel)


    except:
        # pas de logger disponible
        pass
    

# Affiche le temps d'éxécution entre 2 temps
def det(label:str,time1:time,time2:time):
    if label == None or time1 == None or time2 == None:
        return
    
    log("",logging.DEBUG)
    log("---------------------------------------------------",logging.DEBUG)
    log(f"Execution de {label} : { time2-time1:0.4f} secondes",logging.DEBUG)
    log("---------------------------------------------------",logging.DEBUG)
    log("",logging.DEBUG)
    


# trouve la première ligne 
def findValueInCsv(df,filterColumnName,filterColumnValue,returnColumnName):
    returnValue=None
    if isinstance(df, pd.DataFrame):
        if filterColumnName in df.columns:
            if returnColumnName in df.columns:
                try:
                    rows=df.loc[df[filterColumnName] == filterColumnValue]
                    if len(rows) > 0:
                        returnValue=rows.iloc[0][returnColumnName]
                except:
                    pass
    return returnValue

# retourne une liste de string, d'objet
def getDataExternes(name,type="text",csv_options={ "delimiter" : ";" }):
    lines=[]
    extension=None
    encoding=None
    match type:
      case "text":
        extension="txt"
        encoding="utf-8"
      case "csv":
        extension="csv"
        encoding="iso-8859-1"
      case _:
        extension=None
    
    if extension == None or encoding == None:
        return lines
    
    # en fonction du type, on charge les données dans une liste, en enlevant les doublons pour les données "texte"
    path=pkg_resources.resource_filename(__name__, f"resources/{name}.{extension}")
    if os.path.isfile(path):
        with open(path,"r",newline="\n") as file:
            match type:
                case "text":
                    lines=[line.rstrip() for line in file]
                    # suppression des doublons
                    lines=list(dict.fromkeys(lines))
                case "csv":
                    lines = pd.read_csv(file,delimiter=csv_options["delimiter"])
                case _:
                    lines = []
    else:
        log(f"Problème de lecture du fichier {path}",loglevel=logging.ERROR)
    return lines

# Recharge les données externes
def loadAllDataExternes():
    global liste_pays,units,clients,regions_france_metropolitaine,departements_france,villes,acronymes,chaines,prenoms,remplacements
    liste_pays=getDataExternes("pays")
    regions_france_metropolitaine = getDataExternes("regions_france_metropolitaine")
    departements_france = getDataExternes("departements_france")
    villes=getDataExternes("villes")
    acronymes = getDataExternes("acronymes")
    clients=getDataExternes("clients")
    chaines=getDataExternes("chaines")
    prenoms=getDataExternes("prenoms")
    units=getDataExternes("units")
    remplacements=getDataExternes("remplacements",type="csv")


# Si besoin de charger tous les dictionnaires en une seule fois
def loadDictionnaries():
    # path to search all txt files 
    path = dict_path+f"/dictionnaire_*.txt"
    for fullname in glob.glob(path):
        # nom court du fichier sans extension
        filename=os.path.basename(fullname).split('.')[0]
        # extraction de la lettre dans le nom du fichier suivant le pattern dictionnaire_([A-Z]).txt
        result = re.search(r"^dictionnaire_(.+)$", filename)
        if result != None and result.groups() and len(result.groups()):
            lettre=result.groups()[0]
            # chargement du fichier 
            with open(fullname, 'r', encoding='utf-8') as file:
                lines=[line.rstrip() for line in file]
                dictionaries[lettre]=lines
        else:
            log(f"Impossible de trouver la première lettre dans le nom du fichier {fullname}",loglevel=logging.ERROR)

def getDictionnary(premiere_lettre):
    # dans le cache des dictionnaires
    if premiere_lettre == None or dictionaries == None or not isinstance(dictionaries,dict):
        return
    
    dictionary=None
    if premiere_lettre not in dictionaries.keys():
        # création du cache
        subdict = dict_path+f"/dictionnaire_{premiere_lettre}.txt"
        if (os.path.exists(subdict)):
            with open(subdict, 'r', encoding='utf-8') as file:
                lines=[line.rstrip() for line in file]
                dictionaries[premiere_lettre]=lines

    if premiere_lettre in dictionaries.keys():
        dictionary = dictionaries[premiere_lettre]
    
    return dictionary

# Découpage d'un paragraphe en mot. Les espaces sont gardés dans le résultat
def split(paragraphe,config : Configuration = None):

    phrase = paragraphe

    # amélioration basique du texte
    if config != None and config.flagAmeliorationBasiqueTexte:
        helpers={
            "NEWLINE" : ("asdrYuikBFGTnjkiuZER","\n"),
            "CARRIAGE_RETURN" : ("RTbhYUJvDFRxSZEL","\r")
        }

        # On remplace les \r et \n par un placeholder pour remettre le code en fin de split
        phrase = phrase.replace(helpers["NEWLINE"][1],helpers["NEWLINE"][0])
        phrase = phrase.replace(helpers["CARRIAGE_RETURN"][1],helpers["CARRIAGE_RETURN"][0])

        # on met un blanc devant et après la phrase pour que la regex suivante avec [^\d] soit vrai pour le groupe 1
        phrase=" "+phrase+" "

        # enlève les blancs d'une chaine incluant une notion d'heure => 00:00 à 23:59
        # on crée une chaine qui sera remplacer par le format HH:mm
        regex = r"([^\d])([0-1][0-9]|2[0-4])\s*[:|h|H]\s*([0-5][0-9])([^\d])"
        subst = r"\1 __HEURE__\2|\3__HEURE__ \4"

        result = re.sub(regex, subst, phrase, 0)
        if result:
            phrase=result

        # remplace le texte ressemblance à Azerty/Bzerty par Azerty / Bzerty
        phrase = re.sub(r'([A-Z][a-z]*)\/([A-Z][a-z]*)', r'\1 / \2', phrase)

        # ajoute un espace après le point si suivi d'un mot commencant par une majuscule
        phrase = re.sub(r'\.([A-Z][a-z]*)',r'. \1',phrase)

        # découpe sur les caractères de phrase sauf le .
        #mots = re.split(r'(\s+|[;,?!:\[\]])',phrase)
        mots = re.split('(\s)',phrase)

        # remplacement de __HEURE__\1|\2__HEURE__ par \1h\2
        regex2 = r"(\_\_HEURE\_\_)([0-1][0-9]|2[0-4])(\|)([0-5][0-9])(\_\_HEURE\_\_)"
        subst2 = r"\2h\4"
        for index,mot in enumerate(mots):
            result2 = re.sub(regex2, subst2, mot, 0)
            if result2:
                mots[index]=result2
    
        # remplacement de __NEWLINE__ par \n
        # remplacement de __CARRIAGE_RETURN__ par \n
        for index,mot in enumerate(mots):
            mot = mot.replace(helpers["NEWLINE"][0],helpers["NEWLINE"][1])
            mot = mot.replace(helpers["CARRIAGE_RETURN"][0],helpers["CARRIAGE_RETURN"][1])  
            mots[index] = mot
    
        completeText="".join(mots)
        # on lit ligne par ligne et on ébarde les espaces au début à la fin, on enlève les espaces multiples
        lines=completeText.splitlines()
        nbLines=len(lines)
        motsTarget=[]
        delimiter=" "
        for index,line in enumerate(lines):
            line=line.strip()
            # suppression des multiples espaces consécutifs
            while "  " in line:
                line=line.replace("  "," ")

            #Gestion des points ( dans nombre ou séparateur de phrase, ou notation pour réduire un mot trop long (probl. pour problème))
            words=re.split('(\s)',line)
            nbWords=len(words)

            for index2,word in enumerate(words):
                # on regarde si le mot contient un point ou plusieurs
                nbDots=word.count(".")
                # flag isFloat
                isFloat = False

                # si un seul point , on regarde si c'est potentiellement un nombre à partir d'un test de conversion
                if nbDots == 1:
                    try:
                        input_1 = float(word)
                        isFloat = True
                        motsTarget.append(word)
                    except:
                        # peut-etre une mesure
                        # on extrait la partie numérique qui se suit. Exemple 35.7°C => 35.7 
                        regex3 = r"^(-?[\d]{2,}\.{0,1}[\d]*)([^\d]*)"
                        matches=re.search(regex3,word)
                        if matches and len(matches.groups())==2:
                            try:
                                groupe1=matches.group(1)
                                input_2 = float(groupe1)  
                                motsTarget.append(word)                         
                                isFloat = True

                                # code difficile pour tester les unités comme les °
                                # mise en commentaire pour le moment
                                """          
                                # est-ce que le groupe2 est une unité de mesure ?
                                groupe2=matches.group(2)
                                if is_unit(groupe2):
                                    print("|unit =>"+word+"|")
                                    print(word + " is a unit")
                                    isFloat = True
                                    motsTarget.append(groupe1)
                                    motsTarget.append(groupe1)
                                """
                            except:
                                isFloat = False
                        else:
                            isFloat = False

                if isFloat == False:  
                    if  nbDots >= 1:
                        tokens=word.split(".")
                        nbTokens=len(tokens)
                        for indexToken,token in enumerate(tokens):
                            motsTarget.append(token)
                            if indexToken < nbTokens - 1:
                                # on met un espace après le point
                                motsTarget.append(" . ")
                    else:
                        motsTarget.append(word)

            if index < nbLines - 1:
                motsTarget.append("\n")

        # on merge les . consecutifs : ". ", "."
        phraseComplete="".join(motsTarget)
        
        # on réorganise les espaces et les .
        sep="  "
        while sep in phraseComplete:
            phraseComplete=phraseComplete.replace(sep," ")
        sep=". . "
        while sep in phraseComplete:
            phraseComplete=phraseComplete.replace(sep,".. ")
        sep=" ."
        while sep in phraseComplete:
            phraseComplete=phraseComplete.replace(sep,".")
        
        phrase = phraseComplete
    # fin amélioration texte

    # on recrée le tableau de mots à partir de phrase
    mots=re.split('(\s)',phrase)
    return mots


def fake_num_string(original):
    fakedigit=[0,1,2,3,4,5,6,7,8,9]
    fakeData = list(original)
    for i in range(len(fakeData)):
        if(fakeData[i].isnumeric()):
            digit = random.choice(fakedigit)
            fakeData[i] = str(digit)
    fakeData = "".join(fakeData)
    return fakeData

def cherche_chaine(chaine):
    chaine = chaine.upper()
    if chaines == None or not isinstance(chaines,list):
        return False
    for item in chaines:
        if  item in chaine  :
            return True
    return False


def cherche_ville(ville):
    ville = ville.lower()

    # implementer unidecode.unidecode pour enlever les accents
    # https://www.geeksforgeeks.org/how-to-remove-string-accents-using-python-3/
    ville = unidecode.unidecode(ville)

    return ville in villes


# a modifier
def is_unit(word):
    if word!= None and units != None and any(word == x for x in units) :
        return True
    else: 
        return False 

def is_in_dico(mot):
    
    if mot == None :
        return False    
    premiere_lettre = mot[0].upper()   
    dictionary=getDictionnary(premiere_lettre)
    if dictionary and mot.lower() in dictionary:
        return True
    else:
        return False


def check_same(mot):
    anonymisedData = pd.read_csv(word_path, encoding="iso-8859-1", dtype={"original": str, "anonymous": str, "index":int})
    for index, row in anonymisedData.iterrows():
        if (row["anonymous"] == mot):
            return False
    return True

def anonymiser_mot(text: textAnonyms,config : Configuration ):
    fakehour=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
    try:
        anonymisedData = pd.read_csv(word_path, encoding="iso-8859-1", dtype={"original": str, "anonymous": str, "index":int})
        original = text.originalText
        # Initialisation
        fakeData=original
        if (text.textFormat == "CITY" and config.ville == True):
            fakeData=None
            while fakeData == None:
                fakeData=translation.actionAnonymisationVilles(original)
                # on verifie que la fakedata commence par une voyelle si la donnée initiale commence par une voyelle
                # et vice-versa, grace à l'opérateur ^
                # https://fr.wikibooks.org/wiki/Programmation_Python/Op%C3%A9rateurs
                if (original.lower()[0] in voyelles) ^ (fakeData.lower()[0] in voyelles) == 1:
                    fakeData = None
                    translation.actionAnonymisationVilles(original,action="remove")
        elif (text.textFormat == "CHAINE" and config.chaine == True):
            fakeData=translation.actionAnonymisationChaines(original)
        elif(text.textFormat == "PERSON" and config.nom == True):
            fakeData=translation.actionAnonymisationPrenoms(original)
        elif(text.textFormat == "DATE" and config.date == True):
            fakeData = faker.date()
            fakeData = datetime.strptime(fakeData, "%Y-%m-%d")
            fakeData = fakeData.strftime("%d/%m/%Y")
        elif(text.textFormat == "HOUR" and config.heure == True):
            hour = random.choice(fakehour)
            fakehour.remove(hour)
            fakeData = (str(hour) if hour>9 else "0"+str(hour))+"h00"
        elif(text.textFormat == "NUMBER" and config.nombre == True):
            unique = False
            while unique == False:
                fakeData = fake_num_string(original)
                unique = check_same(fakeData)
            while any(anonymisedData["anonymous"] == fakeData) and any(anonymisedData["original"] == fakeData):
                fakeData = fake_num_string(original)
        elif(text.textFormat == "COUNTRY" and config.pays == True):
            fakeData=translation.actionAnonymisationPays(original)
            #fakeData = fakepays[0]+str(nbfakepays)
            #nbfakepays +=1
        elif(text.textFormat == "ORGANIZATION" and config.entreprise == True):
            fakeData=translation.actionAnonymisationClients(original)
        elif(text.textFormat == "ACRONYM" and config.acronyme == True):
            fakeData=translation.actionAnonymisationAcronymes(original)
        elif(text.textFormat == "TEXT"):
            # On applique le remplacement des mots issus du fichier remplacements.csv
            # A faire
            # if  original.lower()      
            # A remplacer par la version translation
            fakeData = findValueInCsv(remplacements,"texte",original.lower(),"remplacement")
            if fakeData == None:
                fakeData = original
        else: # on ne fait rien de spécial
            fakeData = original
    
        return fakeData
    except Exception as e:
        log("fonction anonymiser_mot " + str(e),loglevel=logging.ERROR)
        return text.originalText

def anonymiser_email(paragraphe):
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    fakemail = ["fakemail"]
    nbfakemail = 1
    adresses_email = re.findall(pattern, paragraphe)
    for adresse in adresses_email:
        fakeData = (fakemail[0]+str(nbfakemail))
        paragraphe = paragraphe.replace(adresse,fakeData)
        nbfakemail +=1
        with open(word_path, mode='a', newline='', encoding="iso-8859-1") as fichier_csv:
            writer = csv.writer(fichier_csv)
            writer.writerow([adresse,fakeData])
    return paragraphe

def is_a_prenom(word):
    # on a chargé le fichier des prénoms à l'initialisation
    if word!= None and prenoms != None and any(word.lower() == x.lower() for x in prenoms) :
        return True
    else: 
        return False 
    
def is_a_date(word):
    if word == None:
        return False
    flag=False
    for formatDate in formatDatesForCheck:
        try:
            flag = bool(datetime.strptime(word, formatDate))
            break
        except ValueError:
            flag = False
    
    return flag


def setupNLP():
    global nlp
    if nlp == None:

        time1=time.perf_counter()

        import spacy
        nlp=spacy.load("fr_core_news_sm")

        # chargement des entités
        ruler = nlp.add_pipe("entity_ruler")        

        log("Chargement des clients comme entité",loglevel=logging.DEBUG)
        for client in clients:
            ruler.add_patterns([{"label": "ORGANIZATION", "pattern": client}])

        log("Chargement des chaines comme entité",loglevel=logging.DEBUG)
        for chaine in chaines:
            ruler.add_patterns([{"label": "CHAINE", "pattern": chaine}])

        log("Chargement des acronymes comme entité",loglevel=logging.DEBUG)
        for acronyme in acronymes:
            ruler.add_patterns([{"label": "ACRONYM", "pattern": acronyme}])

        time2=time.perf_counter()
        det("Setup NLP + Chargement des entités",time1,time2)



# fonction pour lever une ambiguité
# retourne un label 
def GetLabelToResolveAmbiguity(text,word):
    global nlp,doc
    setupNLP()
    label=None   
    if doc == None:
        doc=nlp(text)
    for ent in doc.ents:
        if word in ent.text:
            label=ent.label_
            break
    return label

    
def anonymiser_lien(paragraphe):
    pattern = r'https?://\S+'
    fakelink = ["fakelink"]
    nbfakelink = 1
    liens = re.findall(pattern, paragraphe)
    for lien in liens:
        fakeData = (fakelink[0]+str(nbfakelink))
        paragraphe = paragraphe.replace(lien,fakeData)
        nbfakelink +=1
        with open(word_path, mode='a', newline='') as fichier_csv:
            writer = csv.writer(fichier_csv)
            writer.writerow([lien,fakeData])
    return paragraphe

def anonymiser_paragraphe(paragraphe,config:Configuration):

    log("="*100,loglevel=logging.DEBUG)
    log("Paragraphe initial",loglevel=logging.DEBUG)
    log("="*100,loglevel=logging.DEBUG)
    log("\n"+paragraphe,loglevel=logging.DEBUG)

    time1=time.perf_counter()

    phrase = anonymiser_email(paragraphe)
    if (config.lien == True):
        phrase = anonymiser_lien(phrase)

    tokens = split(phrase,config=config)
    listmot = []
    entites_nommees = []
    index = 0
    pos_word = 0

    
    # compteur flags , contiendra la somme logigue 1|2|4|8|16|32|64|128|256
    # flagInDico=1
    # flagChaine=2
    # flagClient=4
    # flagDate=8
    # flagHour=16
    # flagUnit=32
    # flagCountry=64
    # flagCity=128
    # flagPerson=256
    # flagText=512
    compteurFlag=0
    
    arrayAcceptableFlags=[1,2,4,8,16,32,64,128,256,512,1024,2048,5192]

    last_was_dot = True
    for word in tokens:
        compteurFlag=0
        index=index+1
        listmot.append(word)
        if ((word != " " and word != "" and word != "\n" and word != "\r")):
            flagIsInDico=is_in_dico(word)
            if flagIsInDico:
               compteurFlag+=1
            if (cherche_chaine(word)):
                compteurFlag+=2
            if word in clients or word.lower() in clients:
                compteurFlag+=4
            if is_a_date(word):
                compteurFlag+=8
            if (re.match("^([0-1][0-9]|2[0-3])h([0-5][0-9])$",word)):
                compteurFlag+=16
            #if (is_unit(word)):
            #    compteurFlag+=32
            if  word.lower() in liste_pays:
                compteurFlag+=64
            if ((cherche_ville(word.lower()) or word in departements_france or word in regions_france_metropolitaine)):
                compteurFlag+=128
            if re.match("[A-Z].*",word) and is_a_prenom(word) == True:
                compteurFlag+=256
            if word.upper() in acronymes:
                compteurFlag+=512
            if compteurFlag == 0 and not flagIsInDico:
                compteurFlag+=1024

            # check des flags
            if not compteurFlag in arrayAcceptableFlags:

                time10=time.perf_counter()

                label=GetLabelToResolveAmbiguity(paragraphe,word)
                if label == "MISC":
                    # on garde le mot car pas d'entité MISC = divers
                    # on indique au service de translation que le mot ne peut pas être utilisé pour anonymiser
                    translation.addExcludedWord(word)
                elif label == "ACRONYM":
                    entites_nommees.append(("ACRONYM", word,pos_word))
                elif label == "ORG":
                    entites_nommees.append(("ORGANIZATION", word,pos_word))
                elif label == "LOC":
                    entites_nommees.append(("CITY", word,pos_word))
                else:
                    # on garde le mot
                    translation.addExcludedWord(word)

                time20=time.perf_counter()
                det("Resolve ambiguity for " + word, time10,time20)

            else:
                # on append les entitées nommées pour les données non ambigues
                if compteurFlag == 1:
                    entites_nommees.append(("",word,pos_word))
                elif compteurFlag == 2:    
                    entites_nommees.append(("CHAINE",word,pos_word))
                elif compteurFlag == 4:    
                    entites_nommees.append(("ORGANIZATION",word,pos_word))
                elif compteurFlag == 8:    
                    entites_nommees.append(("DATE", word,pos_word))
                elif compteurFlag == 16:    
                    entites_nommees.append(("HOUR", word, pos_word))
                elif compteurFlag == 32:    
                    entites_nommees.append(("UNIT", word, pos_word))
                elif compteurFlag == 64:    
                    entites_nommees.append(("COUNTRY", word,pos_word))
                elif compteurFlag == 128:    
                    entites_nommees.append(("CITY", word,pos_word))
                elif compteurFlag == 256:    
                    entites_nommees.append(("PERSON",word,pos_word))
                elif compteurFlag == 512:    
                    entites_nommees.append(("ACRONYM",word,pos_word))
                elif compteurFlag == 1024:    
                    entites_nommees.append(("TEXT",word,pos_word))
                else:
                    pass
                

        pos_word += 1

    nbfakeorganisation = 1
    nbfakechaine = 1
    nbfakecity = 1
    nbfakepays = 1
    for entity_type, entity_value,position in entites_nommees:
        text = textAnonyms(originalText=entity_value, textFormat=entity_type)
        found = False
        mot=translation.getAnonymisation(entity_value)
        if mot != None:
            listmot[position]=mot
            found=True
        if found == False:
            faketext = anonymiser_mot(text,config)
            listmot[position]=faketext
        
        # print(entity_type + "/" + str(position) + "/" + entity_value + " => " + faketext)
            
    paragraphe = ("".join(listmot))


    time2=time.perf_counter()
    det("Anonymisation paragraphe",time1,time2)

    log("="*100,loglevel=logging.DEBUG)
    log("Paragraphe désanonymisé",loglevel=logging.DEBUG)
    log("="*100,loglevel=logging.DEBUG)
    log("\n"+paragraphe,loglevel=logging.DEBUG)

    return paragraphe

def desanonymiser_paragraphe(anonymous_paragraphe,config:Configuration=None):

    time1=time.perf_counter()

    listmot = split(anonymous_paragraphe,config=config)
    
    for index,mot in enumerate(listmot):
        nouveauMot=translation.getDesanonymisation(mot)
        if nouveauMot != None :
            listmot[index]=nouveauMot
    
    anonymous_paragraphe = "".join(listmot)

    while "  " in anonymous_paragraphe:
        anonymous_paragraphe = anonymous_paragraphe.replace("  "," ")


    time2=time.perf_counter()
    det("Desanonymisation paragraphe",time1,time2)

    return anonymous_paragraphe

def getTranslation():
    global translation
    return translation

def initialiser():

    # chargement des données externes
    loadAllDataExternes()

    # Structure de translation
    global translation
    translation = Translation()
    translation.setClients(clients)
    translation.setPrenoms(prenoms)
    translation.setVilles(villes)
    translation.setChaines(chaines)
    translation.setAcronymes(acronymes)
    translation.setRemplacements(remplacements)



    csv_file_path = word_path
    if os.path.exists(csv_file_path):
        os.remove(csv_file_path)

    empty_dataframe = pd.DataFrame(columns=["original", "anonymous"])
    empty_dataframe.to_csv(csv_file_path, index=False)






