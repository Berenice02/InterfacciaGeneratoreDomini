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
lista = [Task("T1", "Supportive", [Function("0", "Manipolazione", "1", "0", "Human/Robot"), Function("1", "Manipolazione", "2", "0", "Human/Robot")]), Task("T2", "Independent", [Function("0", "Spostamento", "1", "3", "Robot")]), Task("T3", "Lupo", [])]
numeroDominio = 0

#pagina iniziale
@app.route('/')
def hello():
    return render_template("index.html", lista=lista)

#aggiunta di un task al processo
@app.route('/', methods=['POST'])
def aggiungi():
    data = request.json
    print (data)
    functions = []

    #aggiunta di tutte le function a una lista
    for i in range(len(data)-1):
        f_id = data[i]["id"]
        f_type = data[i]["type"]
        f_pos = data[i]["pos"]
        f_pos1 = data[i]["pos1"]
        f_operator = data[i]["operator"]
        func = Function(f_id, f_type, f_pos, f_pos1, f_operator)
        functions.append(func)

    name = data[-1]["taskName"].strip().capitalize()
    collaboration = data[-1]["collab"]
    task = Task(name, collaboration, functions)
    #aggiunta del task alla lista
    lista.append(task)
    return render_template("index.html", lista=lista)


def aggiungiIndValue(op, task, function):
    tmp = "\t\t\tt" + str(function.id) + " <!> " 
    if( function.operator == "Human"):
        tmp += "HumanProcess.process._"
    if( function.operator == "Robot"):
        tmp += "RoboticProcess.process."
    if( function.type == "Manipolazione"):
        tmp += "Task_manipolazione(?loc" + str(id) + ");\n"
        tmp += "\t\t\t?loc" + str(function.id) + " = Pos" + str(function.pos) + ";\n"
        # Se l'operatore è solo robot o solo umano la manipolazione è per forza independent
        tmp += "\t\t\t\tp" + str(function.id) + " <!> Pos" + str(function.pos) + ".position.REQUIREMENT(?amountP" + str(function.id) + ");\n"
        tmp += "\t\t\t\t?amountP" + str(function.id) + " = 2;\n"
        tmp += "\t\t\t\tp" + str(function.id) + " EQUALS t" + str(function.id) + ";\n"
    if( function.type == "Spostamento"):
        tmp += "Task_spostamento(?from" + str(function.id) + "?to" + str(id) + ");\n"
        tmp += "\t\t\t?from" + str(function.id) + " = Pos" + str(function.pos) + ";\n"
        tmp += "\t\t\t?to" + str(function.id) + " = Pos" + str(function.pos1) + ";\n"
        # Se l'operatore è solo robot o solo umano la manipolazione è per forza independent
        tmp += "\t\t\t\ts" + str(function.id) + " <!> Pos" + str(function.pos) + ".position.REQUIREMENT(?amountS" + str(function.id) + ");\n"
        tmp += "\t\t\t\t?amountS" + str(function.id) + " = 2;\n"
        tmp += "\t\t\t\ts" + str(function.id) + " EQUALS t" + str(function.id) + ";\n"
        tmp += "\t\t\t\td" + str(function.id) + " <!> Pos" + str(function.pos) + ".position.REQUIREMENT(?amountD" + str(function.id) + ");\n"
        tmp += "\t\t\t\t?amountD" + str(function.id) + " = 2;\n"
        tmp += "\t\t\t\td" + str(function.id) + " EQUALS t" + str(function.id) + ";\n"
        return tmp



#salvataggio del dominio in un file
@app.route('/salva', methods=['GET', 'POST'])
def salva():
    pos = int(request.form["n_positions"])

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
    for element in lista:
        SV_AssemblyProcess += "\t\t\t" + element.name + "();\n"
    SV_AssemblyProcess += "\t\t}\n\n"
    for element in lista:
        SV_AssemblyProcess += "\t\tVALUE " + element.name + "() [1, +INF]\n"
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
        SYN_Task += "\t\tVALUE " + task.name + "() {\n"
        for function in element.functions:
            if (function.operator == "Human/Robot"):
                print("ok")
            if (function.operator == "Robot"):
                SYN_Task += aggiungiIndValue("Robot", task, function)
            if(function.operator == "Human"):
                SYN_Task += aggiungiIndValue("Human", task, function)
            if(function.operator == "Indifferente"):
                print("ok")

        #aggiungo la modalità collaborativa e i vincoli
        SYN_Task += "\n\t\t\tm CollaborationType.modality." + task.collaboration_type + "();\n"
        for i in range(len(element.functions)):
            SYN_Task += "m CONTAINS [0, +INF] [0, +INF] t" + str(i) + ";\n"
            SYN_Task += "CONTAINS [0, +INF] [0, +INF] t" + str(i) + ";\n"
        SYN_Task += "\t\t}\n"
                        
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
