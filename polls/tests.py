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
        test_questions = ["What's ya name?", "What's ya pet's name?"]

        # introduïm dades per pregunta
        for question in test_questions:
            # Buscar al butón 'Add' de 'Questions'
            self.selenium.find_element(By.XPATH, "//a[@href='/admin/polls/question/add/']").click()
            
            # Rellenar el formulari
            question_text = self.selenium.find_element(By.NAME, "question_text") 
            question_text.send_keys(question)
            
            question_date = self.selenium.find_element(By.LINK_TEXT,"Today").click()
            question_time = self.selenium.find_element(By.LINK_TEXT,"Now").click()
            
            self.selenium.find_element(By.XPATH,'//input[@value="Save"]').click()
            
            # comprovem de nou que el títol de la pàgina és el què esperem
            self.assertEqual( self.selenium.title , "Select question to change | Django site admin" )
        
        # introduïm dades per a 'Choice'
        # matrix = {"What's ya name?": ["Joan", "Ariadna"], "What's ya pet's name?": ["Fify", "Kitty"]}
        q_name = ["What's ya name?"]
        name_choices = ["Joan", "Ariadna"]
        q_pet = ["What's ya pet's name?"]
        pet_choices = ["Fify", "Kitty"]

        for name in name_choices:
            # accedir a la pàgina d'afegeix opcions des de el menú lateral
            self.selenium.find_element(By.XPATH, "//a[@href='/admin/polls/choice/add/']").click()
 
            # self.selenium.get('%s%s' % (self.live_server_url, '/admin/polls/choice/add'))
            # comprovem que el títol de la pàgina és el què esperem
            self.assertEqual( self.selenium.title , "Add choice | Django site admin" )
            
            # Rellenar el formulari
            # Seleccionem la cuestió correcta
            select_element = self.selenium.find_element(By.NAME, "question")
            select = Select(select_element)
            select.select_by_visible_text("What's ya name?")
            
            choice_text = self.selenium.find_element(By.NAME, "choice_text") 
            choice_text.send_keys(name)
            self.selenium.find_element(By.XPATH,'//input[@value="Save"]').click()
            
            # comprovem de nou que el títol de la pàgina és el què esperem
            self.assertEqual( self.selenium.title , "Select choice to change | Django site admin" )

        for name in pet_choices:
        # accedir a la pàgina d'afegeix preguntes
        
            self.selenium.get('%s%s' % (self.live_server_url, '/admin/polls/choice/add'))
            # comprovem que el títol de la pàgina és el què esperem
            self.assertEqual( self.selenium.title , "Add choice | Django site admin" )
            
            # Rellenar el formulari
            # Seleccionem la cuestió correcta
            select_element = self.selenium.find_element(By.NAME, "question")
            select = Select(select_element)
            select.select_by_visible_text("What's ya pet's name?")
            
            choice_text = self.selenium.find_element(By.NAME, "choice_text") 
            choice_text.send_keys(name)
            self.selenium.find_element(By.XPATH,'//input[@value="Save"]').click()
            
            # comprovem de nou que el títol de la pàgina és el què esperem    
            self.assertEqual( self.selenium.title , "Select choice to change | Django site admin" )
