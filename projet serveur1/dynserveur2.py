from serveur import get_template, render, OK, Redirect, pageDynamique, lancerServeur
from hashlib import *
from datetime import datetime
from socket import *
from random import *
import webbrowser
import urllib
import smtplib
import secrets
import json
import re

def start(url,vars):
    return Redirect("/accueil.html")

#salt = secrets.token_hex(24).encode()
salt =  b'28e98973d80a54d87f8a42d394bab50ac2585d1be4dd864b'

def init_black_list():
	black_list=[]
	with open('black_list.json', 'w') as b:
		json.dump(black_list,b)
		b.close()

try:
	with open('black_list.json', 'r') as b:
			black_list = json.load(b)
except Exception as e:
	print(f"Erreur d'ouverture du fichier black_list.json : {e}")
	init_black_list()
	with open('black_list.json', 'r') as b:
			black_list = json.load(b)
                        
def init_mots_interdits():
	mots_interdits=[]
	with open('mots_interdits.json', 'w') as m:
		json.dump(mots_interdits,m)
		m.close()

try:
	with open('mots_interdits.json', 'r') as m:
			mots_interdits = json.load(m)
except Exception as e:
	print(f"Erreur d'ouverture du fichier mots_interdits.json : {e}")
	init_mots_interdits()
	with open('mots_interdits.json', 'r') as m:
			mots_interdits = json.load(m)

def init_file():
	hmdp_ref_from_file={}
	with open('file.json', 'w') as f:
		json.dump(hmdp_ref_from_file,f)
		f.close()

              
try:
	with open('file.json', 'r') as f:
			hmdp_ref_from_file = json.load(f)
except Exception as e:
	print(f"Erreur d'ouverture du fichier file.json : {e}")
	init_file()
	with open('file.json', 'r') as f:
			hmdp_ref_from_file = json.load(f)

def init_conv():
	conversation=[]
	with open('conv.json', 'w') as c:
		json.dump(conversation,c)
		c.close()

try:
	with open('conv.json', 'r') as c:
			conversation = json.load(c)
except Exception as e:
	print(f"Erreur d'ouverture du fichier conv.json : {e}")
	init_conv()
	with open('conv.json', 'r') as c:
			conversation = json.load(c)

def init_code():
	code={}
	with open('code.json', 'w') as c:
		json.dump(code,c)
		c.close()

try:
	with open('code.json', 'r') as c:
			code = json.load(c)
except Exception as e:
	print(f"Erreur d'ouverture du fichier code.json : {e}")
	init_code()
	with open('code.json', 'r') as c:
			code = json.load(c)

def init_devoirs():
	devoirs_liste=[]
	with open('devoirs.json', 'w') as d:
		json.dump(devoirs_liste, d)
		d.close()

try:
	with open('devoirs.json', 'r') as d:
			devoirs_liste = json.load(d)
except Exception as e:
	print(f"Erreur d'ouverture du fichier devoirs.json : {e}")
	init_devoirs()
	with open('devoirs.json', 'r') as d:
			devoirs_liste = json.load(d)

def init_pseudo():
	pseu={}
	with open('pseudo.json', 'w') as f:
		json.dump(pseu,f)
		f.close()

try:
	with open('pseudo.json', 'r') as f:
			pseu = json.load(f)
except Exception as e:
	print(f"Erreur d'ouverture du fichier pseudo.json : {e}")
	init_pseudo()
	with open('pseudo.json', 'r') as f:
			pseu = json.load(f)

def inscription(url, vars):
    pseudo=vars['pseudo']
    id_ref = vars["email_inscr"]
    if (re.search("@sacrecoeuraix.com$", id_ref) or re.search("@gmail.com$", id_ref) or re.search("@outlook.com$", id_ref) or re.search("@outlook.fr$", id_ref) or re.search("@hotmail.com$", id_ref)):
        mdp_ref = vars["psw_inscr"]
        mdp = mdp_ref
        mdp_ref = mdp_ref.encode()
        hmdp_ref = sha512(salt + mdp_ref).hexdigest()
        ver_mdp = vars["ver_psw_inscr"]
        if mdp == ver_mdp :
            with open('file.json', 'w') as f:
                hmdp_ref_from_file[id_ref] = [hmdp_ref,pseudo]
                json.dump(hmdp_ref_from_file, f, indent=4)
            return Redirect("/connexion.html#inscription_valide")
        else : 
            return Redirect("/inscription.html#psw_diff")
    else:
	    return Redirect("/inscription.html#email_invalide")

def connexion(url, vars):
    with open('file.json', 'r') as f:
        hmdp_ref_from_file = json.load(f)
    id_connex = vars["email_connex"]
    mdp_connex = vars["psw_connex"]
    mdp_connex = mdp_connex.encode()
    hmdp_connex = sha512(salt + mdp_connex).hexdigest()
    if (re.search("@sacrecoeuraix.com$", id_connex) or re.search("@gmail.com$", id_connex) or re.search("@outlook.com$", id_connex) or re.search("@outlook.fr$", id_connex) or re.search("@hotmail.com$", id_connex)):
        if id_connex in hmdp_ref_from_file :
            if hmdp_connex == hmdp_ref_from_file[id_connex][0]:
                
                id=gethostbyname(gethostname())
                pseudo=hmdp_ref_from_file[id_connex][1]
                if id in pseu:
                      del pseu[id]
                pseu[id] = [id_connex,pseudo]
                with open('pseudo.json', 'w') as p:
                    
                    json.dump(pseu, p, indent=4)
                return Redirect("/accueil.html")
            else :
                return Redirect("/connexion.html#mdp_invalide")
        else:
            return Redirect("/inscription.html#email_introuvable")
    else :
        return Redirect("/connexion.html#email_invalide")

