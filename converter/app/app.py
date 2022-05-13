# Pour créer l'interface
from PySide2 import QtWidgets
# Pour récupérer les devises
import currency_converter

class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.c = currency_converter.CurrencyConverter()
        self.setWindowTitle("Convertisseur de devises")
        self.setup_ui()
        self.set_default_values()
        self.setup_css()
        self.resize(500,50)
        self.setup_connections()

    
    def setup_ui(self):
        """
        Création de l'interface : Convertisseur de devises
        """
        # On créer un layout qui nous permet de positionner nos différents widgets. self: parenter à notre fenêtre
        self.layout = QtWidgets.QHBoxLayout(self)
        # ************** On créer nos différents widgets disponibles grâce au module PySide **************
        # Menu déroulant cbb : ComboBox 
        self.cbb_deviseFrom =QtWidgets.QComboBox()
        # Spin Box (spn) pour rentrer une valeur 
        self.spn_amount = QtWidgets.QSpinBox()
        # Deuxième menu déroulant cbb : ComboBox
        self.cbb_deviseTo = QtWidgets.QComboBox()
        # Spin Box (spn) pour rentrer une valeur
        self.spn_converted_amount = QtWidgets.QSpinBox()
        # Bouton (btn) : ici pour inverser les devises
        self.btn_inverser = QtWidgets.QPushButton("Inverser devises")
        
        # On ajoute nos widgets créer au dessus dans notre layout :
        self.layout.addWidget(self.cbb_deviseFrom)
        self.layout.addWidget(self.spn_amount)
        self.layout.addWidget(self.cbb_deviseTo)
        self.layout.addWidget(self.spn_converted_amount)
        self.layout.addWidget(self.btn_inverser)

    def setup_css(self):
        """
        Redéfinit le style de l'application
        """
        self.setStyleSheet(""" 
        background-color: #B8CBD0;
        border: none;
        """)

        self.btn_inverser.setStyleSheet("""
        background-color: #ECF8F6;
        padding: 10px;
        border-radius: 5px;
        """)
    
    def set_default_values(self):
        """
        Ajoute des valeurs par defauts à l'intérieur de nos widgets présent dans notre interfaces
        """
        # On converti le set (liste sans deux valeurs identique) en liste que l'on trie par ordre alpahbétique
        self.cbb_deviseFrom.addItems(sorted(list(self.c.currencies)))
        self.cbb_deviseTo.addItems(sorted(list(self.c.currencies)))
        # On définit par défaut la valeur EUR 
        self.cbb_deviseFrom.setCurrentText("EUR")
        self.cbb_deviseTo.setCurrentText("EUR")
        # On modifie la plage de valeur
        self.spn_amount.setRange(1, 1000000)
        self.spn_converted_amount.setRange(1, 1000000)
        # Valeur par défaut
        self.spn_amount.setValue(100)
        self.spn_converted_amount.setValue(100)
        
    def setup_connections(self):
        """
        Connecte les différents widgets a d'autres méthodes de notre classe grâce au signaux (click, activated, valueChange)
        """
        self.cbb_deviseFrom.activated.connect(self.compute)
        self.cbb_deviseTo.activated.connect(self.compute)
        self.spn_amount.valueChanged.connect(self.compute)
        self.btn_inverser.clicked.connect(self.change_devises)

    def compute(self):
        """
        Réalise le calcul pour convertir le montant d'une devise à une autre
        """
        # On recupère nos valeurs
        amount = self.spn_amount.value()
        devise_from = self.cbb_deviseFrom.currentText()
        devise_to = self.cbb_deviseTo.currentText()
            # Convertion
        try:
            result = self.c.convert(amount, devise_from, devise_to)  
        except currency_converter.currency_converter.RateNotFoundError:
            print("La conversion n'as pas fonctionné")
        else:
            # Affiche le montant converti
            self.spn_converted_amount.setValue(result)
        

    def change_devises(self):
        """
        Inverse les devises
        """
        devise_from = self.cbb_deviseFrom.currentText()
        devise_to = self.cbb_deviseTo.currentText()
        # On inverse les valeurs 
        self.cbb_deviseFrom.setCurrentText(devise_to)
        self.cbb_deviseTo.setCurrentText(devise_from)
        # On appelle la méthode permettant de faire le calcul
        self.compute()


# On cree notre application
app = QtWidgets.QApplication([])
# On cree une fenêtre : instance de App
win = App()
# On cree 1 fenêtre
win.show()
# On l'execute
app.exec_()
