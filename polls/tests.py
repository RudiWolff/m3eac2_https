from django.test import TestCase

# Create your tests here.

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

class MySeleniumTests(StaticLiveServerTestCase):
    # carregar una BD de test
    fixtures = ['testdb.json',]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = Options()
        cls.selenium = WebDriver(options=opts)
        cls.selenium.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        # tanquem browser
        # comentar la propera línia si volem veure el resultat de l’execució al navegador
        # cls.selenium.quit()
        cls.selenium.implicitly_wait(500)
        super().tearDownClass()

    def test_login(self):
        # anem directament a la pàgina d’accés a l’admin panel
        self.selenium.get('%s%s' % (self.live_server_url, '/admin/login/'))
        
        # comprovem que el títol de la pàgina és el què esperem
        self.assertEqual( self.selenium.title , "Log in | Django site admin" )
        
        # introduïm dades de login i cliquem el botó "Log in" per entrar
        username_input = self.selenium.find_element(By.NAME,"username")
        username_input.send_keys('isard')
        password_input = self.selenium.find_element(By.NAME,"password")
        password_input.send_keys('pirineus')
        self.selenium.find_element(By.XPATH,'//input[@value="Log in"]').click()

        # comprovem que el títol de la pàgina és el què esperem
        self.assertEqual( self.selenium.title , "Site administration | Django site admin" )
        
        # Definició de preguntes per inserir
        matrix = {
            "What's ya name?": ["Joan", "Ariadna"], 
            "What's ya pet's name?": ["Fiffy", "Kitty"]
            }
        
        # introduïm dades per pregunta
        for question in matrix:
            # Buscar al butón 'Add' de 'Questions'
            self.selenium.find_element(By.XPATH, "//a[@href='/admin/polls/question/add/']").click()
            
            # comprovem de nou que el títol de la pàgina és el què esperem
            self.assertEqual( self.selenium.title , "Add question | Django site admin" )
            
            # Rellenar el formulari
            question_text = self.selenium.find_element(By.NAME, "question_text") 
            question_text.send_keys(question)
            
            # Expandir menú "Date Information" y rellenar campos
            self.selenium.find_element(By.ID, "fieldset-0-1-heading").click()

            question_date = self.selenium.find_element(By.LINK_TEXT,"Today").click()
            question_time = self.selenium.find_element(By.LINK_TEXT,"Now").click()
            
            index = 0
            
            # introduïm dades per a 'Choice'
            for option in matrix[question]:
                # Introducir valor para opcion de index X
                choice_text = self.selenium.find_element(By.NAME, f"choice_set-{index}-choice_text") 
                choice_text.send_keys(option)
                
                # Aumentar index para la siguiente opción
                index += 1
            
            # Guardar el set de 1 pregunta con 2 opciones
            self.selenium.find_element(By.XPATH,'//input[@value="Save"]').click()
            
            # comprovem de nou que el títol de la pàgina és el què esperem
            self.assertEqual( self.selenium.title , "Select question to change | Django site admin" )
            
        # Comprobación de la inserción correcta
        for question in matrix:
            q_valid =  self.selenium.find_element(By.LINK_TEXT, question)
            if q_valid:
                print("Pregunta: ", question)
                self.selenium.find_element(By.LINK_TEXT, question).click()

            # Búsqueda de las opciones
            for option in matrix[question]:
                if self.selenium.find_element(By.XPATH, f'//input[@value="{option}"]'):
                    print(f"\t✓ Opción {option} insertada correctamente")

            # Volver a la lista de las preguntas
            self.selenium.get('%s%s' % (self.live_server_url, '/admin/polls/question/'))
