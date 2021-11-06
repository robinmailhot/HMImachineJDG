from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QDialog, QLCDNumber, QTextEdit, QDialog
from PyQt5 import uic
from PyQt5.QtCore import QTime, QTimer
import sys
import datetime

uiFile = "machine.ui"

class UI(QDialog):
    def __init__(self):
        super(UI, self).__init__()

        #load the ui file
        uic.loadUi(uiFile, self)

        #resource
        self.ressources_list = []
        self.arbre = self.Ressource(self, self.findChild(QPushButton, "arbre_button"), self.findChild(QLabel, "n_arbre"), self.findChild(QLabel, "prix_arbre_label"), 1.0)
        self.cereal = self.Ressource(self, self.findChild(QPushButton, "cereal_button"), self.findChild(QLabel, "n_cereal"), self.findChild(QLabel, "prix_cereal_label"), 1.5)
        self.eau = self.Ressource(self, self.findChild(QPushButton, "eau_button"), self.findChild(QLabel, "n_eau"), self.findChild(QLabel, "prix_eau_label"), 2.0)
        self.farine = self.Ressource(self, self.findChild(QPushButton, "farine_button"), self.findChild(QLabel, "n_farine"), self.findChild(QLabel, "prix_farine_label"), 3.0)
        self.planche = self.Ressource(self, self.findChild(QPushButton, "planche_button"), self.findChild(QLabel, "n_planche"), self.findChild(QLabel, "prix_planche_label"), 3.0)
        self.papier_toilette = self.Ressource(self, self.findChild(QPushButton, "papier_toilette_button"), self.findChild(QLabel, "n_papier_toilette"), self.findChild(QLabel, "prix_papier_toilette_label"), 5.0)
        self.biere = self.Ressource(self, self.findChild(QPushButton, "biere_button"), self.findChild(QLabel, "n_biere"), self.findChild(QLabel, "prix_biere_label"), 6.0)
        self.pain = self.Ressource(self, self.findChild(QPushButton, "pain_button"), self.findChild(QLabel, "n_pain"), self.findChild(QLabel, "prix_pain_label"), 7.0)

        #other widgets
        self.start_stop_button = self.findChild(QPushButton,"start_button")
        self.start_button.clicked.connect(self.start_stop)

        self.reset_button = self.findChild(QPushButton,"reset_button")
        self.reset_button.clicked.connect(self.reset)

        self.robot_tombe_button = self.findChild(QPushButton,"robot_tombe_button")
        self.robot_tombe_button.clicked.connect(self.robot_tombe)




        #penality variables, buttons and labels
        self.n_arbre_parc = 0
        self.n_maison_tombe = 0
        self.arbre_parc_plus_button = self.findChild(QPushButton, 'arbre_parc_plus')
        self.arbre_parc_moins_button = self.findChild(QPushButton, 'arbre_parc_moins')
        self.arbre_parc_plus_button.clicked.connect(self.arbre_parc_button_plus) 
        self.arbre_parc_moins_button.clicked.connect(self.arbre_parc_button_moins)

        self.maison_tombe_plus_button = self.findChild(QPushButton, 'maison_tombe_plus')
        self.maison_tombe_moins_button = self.findChild(QPushButton, 'maison_tombe_moins')
        self.maison_tombe_plus_button.clicked.connect(self.maison_tombe_button_plus)
        self.maison_tombe_moins_button.clicked.connect(self.maison_tombe_button_moins)

        self.n_maison_tombe_label = self.findChild(QLabel, "n_maison_tombe_label")
        self.n_arbre_parc_label = self.findChild(QLabel, "n_arbre_parc_label")
        self.score_final_label = self.findChild(QLabel, 'score_final_label')

        #running
        self.time_running = False

        #score
        self.score_actuel_label = self.findChild(QLabel, "score_actuel_label")
        self.score_actuel = 0
        self.perte_premiere_vente = 0
        self.perte_premiere_vente_label = self.findChild(QLabel, "perte_premiere_vente_label")
        self.penalite = 0
        self.score_final = 0 

        #temps
        self.time_left_label = self.findChild(QLabel, "time_left_label")
        self.time_left = 6
        self.timer = QTimer()
        self.timer.timeout.connect(self.time_update)
        self.timer.start(1000) #start and update avery second


        self.show()


    def time_update(self):
        if self.time_running:
            if self.time_left>1:
                self.change_time()
                self.time_update_prix()
                self.time_update_perte_premiere_vente()
                self.calculate_score_final()

            else:
                self.time_end()

    def change_time(self):
        self.time_left -= 1
        m, s = divmod(self.time_left, 60)
        formatted_time = f'{m:02d}:{s:02d}'

        self.time_left_label.setText(formatted_time)

    def time_update_prix(self):
        for ressource in self.ressources_list:
            ressource.update_prix(1.001)
    
    def time_update_perte_premiere_vente(self):
        for ressource in self.ressources_list:
            if not ressource.premiere_vente_done:
                self.perte_premiere_vente += ressource.prix_init *0.001
        self.perte_premiere_vente_label.setText(str(round(self.perte_premiere_vente,3)))
            

    def start_stop(self):
        if self.time_running: # si il roule deja, on arrete
            self.time_running = False
            self.start_stop_button.setStyleSheet("QPushButton{background-color : green;}")
            self.start_stop_button.setText('Start')
            self.reset_button.setEnabled(True)
            for ressource in self.ressources_list:
                ressource.button.setDisabled(True)
        else:
            self.time_running = True # si il etait arrete
            self.start_stop_button.setStyleSheet("QPushButton{background-color : red;}")
            self.start_stop_button.setText('Stop')
            self.reset_button.setDisabled(True)
            for ressource in self.ressources_list:
                ressource.button.setEnabled(True)

    def time_end(self):
        self.change_time()
        self.time_running = False
        self.start_stop_button.setDisabled(True)
        self.reset_button.setEnabled(True)
        for ressource in self.ressources_list:
            ressource.button.setDisabled(True)
        self.calculate_score_final()

        

         
    def reset(self):
        self.time_running = False
        self.start_stop_button.setEnabled(True)
        self.time_left = 601
        self.change_time()
        self.score_actuel = 0
        self.score_actuel_label.setText(f"{round(self.score_actuel, 2)}")
        self.perte_premiere_vente = 0
        self.perte_premiere_vente_label.setText(f"{round(self.perte_premiere_vente, 2)}")

        for ressource in self.ressources_list:
            ressource.reset()

    def robot_tombe(self):
        for ressource in self.ressources_list:
            ressource.update_prix(0.80)


    def calculate_score_final(self):
        self.score_final = self.score_actuel * (1-self.penalite)
        self.score_final_label.setText(str(round(self.score_final,2)))

    def update_penalite(self, penalite:float):
        #should be called when a penality button is pressed
        self.n_arbre_parc_label.setText(str(self.n_arbre_parc))
        self.n_maison_tombe_label.setText(str(self.n_maison_tombe))
        self.penalite += penalite
        self.calculate_score_final()



    def maison_tombe_button_plus(self, n):
        self.n_maison_tombe += 1
        self.update_penalite(0.05)

    def maison_tombe_button_moins(self, n):
        self.n_maison_tombe -= 1
        self.update_penalite(-0.05)

    def arbre_parc_button_plus(self, n):
        self.n_arbre_parc += 1
        self.update_penalite(0.01)

    def arbre_parc_button_moins(self, n):
        self.n_arbre_parc -= 1
        self.update_penalite(-0.01)

    class Ressource():
        def __init__(self, MainWindow:QDialog, button:QPushButton, n_vendu_label:QLabel, prix_label:QLabel,  prix_init:float):

            self.MainWindow = MainWindow #can acces now the variables from the outter  class
            self.MainWindow.ressources_list.append(self)
            self.button = button
            self.button.clicked.connect(self.vendu)

            self.label = n_vendu_label
            self.premiere_vente_done = False
            self.temps_premiere_vente = 0
            self.n_vendu = 0
            self.prix_init = prix_init
            self.prix = prix_init
            self.prix_label = prix_label

        def reset(self):
            self.n_vendu = 0
            self.label.setText(f"{self.n_vendu}")
            self.button.setDisabled(True)
            self.prix = self.prix_init
            self.prix_label.setText(str(round(self.prix,3)))
            self.premiere_vente_done = False



        def vendu(self):
            self.n_vendu += 1
            self.label.setText(f"{self.n_vendu}")
            self.MainWindow.score_actuel += self.prix
            self.MainWindow.score_actuel_label.setText(f"{round(self.MainWindow.score_actuel, 2)}")
            self.update_prix(0.6)
            if not self.premiere_vente_done:
                self.premiere_vente_done = True
                #self.temps_premiere_vente = self.MainWindow.time_left

        def update_prix(self, k, reset=False):
            # k is the multiplying factor that we want. When updating every second, 1.001 and when selling 0.6
            self.prix = min(self.prix*k, self.prix_init)
            self.prix_label.setText(str(round(self.prix,3)))
            
            
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()



