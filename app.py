from flask import Flask, render_template, request, jsonify
import os
from tkinter import Tk
from tkinter.filedialog import asksaveasfilename
app = Flask(__name__)

#classe dei task
class Task:
    def __init__(self, name, collaboration_type, functions):
        self.name = name
        self.collaboration_type = collaboration_type
        self.functions = functions
#delle funzioni di ogni task
class Function:
    def __init__(self, id, type, pos, pos1, assigned_to):
        self.id = id
        self.type = type
        self.pos = pos
        self.pos1 = pos1
        self.assigned_to = assigned_to
#classe dei vincoli sulla timeline principale
class Vincolo:
    def __init__(self, id, t1, t2):
        self.id = id
        self.t1 = t1
        self.t2 = t2

#costanti
IND = "Independent"
SYN = "Synchronous"
SIM = "Simultaneous"
SUPP = "Supportive"

#lista di task
lista = []
#lista di vincoli di precedenza sui task
vincoli = []
numeroDominio = 0

###############################################################################
###############################################################################
#                       PAGINA INIZIALE                                       #
###############################################################################
###############################################################################
@app.route('/')
def hello():
    return render_template("index.html", lista=lista)

########################################################################
#       Aggiunta/Rimozione/Modifica di un task al processo
########################################################################
@app.route('/', methods=['POST'])
def aggiungi():
    data = request.json
    functions = []

    if(data[-1] == "new"):
        #aggiunta di tutte le function a una lista
        for i in range(len(data)-2):
            #questo è un int
            f_id = data[i]["id"]
            f_type = data[i]["type"]
            f_pos = data[i]["pos"]
            f_pos1 = data[i]["pos1"]
            f_operator = data[i]["operator"]
            func = Function(f_id, f_type, f_pos, f_pos1, f_operator)
            functions.append(func)

        name = data[-2]["taskName"].replace(" ", "").capitalize()
        collaboration = data[-2]["collab"]
        task = Task(name, collaboration, functions)
        #aggiunta del task alla lista
        lista.append(task)

    if(data[-1] == "removeF"):
        for element in lista:
            if element.name == data[0]:
                for function in element.functions:
                    if function.id == int(data[1]):
                        element.functions.remove(function)
                if len(element.functions) == 0:
                    lista.remove(element)

    if(data[-1] == "removeT"):
        for element in lista:
            if element.name == data[0]:
                for con in vincoli:
                    if con.t1 == element.name:
                        vincoli.remove(con)
                    if con.t2 == element.name:
                        vincoli.remove(con)
                lista.remove(element)

    if(data[-1] == "mod"):
        func = data[1]
        for element in lista:
            if element.name == data[0]:

                f_id = int(func["id"])
                f_type = func["type"]
                f_pos = func["pos"]
                f_pos1 = func["pos1"]
                f_operator = func["operator"]
                f = Function(f_id, f_type, f_pos, f_pos1, f_operator)

                element.functions[:] = [f if x.id==f.id else x for x in element.functions]

    return render_template("index.html", lista=lista)

###############################################################################
#   Reinderizzazione verso la pagina di selezione dei vincoli
###############################################################################
@app.route('/vincoli')
def prosegui():
    if len(lista)>1:
        return render_template("vincoli.html", lista=lista, vincoli=vincoli)
    else:
        return render_template("vincoli.html", lista=[], vincoli=[], v="true")

##############################################################################
#       Salvataggio dei vincoli
##############################################################################
@app.route('/vincoli', methods=['POST'])
def aggiungiVincoli():
    data = request.json

    if(data[-1] == "new"):
        #aggiunta del vincolo alla lista
        con = data[0]
        #questo è un int
        v_id = con["id"]
        t1 = con["t1"]
        t2 = con["t2"]
        v = Vincolo(v_id, t1, t2)
        vincoli.append(v)

    if(data[-1] == "remove"):
        #rimuovi il vincolo dalla lista
        for element in vincoli:
            if element.id == int(data[0]):
                vincoli.remove(element)

    if(data[-1] == "mod"):
        #modifica il vincolo
        con = data[0]

        id = int(con["id"])
        t1 = con["t1"]
        t2 = con["t2"]
        v = Vincolo(id, t1, t2)

        vincoli[:] = [v if x.id==v.id else x for x in vincoli]

    return render_template("vincoli.html", lista=lista, vincoli=vincoli)


