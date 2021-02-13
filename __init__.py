from os.path import join, abspath, dirname
import os.path
import random
from adapt.tools.text.tokenizer import EnglishTokenizer
#from mycroft.messagebus.client.ws import WebsocketClient
from mycroft.messagebus.message import Message
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger
from mycroft.util import nice_number
from mycroft.util.parse import fuzzy_match
from mycroft.util.parse import  extract_number, normalize
from mycroft.util.parse import match_one
from mycroft.audio import wait_while_speaking
from mycroft import MycroftSkill, intent_file_handler
from mycroft.skills.context import *
import subprocess
from mycroft.util.parse import normalize
import re
import time
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler


class AllRecipes(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        
    def initialize(self):
        self.gui.register_handler('pause', self.handle_pause)
        self.gui.register_handler('cont', self.handle_cont)
        self.gui.register_handler('scrot', self.handle_scrot)
        #Register list of recipe titles that are held in a padatious entity
        self.register_entity_file("title.entity")
        self.process = None        
        self.play_list = {

        }      
       
        self.is_MUTE = False
        self.is_choice = None
        self.is_title = None
        self.process = None 
        self.is_reading = False
        self.is_paused = False
        self.is_continue = False
        self.is_repeat = False 
        self.is_next = False
          

######## gui interface ######### 
    

    @intent_handler(IntentBuilder('').require('scrot'))
    def handle_scrot(self, message):
           self.is_reading = False   
           print(self.is_title)
           TITLE1 = self.is_title
           TITLE1 = TITLE1.replace(".", "") 
           TITLE1 = TITLE1.replace(" ", "_") 
           TITLE1 = TITLE1[:-1]
           TITLE1 = TITLE1[:-1]
           TITLE1 = TITLE1[:-1]
           EXT = ".jpg"
           TITLE1 = "".join((TITLE1, EXT))
           #TITLE1 = TITLE1 + EXT
           print(TITLE1)
           os.system("spectacle -a -b -o $HOME/Pictures/recipes/"+ TITLE1 )
     
    @intent_handler(IntentBuilder('').require('pause'))
    def handle_pause(self, message):
           self.is_reading = False
     
               ############Directionss###########       
        
    @intent_file_handler('pick.directions.intent')
    def handle_pick_directions(self, message):
       self.is_reading = True              
       self.is_paused = True
       self.is_continue = False
       self.is_repeat = True

       filepath = open("recipe.dat","r")  
       path = filepath.read()
       #Recipe_str = os.popen("cat " + path + " |  sed -n '/^Directions/, $ p' | sed  '1d' ").read()
       Recipe_str = os.popen("skills/all-recipes-skill/bash/"  + self.lang +  "/./directions " + path).read()
       TITLE_OL = "DIRECTIONS"
       PIC_OL = os.popen("cat PIC_URL ").read()
       self.gui.show_image(PIC_OL)
       file0 = open("recipeD.conv","w")
       file0.write(Recipe_str)
       file0.close() 
       file1 = open("recipeD.dat","w")
       file1.write('recipeD.conv')
       file1.close() 
       filepath = open("recipeD.dat","r")  
       path = filepath.read()
       
       Rcnt = 0
       ########## FRACTION COINVERSION ############
       Recipe_CONV = os.popen("skills/all-recipes-skill/bash/" + self.lang +  "/./FRAC " + path).read()
       file0 = open("recipeD.conv","w")
       file0.write(Recipe_CONV)
       file0.close() 
       file1 = open("recipe2.dat","w")
       file1.write('recipeD.conv')
       file1.close() 
       filepath = open("recipe2.dat","r")  
       path = filepath.read()
 ############################################# 
       Recipe_str = os.popen("cat recipeD.conv").read()
       self.gui['title'] = TITLE_OL
       self.gui['reclist'] = Recipe_str
       self.gui['summary'] = "            "
       self.gui.show_page("recipe.qml", override_idle=600)
 
       self.is_reading = True
       with open(path) as fp:  

                  for cnt, line in enumerate(fp):
                      if self.is_reading is False:                     
                         break
                      self.speak("{}".format(line), wait=True) 

           
       if self.is_reading is True:
            self.is_reading = False


        
        ############ingredients###########       
        
    @intent_file_handler('pick.ingredient.intent')
    def handle_pick_ingredients(self, message):
       self.is_reading = True             
       self.is_paused = True
       self.is_continue = False
       self.is_repeat = True       

       filepath = open("recipe.dat","r")  
       path = filepath.read()
       Recipe_str = os.popen("skills/all-recipes-skill/bash/"  + self.lang +  "/./ingredient " + path).read()
       TITLE_OL =  "INGREDIENTS"
       Rcnt = 0
       PIC_OL = os.popen("cat PIC_URL ").read()
       self.gui.show_image(PIC_OL)
       self.gui['title'] = TITLE_OL
       self.gui['reclist'] = Recipe_str
       self.gui['summary'] = "          "
       self.gui.show_page("recipe.qml", override_idle=600)
       
       file0 = open("recipeI.conv","w")
       file0.write(Recipe_str)
       file0.close() 
       file1 = open("recipeI.dat","w")
       file1.write('recipeI.conv')
       file1.close() 
       filepath = open("recipeI.dat","r")  
       path = filepath.read()
       
       ########## FRACTION COINVERSION ############
       Recipe_CONV = os.popen("skills/all-recipes-skill/bash/" + self.lang +  "/./FRAC " + path).read()
       file0 = open("recipeI.conv","w")
       file0.write(Recipe_CONV)
       file0.close() 
       file1 = open("recipe2.dat","w")
       file1.write('recipeI.conv')
       file1.close() 
       filepath = open("recipe2.dat","r")  
       path = filepath.read()
 ############################################# 
       self.is_reading = True
       with open(path) as fp:  
                  for cnt, line in enumerate(fp):
                      if self.is_reading is False:                     
                         break
                      self.speak("{}".format(line), wait=True) 

           
       if self.is_reading is True:
            self.is_reading = False
       
    
     
 ########## SEARCH RESULTS ################         
    @intent_handler(IntentBuilder('').require('cont'))
    def handle_cont(self, message):
           
        filepath = open("tmp_recipe","r")  
        path = filepath.read()
        #self.gui.show_text(path, override_idle=None)
        TITLE_LI = "SEARCH RESULTS"
        self.gui.clear()
        LOGO = ("/opt/mycroft/skills/all-recipes-skill/bash/" + self.lang +  "/pics/AR.png")
        LOGO = LOGO.strip()
        self.gui.show_image(LOGO)  
        time.sleep(1)
        self.gui['title'] = TITLE_LI  
        self.gui['reclist'] = path
        self.gui['summary'] = ""
        #self.gui.show_text(summary)
        self.gui.show_page("recipe.qml", override_idle=600)
        #if self.ask_yesno("which.recipe.number") == "number one":
        self.is_reading = True              
        self.is_paused = True
        self.is_continue = False
        self.is_repeat = True
        self.is_recipe = False  
        #if self.is_MUTE is True:                     
           #self.is_reading = False
           #break
        NUMBER =1 
        for  line in (path.splitlines()):   
               #self.speak(path)
               #RECNT
               self.is_title = ""
               if self.is_reading is False:                     
                   break
               else: 
                    if self.is_paused is True:   
                       #self.speak(path, wait=True)
                       for x in range(10):
                           self.is_reading = False
                           #time.sleep(6)
                           if self.is_continue is True:
                                  self.is_continue = False
                                  self.is_paused = False
                                  break
                              
                           else:
                               if self.is_repeat is True:
                                  wait_while_speaking() 
                                  #self.speak(path, wait=True)
                                  #self.speak("{}".format(line), wait=True)
                                  time.sleep(10)
                                  self.is_repeat = False
                                  response = self.get_response('which.recipe.number') #/dialog/lang/which.recipe.number.dialog
                                  
                                  if response == '1':
                                     NUMBER = '1'
                                     self.is_recipe = True
                                     break     
                                 
                                  if response == '2':
                                     NUMBER = '2'
                                     self.is_recipe = True
                                     break  
                                                                   
                                  if response == '3':
                                     NUMBER = '3'
                                     self.is_recipe = True
                                     break     
                                 
                                  if response == '4':
                                     NUMBER = '4'

                                     self.is_recipe = True
                                     break 
                                                                    
                                  if response == '5':
                                     NUMBER = '5'
                                     self.is_recipe = True
                                     break 
                                 
                                  if response == '6':
                                     NUMBER = '6'
                                     self.is_recipe = True
                                     break 
                                 
                                  if response == '7':
                                     NUMBER = '7'
                                     self.is_recipe = True
                                     break    
                                 
                                  if response == '8':
                                     NUMBER = '8'
                                     self.is_recipe = True
                                     break
                                 
                                  if response == '9':
                                     NUMBER = '9'
                                     self.is_recipe = True
                                     break  
                                 
                                  if response == '10':
                                     NUMBER = '10'
                                     self.is_recipe = True
                                     break  
                                                                   
                                  if response == '11':
                                     NUMBER = '11'
                                     self.is_recipe = True
                                     break    
                                 
                                  if response == '12':
                                     NUMBER = '12'
                                     self.is_recipe = True
                                     break 
                                                                    
                                  if response == '13':
                                     NUMBER = '13'
                                     self.is_recipe = True
                                     break   
                                 
                                  if response == '14':
                                     NUMBER = '14'
                                     self.is_recipe = True
                                     break 
                                 
                                  if response == '15':
                                     NUMBER = '15'
                                     self.is_recipe = True
                                     break    
                                 
                                  if response == '16':
                                     NUMBER = '16'
                                     self.is_recipe = True
                                     break
                                 
                                  if response == '17':
                                     NUMBER = '17'
                                     self.is_recipe = True
                                     break     
                                 
                                  if response == '18':
                                     NUMBER = '18'
                                     self.is_recipe = True
                                     break 
                                 
                                  if response == '19':
                                     NUMBER = '19'
                                     self.is_recipe = True
                                     break   
                                 
                                  if response == '20':
                                     NUMBER = '20'
                                     self.is_recipe = True
                                     break
                                          
                                  elif self.voc_match(response, 'repeat'): #/vocab/lang/repeat.voc
                                     self.is_repeat = True
                                     self.is_recipe = False
                                     break
                                   
                                  elif self.voc_match(response,'new_search'): #/vocab/lang/new_search.voc
                                     self.is_recipe = False
                                     self.speak_dialog('new.search') #/dialog/lang/new.search.dialog
                                     break  
                                  if self.is_reading is False:                     
                                     break
                                     
                                  else:
                                     time.sleep(10) 
                                     self.is_repeat = True
                                          
                               if self.is_next is True:
                                  wait_while_speaking() 
     
                                  self.is_next = False 
                                  self.is_paused = True
                                  self.is_repeat = True
                                  break      
           
        if self.is_recipe is True:
           self.speak(NUMBER)  
           self.is_choice = NUMBER
           #os.system("echo " + NUMBER)
           Recipe_OL = os.popen("skills/all-recipes-skill/bash/" + self.lang +  "/./process_recipe3 " + NUMBER).read()
           TITLE_OL = os.popen("skills/all-recipes-skill/bash/" + self.lang +  "/./TITLE " + NUMBER).read()
           PIC_OL = os.popen("cat PIC_URL ").read()
           self.gui.show_image(PIC_OL)
           #print(Recipe_OL)
           print(TITLE_OL)
           TITLE_OL = TITLE_OL.upper()
           TITLE_OL = TITLE_OL.replace(".", "")
           self.is_title = TITLE_OL
           
           os.system("echo " + TITLE_OL)
           time.sleep(5)
           file0 = open("recipe.lis","w")
           file0.write(TITLE_OL)
           file0.write('')
           file0.write(Recipe_OL)
           file0.close() 
           
           file1 = open("recipe.dat","w")
           file1.write('recipe.lis')
           file1.close() 
           filepath = open("recipe.dat","r")  
           path = filepath.read()

########## FRACTION COINVERSION ############
           Recipe_CONV = os.popen("skills/all-recipes-skill/bash/" + self.lang +  "/./FRAC " + path).read()
           file0 = open("recipe.conv","w")
           file0.write(Recipe_CONV)
           file0.close() 
           file1 = open("recipe2.dat","w")
           file1.write('recipe.conv')
           file1.close() 
           filepath = open("recipe2.dat","r")  
           path = filepath.read()
 #############################################     
           
           self.gui['title'] = TITLE_OL
           self.gui['reclist'] = ""
           self.gui['summary'] = Recipe_OL
           self.gui.show_page("recipe.qml", override_idle=600)
           self.is_reading = True
           with open(path) as fp:  
                  for cnt, line in enumerate(fp):
                      if self.is_reading is False:                     
                         break
                      self.speak("{}".format(line), wait=True) 

           
        if self.is_reading is True:
            self.is_reading = False
      
        
######### get online recipes ###########       
    @intent_file_handler('online.getrecipe.intent')
    def handle_online_getrecipe(self, message):
        os.popen("skills/Energy-Monitor/./GUI.sh ")
     
        #self.is_MUTE = False
        self.speak_dialog('online.getrecipes')
        time.sleep(5)
        #wait_while_speaking()
        INPUT = message.data.get('group')
        os.system("skills/all-recipes-skill/bash/" + self.lang +  "/./online " + INPUT) 
        #time.sleep(1)
        filepath = open("tmp_recipe","r")  
        path = filepath.read()
        #self.gui.show_text(path, override_idle=None)
        self.process = None
        TITLE_LI = "SEARCH RESULTS"
        self.gui.clear()
        LOGO = ("/opt/mycroft/skills/all-recipes-skill/bash/" + self.lang + "/pics/AR.png")
        LOGO = LOGO.strip()
        os.system("echo " + LOGO)
        self.gui.show_image(LOGO)
        time.sleep(1)
        self.gui['title'] = TITLE_LI
        self.gui['reclist'] = path
        self.gui['summary'] = ""
        #self.gui.show_text(summary)
        self.gui.show_page("recipe.qml", override_idle=600)
        #if self.ask_yesno("which.recipe.number") == "number one":
        self.is_reading = True              
        self.is_paused = True
        self.is_continue = False
        self.is_repeat = True
        self.is_recipe = False  
        #self.is_MUTE = False
        NUMBER =1 
        for  line in (path.splitlines()):   
               #self.speak(path)
               #RECNT
               self.is_title = ""
               if self.is_reading is False:                     
                   break
               else: 
                    if self.is_paused is True:   
                       #self.speak(path, wait=True)
                       for x in range(10):
                           #time.sleep(6)
                           if self.is_continue is True:
                                  self.is_continue = False
                                  self.is_paused = False
                                  break
                              
                           else:
                               if self.is_repeat is True:
                                  wait_while_speaking() 
                                  #self.speak(path, wait=True)
                                  #self.speak("{}".format(line), wait=True)
                                  time.sleep(5)
                                  self.is_repeat = False
                                  self.is_repeat = False
                                  response = self.get_response('which.recipe.number') #/dialog/lang/which.recipe.number.dialog
                                  
                                  if response == '1':
                                     NUMBER = '1'
                                     self.is_recipe = True
                                     break     
                                 
                                  if response == '2':
                                     NUMBER = '2'
                                     self.is_recipe = True
                                     break  
                                                                   
                                  if response == '3':
                                     NUMBER = '3'
                                     self.is_recipe = True
                                     break     
                                 
                                  if response == '4':
                                     NUMBER = '4'

                                     self.is_recipe = True
                                     break 
                                                                    
                                  if response == '5':
                                     NUMBER = '5'
                                     self.is_recipe = True
                                     break 
                                 
                                  if response == '6':
                                     NUMBER = '6'
                                     self.is_recipe = True
                                     break 
                                 
                                  if response == '7':
                                     NUMBER = '7'
                                     self.is_recipe = True
                                     break    
                                 
                                  if response == '8':
                                     NUMBER = '8'
                                     self.is_recipe = True
                                     break
                                 
                                  if response == '9':
                                     NUMBER = '9'
                                     self.is_recipe = True
                                     break  
                                 
                                  if response == '10':
                                     NUMBER = '10'
                                     self.is_recipe = True
                                     break  
                                                                   
                                  if response == '11':
                                     NUMBER = '11'
                                     self.is_recipe = True
                                     break    
                                 
                                  if response == '12':
                                     NUMBER = '12'
                                     self.is_recipe = True
                                     break 
                                                                    
                                  if response == '13':
                                     NUMBER = '13'
                                     self.is_recipe = True
                                     break   
                                 
                                  if response == '14':
                                     NUMBER = '14'
                                     self.is_recipe = True
                                     break 
                                 
                                  if response == '15':
                                     NUMBER = '15'
                                     self.is_recipe = True
                                     break    
                                 
                                  if response == '16':
                                     NUMBER = '16'
                                     self.is_recipe = True
                                     break
                                 
                                  if response == '17':
                                     NUMBER = '17'
                                     self.is_recipe = True
                                     break     
                                 
                                  if response == '18':
                                     NUMBER = '18'
                                     self.is_recipe = True
                                     break 
                                 
                                  if response == '19':
                                     NUMBER = '19'
                                     self.is_recipe = True
                                     break   
                                 
                                  if response == '20':
                                     NUMBER = '20'
                                     self.is_recipe = True
                                     break
                                          
                                  elif self.voc_match(response, 'repeat'): #/vocab/lang/repeat.voc
                                     self.is_repeat = True
                                     self.is_recipe = False
                                     break
                                   
                                  elif self.voc_match(response,'new_search'): #/vocab/lang/new_search.voc
                                     self.is_recipe = False
                                     self.speak_dialog('new.search') #/dialog/lang/new.search.dialog
                                     break  
                                  if self.is_reading is False:                     
                                     breakk  
                                 
                                  if self.is_reading is False:                     
                                     break
                                     
                                  else:
                                     time.sleep(10) 
                                     self.is_repeat = True
                                          
                               if self.is_next is True:
                                  wait_while_speaking() 
     
                                  self.is_next = False 
                                  self.is_paused = True
                                  self.is_repeat = True
                                  break                                
                           
  
           
        if self.is_recipe is True:
           self.speak(NUMBER) 
           self.is_choice = NUMBER
           #LANG = self.lang
           #os.system("echo " + LANG)
           Recipe_OL = os.popen("skills/all-recipes-skill/bash/" + self.lang +  "/./process_recipe3 " + NUMBER).read()
           TITLE_OL = os.popen("skills/all-recipes-skill/bash/" + self.lang +  "/./TITLE " + NUMBER).read()
           PIC_OL = os.popen("cat PIC_URL ").read()
           self.gui.show_image(PIC_OL)

           TITLE_OL = TITLE_OL.upper()
           TITLE_OL = TITLE_OL.replace(".", "")
           self.is_title = TITLE_OL
           
           os.system("echo " + TITLE_OL)
           time.sleep(5)
           file0 = open("recipe.lis","w")
           file0.write(TITLE_OL)
           file0.write('')
           file0.write(Recipe_OL)
           file0.close() 
           
           file1 = open("recipe.dat","w")
           file1.write('recipe.lis')
           file1.close() 
           filepath = open("recipe.dat","r")  
           path = filepath.read()
           
########## FRACTION COINVERSION ############
           Recipe_CONV = os.popen("skills/all-recipes-skill/bash/" + self.lang +  "/./FRAC " + path).read()
           file0 = open("recipe.conv","w")
           file0.write(Recipe_CONV)
           file0.close() 
           file1 = open("recipe2.dat","w")
           file1.write('recipe.conv')
           file1.close() 
           filepath = open("recipe2.dat","r")  
           path = filepath.read()
 #############################################   
 
           self.gui['title'] = TITLE_OL
           self.gui['reclist'] = ""
           self.gui['summary'] = Recipe_OL
           self.gui.show_page("recipe.qml", override_idle=600)
           with open(path) as fp:  
                  for cnt, line in enumerate(fp):
                      if self.is_reading is False:                     
                         break
                      self.speak("{}".format(line), wait=True)
 
           
        if self.is_reading is True:
            self.is_reading = False
      
        
 ###############EMAILRecipe######################       
    @intent_file_handler('email.read.intent')
    def handle_email_read(self, message):
       self.speak_dialog('online.email')
       #self.speak('Sending recipe to your email')
       filepath = open("recipe.dat","r")  
       path = filepath.read()
        
       os.system("skills/all-recipes-skill/./email " + path )
       self.speak('done')
        
  
##########FAV#############
    #Play random recipe from list
    @intent_file_handler('recipes.pick.intent')
    def handle_recipes_pick(self, message):
        os.popen("skills/Energy-Monitor/./GUI.sh ")
        wait_while_speaking()
        self.speak_dialog('recipes.pick')
        recipe_file = list(self.play_list.values())
        recipe_file = random.choice(recipe_file)
        print(recipe_file)
        #if os.path.isfile(recipe_file):
        wait_while_speaking()
        filepath =  (recipe_file)
        file1 = open("recipe.dat","w")
        file1.write(filepath)
        file1.close()   
        recipe = open(filepath,"r")  
        recipe = recipe.read()

        TMP = os.popen("skills/all-recipes-skill/bash/" + self.lang +  "/./FILE " + filepath).read()
        IMAGE = ("/opt/mycroft/skills/all-recipes-skill/recipes/pics/" + TMP  )
        IMAGE = IMAGE.strip()
        print(IMAGE)
        
########## FRACTION COINVERSION ############
        Recipe_CONV = os.popen("skills/all-recipes-skill/bash/" + self.lang +  "/./FRAC " + filepath).read()
        file0 = open("recipe.conv","w")
        file0.write(Recipe_CONV)
        file0.close() 
        file1 = open("recipe2.dat","w")
        file1.write('recipe.conv')
        file1.close() 
        filepath = open("recipe2.dat","r")  
        path = filepath.read()
 #############################################          
        self.gui.clear()
        self.gui.show_image(IMAGE)
        time.sleep(1)
        self.is_reading = True 
        with open(path) as fp:  
              for cnt, line in enumerate(fp):
                      if self.is_reading is False:                     
                         break
                      self.speak("{}".format(line), wait=True)
                      self.gui['title'] = "RANDOM FAVORITES"
                      self.gui['reclist'] = " "
                      self.gui['summary'] = recipe
                      self.gui.show_page("recipe.qml", override_idle=600)  

                  

    #Pick recipe by title
    @intent_file_handler('pick.recipe.intent')
    def handle_pick_recipe(self, message):
        os.popen("skills/Energy-Monitor/./GUI.sh ")
        self.speak_dialog('pick.recipes')
        wait_while_speaking()
        
        title = message.data.get('title')
        score = match_one(title, self.play_list)
        print(score)
        if score[1] > 0.5:
            self.speak('your recipe is ')
            filepath =  (score[0])
            file1 = open("recipe.dat","w")
            file1.write(filepath)
            file1.close()     
            recipe = open(filepath,"r")  
            recipe = recipe.read() 
 
            TMP = os.popen("skills/all-recipes-skill/bash/" + self.lang +  "/./FILE " + filepath).read()
            IMAGE = ("/opt/mycroft/skills/all-recipes-skill/recipes/pics/" + TMP  )
            IMAGE = IMAGE.strip()
            print(IMAGE)
            
########## FRACTION COINVERSION ############
            Recipe_CONV = os.popen("skills/all-recipes-skill/bash/" + self.lang +  "/./FRAC " + filepath).read()
            file0 = open("recipe.conv","w")
            file0.write(Recipe_CONV)
            file0.close() 
            file1 = open("recipe2.dat","w")
            file1.write('recipe.conv')
            file1.close() 
            filepath = open("recipe2.dat","r")  
            path = filepath.read()
 #############################################                
            self.gui.clear()
            self.gui.show_image(IMAGE)
            time.sleep(3)
            self.is_reading = True 
            with open(path) as fp:  
                  for cnt, line in enumerate(fp):
                      if self.is_reading is False:                     
                         break
                      self.speak("{}".format(line), wait=True)
                      self.gui['title'] = "FAVORITES"
                      self.gui['reclist'] = " "
                      self.gui['summary'] = recipe
                      self.gui.show_page("recipe.qml", override_idle=600)  

                      
                      
        else:
           #find  return None
            #self.speak('Sorry I could not find that recipe in my library')
            self.speak_dialog('online.sorry')

    #List recipes in library
    @intent_file_handler('list.recipes.intent')
    def handle_list_recipes(self, message):
        os.popen("skills/Energy-Monitor/./GUI.sh ")
        wait_while_speaking()
        recipe_list = list(self.play_list.keys())
        print(recipe_list)
        
        filepath = "skills/all-recipes-skill/vocab/" + self.lang +  "/title.entity"
        recipe = open(filepath,"r")  
        recipe = recipe.read()    
        #file1 = open("tmp_recipe","w")
        #file1.write(recipe)
        #file1.close()   
        #self.is_MUTE = True  
        LOGO = ("/opt/mycroft/skills/all-recipes-skill/bash/" + self.lang +  "/pics/AR.png")
        LOGO = LOGO.strip()
        self.gui.show_image(LOGO)
        time.sleep(3)
        self.gui['title'] = "FAVORITES"
        self.gui['reclist'] = recipe
        self.gui['summary'] = " "
        self.gui.show_page("recipe.qml", override_idle=600)
        #self.speak_dialog('list.recipes', data=dict(recipes=recipe_list))

    
    def stop(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()
            self.process.wait()
            
   ###### get recipes ###########       
    @intent_file_handler('pick.getrecipe.intent')
    def handle_pick_getrecipe(self, message):
        self.speak_dialog('pick.getrecipes')
        wait_while_speaking()
        NUMBER  = self.is_choice 
        os.system("skills/all-recipes-skill/bash/" + self.lang +  "/./recipe " + NUMBER +  " "  + self.lang ) 



           
        #self.speak('Finished download new recipes from all recipe  dot com') 
        self.speak_dialog('online.finished')
     
def create_skill():
    return AllRecipes()

