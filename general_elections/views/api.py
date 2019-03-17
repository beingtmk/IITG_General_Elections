from poplib import *

def webmail_login(username, password, login_server):
	em = '%s@iitg.ernet.in' %(username)
	mail = POP3_SSL(login_server)
	mail.user(username)
	try:
		mail.pass_(password)
		mail.quit()
	except:
		return False
	return True
