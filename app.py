from flask import Flask, render_template, request, jsonify
import os
app = Flask(__name__)

#classe dei task
class Task:
    def __init__(self, name, collaboration_type, functions):
        self.name = name
        self.collaboration_type = collaboration_type
        self.functions = functions
#e delle funzioni di ogni task
class Function:
    def __init__(self, id, type, pos, pos1, assigned_to):
        self.id = id
        self.type = type
        self.pos = pos
        self.pos1 = pos1
        self.assigned_to = assigned_to

#lista di task
lista = [Task("T1", "Supportive", [Function("0", "Manipolazione", "1", "0", "Human/Robot"), Function("1", "Manipolazione", "2", "0", "Human/Robot")]), Task("T2", "Independent", [Function("0", "Spostamento", "1", "3", "Indifferente")])]
numeroDominio = 0

#pagina iniziale
@app.route('/')
def hello():
    return render_template("index.html", lista=lista)

#reset della lista se si decide di creare un nuovo dominio
@app.route('/true', methods=['GET'])
def new():
    global lista
    lista.clear()
    return render_template("index.html", lista=lista)

#aggiunta di un task al processo
@app.route('/', methods=['POST'])
def aggiungi():
    data = request.json
    functions = []

    if(data[-1] == "new"):
        #aggiunta di tutte le function a una lista
        for i in range(len(data)-2):
            f_id = data[i]["id"]
            f_type = data[i]["type"]
            f_pos = data[i]["pos"]
            f_pos1 = data[i]["pos1"]
            f_operator = data[i]["operator"]
            func = Function(f_id, f_type, f_pos, f_pos1, f_operator)
            functions.append(func)

        name = data[-2]["taskName"].strip().capitalize()
        collaboration = data[-2]["collab"]
        task = Task(name, collaboration, functions)
        #aggiunta del task alla lista
        lista.append(task)
    if(data[-1] == "remove"):
        print(1)
    if(data[-1] == "mod"):
        func = data[1][0]
        for element in lista:
            if element.name == data[0]:

                f_id = int(func["id"])
                f_type = func["type"]
                f_pos = func["pos"]
                f_pos1 = func["pos1"]
                f_operator = func["operator"]
                function = Function(f_id, f_type, f_pos, f_pos1, f_operator)

                print(element.functions[f_id].pos)
                element.functions[f_id] = function
                print(element.functions[f_id].pos)
    return render_template("index.html", lista=lista)


#funzione che aggiunge un task se la modalità è Independent o Synchronous
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

