import sys,os,logging
logging.basicConfig(stream = sys.stderr)
sys.path.insert(0,'/home/shikhar/Documents/Fitbite')
BASE_DIR = os.path.join(os.path.dirname(__file__))

activate_this = os.path.join(BASE_DIR, 'env/Scripts/activate_this.py')
execfile(activate_this, dict(__file__= activate_this))

if BASE_DIR not in sys.path:
	sys.path.append(BASE_DIR)


from app import app as application