###############################################################################
###############################################################################
#funzione che aggiunge un task se la modalità è Independent o Synchronous
###############################################################################
def aggiungiIndValue(function, operator):
    tmp = "\t\t\tt" + str(function.id) + " <!> " 
    if( operator == "Human"):
        tmp += "HumanProcess.process._"
    if( operator == "Robot"):
        tmp += "RoboticProcess.process."
    if( function.type == "Manipolazione"):
        tmp += "Task_manipolazione(?loc" + str(function.id) + ");\n"
        tmp += "\t\t\t?loc" + str(function.id) + " = Pos" + str(function.pos) + ";\n"
        tmp += "\t\t\t\tp" + str(function.id) + " <!> Pos" + str(function.pos) + ".position.REQUIREMENT(?amountP" + str(function.id) + ");\n"
        tmp += "\t\t\t\t?amountP" + str(function.id) + " = 2;\n"
        tmp += "\t\t\t\tp" + str(function.id) + " EQUALS t" + str(function.id) + ";\n"
    if( function.type == "Spostamento"):
        tmp += "Task_spostamento(?from" + str(function.id) + ", ?to" + str(function.id) + ");\n"
        tmp += "\t\t\t?from" + str(function.id) + " = Pos" + str(function.pos) + ";\n"
        tmp += "\t\t\t?to" + str(function.id) + " = Pos" + str(function.pos1) + ";\n"
        # Se l'operatore è solo robot o solo umano la manipolazione è per forza independent
        tmp += "\t\t\t\ts" + str(function.id) + " <!> Pos" + str(function.pos) + ".position.REQUIREMENT(?amountS" + str(function.id) + ");\n"
        tmp += "\t\t\t\t?amountS" + str(function.id) + " = 2;\n"
        tmp += "\t\t\t\ts" + str(function.id) + " EQUALS t" + str(function.id) + ";\n"
        tmp += "\t\t\t\td" + str(function.id) + " <!> Pos" + str(function.pos1) + ".position.REQUIREMENT(?amountD" + str(function.id) + ");\n"
        tmp += "\t\t\t\t?amountD" + str(function.id) + " = 2;\n"
        tmp += "\t\t\t\td" + str(function.id) + " EQUALS t" + str(function.id) + ";\n"
    return tmp

#funzione che aggiunge un task se la modalità è Simultaneous o Supportive
#In queste modalità robot e umano coesistono sempre
#E il task è sempre manipolazione
def aggiungiSuppValue(function):
    tmp = "\t\t\th" + str(function.id) + " <!> HumanProcess.process._Task_manipolazione(?hloc" + str(function.id) + ");\n" 
    tmp += "\t\t\t?hloc" + str(function.id) + " = Pos" + str(function.pos) + ";\n"
    tmp += "\t\t\t\thp" + str(function.id) + " <!> Pos" + str(function.pos) + ".position.REQUIREMENT(?amountH" + str(function.id) + ");\n"
    tmp += "\t\t\t\t?amountH" + str(function.id) + " = 1;\n"
    tmp += "\t\t\t\thp" + str(function.id) + " EQUALS h" + str(function.id) + ";\n"

    tmp += "\t\t\tr" + str(function.id) + " <!> RoboticProcess.process.Task_manipolazione(?rloc" + str(function.id) + ");\n" 
    tmp += "\t\t\t?rloc" + str(function.id) + " = Pos" + str(function.pos) + ";\n"
    tmp += "\t\t\t\trp" + str(function.id) + " <!> Pos" + str(function.pos) + ".position.REQUIREMENT(?amountR" + str(function.id) + ");\n"
    tmp += "\t\t\t\t?amountR" + str(function.id) + " = 1;\n"
    tmp += "\t\t\t\trp" + str(function.id) + " EQUALS r" + str(function.id) + ";\n"

    return tmp

#funzione che crea la combinazione lineare di operatori
#in base a quanti task con operatore "Indifferente" ci sono
def combLin(n):
	if n==1:
		return [['Human'], ['Robot']]
	else:
		tmp1 = combLin(n-1)
		tmp2 = combLin(n-1)
		for i in range(2**(n-1)):
			tmp1[i].append('Human')
			tmp2[i].append('Robot')
		return tmp1 + tmp2