def page_conversation(url, vars):
	""" Retourner la page de la conversation """
	
	template = get_template('chat.html')
	
	vars['message']=conversation

	html = render(template, vars)
	
	return OK(html)

pageDynamique('/chat.html', page_conversation)

def verif(chaine2caractere):
    tab=json.load(open("mots_interdits.json", "r"))
    for i in tab:
        if i in chaine2caractere:
            chaine2caractere = chaine2caractere.replace(i,len(i)*"*")
    return chaine2caractere
# La page dynamique qui ajoute un message
def nouveau_message(url, vars):
    id=gethostbyname(gethostname())
    with open('pseudo.json', 'r') as p:
          pseu=json.load(p)
    if id in pseu:
        pseudo='[' + str(datetime.now().strftime("%d/%m/%Y %H:%M")) + '] '+pseu[id][1] + ' :'
    else:
        pseudo='[' + str(datetime.now().strftime("%d/%m/%Y %H:%M")) + '] '+"Anonyme"+' :'
    message = verif(vars['msg'])
    
    conversation.insert(len(conversation),[message,pseudo,id])
    with open('conv.json', 'w') as c:
           json.dump(conversation, c, indent=4)

    return Redirect('/chat.html')

def page_devoirs(url, vars):
	""" Retourner la page de la conversation """
	
	template = get_template('devoirs.html')
	
	vars['devoirs']=devoirs_liste
    
	html = render(template, vars)
	
	return OK(html)

pageDynamique('/devoirs.html', page_devoirs)

def nouveau_devoirs(url, vars):
    id=gethostbyname(gethostname())
    with open('pseudo.json', 'r') as p:
          pseu=json.load(p)
    if id in pseu:
        pseudo='[' + str(datetime.now().strftime("%d/%m/%Y %H:%M")) + '] '+pseu[id][1] +' :'
    else:
        pseudo='[' + str(datetime.now().strftime("%d/%m/%Y %H:%M")) + '] '+"Anonyme :"
    devoirs = verif(vars['demande'])
    
    devoirs_liste.insert(len(devoirs_liste),[devoirs,pseudo,id])
    with open('devoirs.json', 'w') as d:
           json.dump(devoirs_liste, d, indent=4)

    return Redirect('/devoirs.html')

def send_email(url, vars):
    email = vars["email_recup"]
    with open('file.json', 'r') as f:
           hmdp_ref_from_file=json.load(f)
    if email in hmdp_ref_from_file:
        with open('code.json', 'r') as c:
           code=json.load(c)
        from_email = 'sacreblog39@gmail.com' # Remplacez cette valeur par votre adresse e-mail
        password = 'knkynmnmtzekfupd' # Remplacez cette valeur par votre mot de passe
        code_user=randint(100000, 999999)
        code[code_user]=email
        with open('code.json', 'w') as c:
           json.dump(code, c)
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(from_email, password)
            
            subject = "Changement de mot de passe"
            body = 'Code de validation : ' + str(code_user)
            message = f'Subject: {subject}\n\n{body}'
            server.sendmail(from_email, email, message)
            server.quit()
            print('E-mail envoyé avec succès')
            return Redirect('/nouveau_mdp.html')
        except:
            print("Erreur lors de l'envoi de l'e-mail")
            return Redirect('/recup_email.html#echec')
    else:
           return Redirect('/recup_email.html#email_introuvable')

def new_mdp(url, vars):
    code_verr=vars['code']
    with open('code.json', 'r') as c:
        code=json.load(c)
    if code_verr in code:
        nouveau_mdp= vars['nouveau_mdp']
        nouveau_mdp = nouveau_mdp.encode()
        hmdp = sha512(salt + nouveau_mdp).hexdigest()
        with open('file.json', 'r') as f:
            hmdp_ref_from_file=json.load(f)
        hmdp_ref_from_file[code[code_verr]][0]=hmdp
        with open('file.json', 'w') as f:
            json.dump(hmdp_ref_from_file,f) 
        del code[code_verr]

        with open('code.json', 'w') as c:
            json.dump(code,c) 
        return Redirect('/connexion.html#changement_valide')
    else:
        return Redirect('/nouveau_mdp.html#code_invalide')
    
def log_out(url, vars):
    id=gethostbyname(gethostname())
    if id in pseu:
        del pseu[id]
    with open('pseudo.json', 'w') as p:
          json.dump(pseu,p)
          
    return Redirect('/accueil.html')

def report(url, vars):
    email = 'sacreblog39@gmail.com'
    from_email = 'sacreblog39@gmail.com' # Remplacez cette valeur par votre adresse e-mail
    password = 'knkynmnmtzekfupd' # Remplacez cette valeur par votre mot de passe

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        subject = "Report"
        body = vars['report']
        message = f'Subject: {subject}\n\n{body}'

        server.sendmail(from_email, email, message)
        server.quit()
        print('E-mail envoyé avec succès')
        return Redirect('/accueil.html')

    except:
        print("Erreur lors de l'envoi de l'e-mail")
        return Redirect('/report.html')

pageDynamique('/nouveau_mdp', new_mdp)
pageDynamique('/report', report)
pageDynamique('/devoirs', nouveau_devoirs)
pageDynamique('/log_out', log_out)
pageDynamique('/recup_email', send_email)
pageDynamique('/message', nouveau_message)
pageDynamique("/",start)
pageDynamique("/inscription", inscription)
pageDynamique("/connexion", connexion)
lancerServeur()
#webbrowser.open('http://localhost:8000/')
#urllib.urlopen("http://localhost:8000/")