#salvataggio del dominio in un file
@app.route('/salva', methods=['POST'])
def salva():
    pos = int(request.form.get('pos_form'))

    #Posizioni
    Positions = "//Enumeration Parameter\n\tPAR_TYPE EnumerationParameterType location = { "
    for i in range(pos):
        Positions += "Pos" + str(i) + ", "
    Positions += "base };\n\n"
    Positions += "// position components\n"
    for i in range(pos):
        Positions += "\tCOMPONENT Pos" + str(i) + "{FLEXIBLE position(primitive)}: PositionType;\n"
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
    for i in range(len(lista)):
        SYN_Cembre += "\t\t\ttask" + str(i) + " <!> AssemblyProcess.tasks." + lista[i].name + "();\n"
        SYN_Cembre += "\t\t\tCONTAINS [0, +INF] [0, +INF] task" + str(i) + ";\n\n"
    for i in range(len(lista)-1):
        SYN_Cembre += "\t\t\ttask" + str(i) + " BEFORE [0, +INF] task" + str(i+1) + ";\n"
    SYN_Cembre += "\t\t}\n\t}\n\n"

    #SYNCHRONIZE AssemblyProcess.tasks
    SYN_Task = "\tSYNCHRONIZE AssemblyProcess.tasks {\n"
    for task in lista:
        indifferenti = []
        SYN_Task += "\n\t\tVALUE " + task.name + "() {\n"
        for function in task.functions:
            if(task.collaboration_type == "Independent" or task.collaboration_type == "Synchronous"):
                if(function.assigned_to != "Indifferente"):
                    SYN_Task += aggiungiIndValue(function, function.assigned_to)
                else:
                    indifferenti.append(function)
                    SYN_Task += aggiungiIndValue(function, "Human")
            else:
                SYN_Task += aggiungiSuppValue(function)

        #aggiungo la modalità collaborativa e i vincoli
        SYN_Task += "\n\t\t\tm CollaborationType.modality." + task.collaboration_type + "();\n"
        for i in range(len(task.functions)):
            if(task.collaboration_type == "Independent"):
                SYN_Task += "\t\t\tm CONTAINS [0, +INF] [0, +INF] t" + str(i) + ";\n"
                SYN_Task += "\t\t\tCONTAINS [0, +INF] [0, +INF] t" + str(i) + ";\n"
            if(task.collaboration_type == "Synchronous"):
                if(i<len(task.functions)-1):
                    #vincolo BEFORE con Synchronous
                    SYN_Task += "\t\t\tt" + str(i) + " BEFORE [0, +INF] t" + str(i+1) + ";\n"
                SYN_Task += "\t\t\tm CONTAINS [0, +INF] [0, +INF] t" + str(i) + ";\n"
                SYN_Task += "\t\t\tCONTAINS [0, +INF] [0, +INF] t" + str(i) + ";\n"
            if(task.collaboration_type == "Simultaneous"):
                SYN_Task += "\t\t\tm CONTAINS [0, +INF] [0, +INF] h" + str(i) + ";\n"
                SYN_Task += "\t\t\tm CONTAINS [0, +INF] [0, +INF] r" + str(i) + ";\n"
                SYN_Task += "\t\t\tCONTAINS [0, +INF] [0, +INF] h" + str(i) + ";\n"
                SYN_Task += "\t\t\tCONTAINS [0, +INF] [0, +INF] r" + str(i) + ";\n"
            if(task.collaboration_type == "Supportive"):
                #Vincolo EQUALS con Supportive
                SYN_Task += "\t\t\th" + str(i) + " EQUALS r" + str(i) + ";\n"
                SYN_Task += "\t\t\tm CONTAINS [0, +INF] [0, +INF] h" + str(i) + ";\n"
                SYN_Task += "\t\t\tm CONTAINS [0, +INF] [0, +INF] r" + str(i) + ";\n"
                SYN_Task += "\t\t\tCONTAINS [0, +INF] [0, +INF] h" + str(i) + ";\n"
                SYN_Task += "\t\t\tCONTAINS [0, +INF] [0, +INF] r" + str(i) + ";\n"
            
        SYN_Task += "\t\t}\n"

        #Se ci sono delle funzioni che possono essere svolte da entrambi gli operatori
        if (len(indifferenti) != 0):
            print(len(indifferenti))
            print(indifferenti)
            operatori = combLin(len(indifferenti))
            print(operatori)
            for i in range(1, len(operatori)):
                #RISCRIVO TUTTA LA FUNZIONE 
                SYN_Task += "\n\t\tVALUE " + task.name + "() {\n"
                for function in task.functions:
                    if(task.collaboration_type == "Independent" or task.collaboration_type == "Synchronous"):
                        if(function.assigned_to != "Indifferente"):
                            SYN_Task += aggiungiIndValue(function, function.assigned_to)
                        else:
                            n = indifferenti.index(function)
                            print(n)
                            SYN_Task += aggiungiIndValue(function, operatori[i][n])
                            print(operatori[i][n])
                    else:
                        SYN_Task += aggiungiSuppValue(function)

                #aggiungo la modalità collaborativa e i vincoli
                SYN_Task += "\n\t\t\tm CollaborationType.modality." + task.collaboration_type + "();\n"
                for i in range(len(task.functions)):
                    if(task.collaboration_type == "Independent"):
                        SYN_Task += "\t\t\tm CONTAINS [0, +INF] [0, +INF] t" + str(i) + ";\n"
                        SYN_Task += "\t\t\tCONTAINS [0, +INF] [0, +INF] t" + str(i) + ";\n"
                    if(task.collaboration_type == "Synchronous"):
                        if(i<len(task.functions)-1):
                            #vincolo BEFORE con Synchronous
                            SYN_Task += "\t\t\tt" + str(i) + " BEFORE [0, +INF] t" + str(i+1) + ";\n"
                        SYN_Task += "\t\t\tm CONTAINS [0, +INF] [0, +INF] t" + str(i) + ";\n"
                        SYN_Task += "\t\t\tCONTAINS [0, +INF] [0, +INF] t" + str(i) + ";\n"
                    if(task.collaboration_type == "Simultaneous"):
                        SYN_Task += "\t\t\tm CONTAINS [0, +INF] [0, +INF] h" + str(i) + ";\n"
                        SYN_Task += "\t\t\tm CONTAINS [0, +INF] [0, +INF] r" + str(i) + ";\n"
                        SYN_Task += "\t\t\tCONTAINS [0, +INF] [0, +INF] h" + str(i) + ";\n"
                        SYN_Task += "\t\t\tCONTAINS [0, +INF] [0, +INF] r" + str(i) + ";\n"
                    if(task.collaboration_type == "Supportive"):
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
        with open("dati.ddl", "w+") as f:
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
    
    tmp = "Cembre" + str(numeroDominio-1) + SV_AssemblyProcess
    return render_template("success.html", file=tmp)

    #reinizializzazione della lista per il nuovo dominio
    #session.clear()
    #lista.clear()

if __name__ == '__main__':
    app.run()