#########################################################################################
#                   Salvataggio del dominio in un file
#########################################################################################
@app.route('/salva', methods=['POST'])
def salva():
    pos = int(request.form.get('pos_form'))

    #Posizioni
    Positions = "//Enumeration Parameter\n\tPAR_TYPE EnumerationParameterType location = { "
    for i in range(pos):
        Positions += "Pos" + str(i+1) + ", "
    Positions += "base };\n\n"
    Positions += "// position components\n"
    for i in range(pos):
        Positions += "\tCOMPONENT Pos" + str(i+1) + "{FLEXIBLE position(primitive)}: PositionType;\n"
    Positions += "\n"

    #COMP_TYPE AssemblyProcessType
    SV_AssemblyProcess = "\tCOMP_TYPE SingletonStateVariable AssemblyProcessType(Idle(), "
    for i in range(len(lista)):
        if i != len(lista)-1:
            append = lista[i].name + "(), "
        else:
            append = lista[i].name + "())\n\t{\n"
        SV_AssemblyProcess += append
    SV_AssemblyProcess += "\t\tVALUE Idle() [1, +INF]\n\t\tMEETS {\n"
    for task in lista:
        SV_AssemblyProcess += "\t\t\t" + task.name + "();\n"
    SV_AssemblyProcess += "\t\t}\n\n"
    for task in lista:
        SV_AssemblyProcess += "\t\tVALUE " + task.name + "() [1, +INF]\n"
        SV_AssemblyProcess += "\t\tMEETS {\n\t\t\tIdle();\n\t\t}\n\n"
    SV_AssemblyProcess += "\t}\n\n"

    #SYNCHRONIZE Cembre.case_study
    SYN_Cembre = "\tSYNCHRONIZE Cembre.case_study {\n\t\tVALUE Assembly() {\n"
    for element in lista:
        SYN_Cembre += "\t\t\ttask_" + element.name + " <!> AssemblyProcess.tasks." + element.name + "();\n"
        SYN_Cembre += "\t\t\tCONTAINS [0, +INF] [0, +INF] task_" + element.name + ";\n\n"
    for element in vincoli:
        SYN_Cembre += "\t\t\ttask_" + element.t1 + " BEFORE [0, +INF] task_" + element.t2 + ";\n"
    SYN_Cembre += "\t\t}\n\t}\n\n"

    #SYNCHRONIZE AssemblyProcess.tasks
    SYN_Task = "\tSYNCHRONIZE AssemblyProcess.tasks {\n"
    for task in lista:
        indifferenti = []
        SYN_Task += "\n\t\tVALUE " + task.name + "() {\n"
        for function in task.functions:
            if(task.collaboration_type == IND or task.collaboration_type == SYN):
                if(function.assigned_to != "Indifferente"):
                    SYN_Task += aggiungiIndValue(function, function.assigned_to)
                else:
                    indifferenti.append(function)
                    SYN_Task += aggiungiIndValue(function, "Human")
            if(task.collaboration_type == SIM or task.collaboration_type == SUPP):
                SYN_Task += aggiungiSuppValue(function)

        #aggiungo la modalità collaborativa e i vincoli
        SYN_Task += "\n\t\t\tm CollaborationType.modality." + task.collaboration_type + "();\n"
        for i in range(len(task.functions)):
            if(task.collaboration_type == IND):
                SYN_Task += "\t\t\tm CONTAINS [0, +INF] [0, +INF] t" + str(i) + ";\n"
                SYN_Task += "\t\t\tCONTAINS [0, +INF] [0, +INF] t" + str(i) + ";\n"
            if(task.collaboration_type == SYN):
                if(i<len(task.functions)-1):
                    #vincolo BEFORE con Synchronous
                    SYN_Task += "\t\t\tt" + str(i) + " BEFORE [0, +INF] t" + str(i+1) + ";\n"
                SYN_Task += "\t\t\tm CONTAINS [0, +INF] [0, +INF] t" + str(i) + ";\n"
                SYN_Task += "\t\t\tCONTAINS [0, +INF] [0, +INF] t" + str(i) + ";\n"
            if(task.collaboration_type == SIM):
                SYN_Task += "\t\t\tm CONTAINS [0, +INF] [0, +INF] h" + str(i) + ";\n"
                SYN_Task += "\t\t\tm CONTAINS [0, +INF] [0, +INF] r" + str(i) + ";\n"
                SYN_Task += "\t\t\tCONTAINS [0, +INF] [0, +INF] h" + str(i) + ";\n"
                SYN_Task += "\t\t\tCONTAINS [0, +INF] [0, +INF] r" + str(i) + ";\n"
            if(task.collaboration_type == SUPP):
                #Vincolo EQUALS con Supportive
                SYN_Task += "\t\t\th" + str(i) + " EQUALS r" + str(i) + ";\n"
                SYN_Task += "\t\t\tm CONTAINS [0, +INF] [0, +INF] h" + str(i) + ";\n"
                SYN_Task += "\t\t\tm CONTAINS [0, +INF] [0, +INF] r" + str(i) + ";\n"
                SYN_Task += "\t\t\tCONTAINS [0, +INF] [0, +INF] h" + str(i) + ";\n"
                SYN_Task += "\t\t\tCONTAINS [0, +INF] [0, +INF] r" + str(i) + ";\n"
            
        SYN_Task += "\t\t}\n"

        #Se ci sono delle funzioni che possono essere svolte da entrambi gli operatori
        if (len(indifferenti) != 0):
            operatori = combLin(len(indifferenti))
            for i in range(1, len(operatori)):
                #RISCRIVO TUTTA LA FUNZIONE 
                SYN_Task += "\n\t\tVALUE " + task.name + "() {\n"
                for function in task.functions:
                    if(task.collaboration_type == IND or task.collaboration_type == SYN):
                        if(function.assigned_to != "Indifferente"):
                            SYN_Task += aggiungiIndValue(function, function.assigned_to)
                        else:
                            n = indifferenti.index(function)
                            SYN_Task += aggiungiIndValue(function, operatori[i][n])
                    else:
                        SYN_Task += aggiungiSuppValue(function)

                #aggiungo la modalità collaborativa e i vincoli
                SYN_Task += "\n\t\t\tm CollaborationType.modality." + task.collaboration_type + "();\n"
                for i in range(len(task.functions)):
                    if(task.collaboration_type == IND):
                        SYN_Task += "\t\t\tm CONTAINS [0, +INF] [0, +INF] t" + str(i) + ";\n"
                        SYN_Task += "\t\t\tCONTAINS [0, +INF] [0, +INF] t" + str(i) + ";\n"
                    if(task.collaboration_type == SYN):
                        if(i<len(task.functions)-1):
                            #vincolo BEFORE con Synchronous
                            SYN_Task += "\t\t\tt" + str(i) + " BEFORE [0, +INF] t" + str(i+1) + ";\n"
                        SYN_Task += "\t\t\tm CONTAINS [0, +INF] [0, +INF] t" + str(i) + ";\n"
                        SYN_Task += "\t\t\tCONTAINS [0, +INF] [0, +INF] t" + str(i) + ";\n"
                    if(task.collaboration_type == SIM):
                        SYN_Task += "\t\t\tm CONTAINS [0, +INF] [0, +INF] h" + str(i) + ";\n"
                        SYN_Task += "\t\t\tm CONTAINS [0, +INF] [0, +INF] r" + str(i) + ";\n"
                        SYN_Task += "\t\t\tCONTAINS [0, +INF] [0, +INF] h" + str(i) + ";\n"
                        SYN_Task += "\t\t\tCONTAINS [0, +INF] [0, +INF] r" + str(i) + ";\n"
                    if(task.collaboration_type == SUPP):
                        #Vincolo EQUALS con Supportive
                        SYN_Task += "\t\t\th" + str(i) + " EQUALS r" + str(i) + ";\n"
                        SYN_Task += "\t\t\tm CONTAINS [0, +INF] [0, +INF] h" + str(i) + ";\n"
                        SYN_Task += "\t\t\tm CONTAINS [0, +INF] [0, +INF] r" + str(i) + ";\n"
                        SYN_Task += "\t\t\tCONTAINS [0, +INF] [0, +INF] h" + str(i) + ";\n"
                        SYN_Task += "\t\t\tCONTAINS [0, +INF] [0, +INF] r" + str(i) + ";\n"
                    
                SYN_Task += "\t\t}\n"

    #chiudi parentesi della regola di sincronizzazione dell'assembly process                    
    SYN_Task += "\t}\n"


    #salvataggio
    global numeroDominio
    with open("static/base.ddl", "r") as s:
        root = Tk()
        root.withdraw()
        nome = apriFinestra(root)
        root.destroy()
        with open(nome, "w+") as f:
            #scrivo nome dominio e incremento il contatore
            f.write("DOMAIN cembre" + str(numeroDominio) + " {\n")
            numeroDominio += 1

            source = s.readlines()
            f.writelines(source)
            f.write(Positions)
            f.write(SV_AssemblyProcess)
            f.write(SYN_Cembre)
            f.write(SYN_Task)

            #chiusura parentesi generale
            f.write("\n}")
            f.close()
        s.close()

    return render_template("success.html", file=nome)

#finestra per il salvataggio
def apriFinestra(root):
    global numeroDominio
    nome = "Cembre" + str(numeroDominio)
    root.filename = asksaveasfilename(defaultextension=".ddl", title="Save as", initialfile=nome+".ddl")
    return root.filename


#######################################################################
#       Reset della lista se si decide di creare un nuovo dominio
#######################################################################
@app.route('/true', methods=['GET'])
def new():
    global lista
    global vincoli
    lista.clear()
    vincoli.clear()
    return render_template("index.html", lista=lista)
    

if __name__ == '__main__':
    app.run()
