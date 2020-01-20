from flask import Flask, render_template, request, jsonify
import os
app = Flask(__name__)

#classe dei task
class Task:
    def __init__(self, name, description, functions):
        self.name = name
        self.description = description
        self.functions = functions
#e delle funzioni di ogni task
class Function:
    def __init__(self, type, pos, pos1, assigned_to, collaboration_type):
        self.type = type
        self.pos = pos
        self.pos1 = pos1
        self.assigned_to = assigned_to
        self.collaboration_type = collaboration_type


#lista di task
lista = [Task("T1", "Ok", [Function("Manipolazione", "1", "0", "Human/Robot", "Supportive"), Function("Spostamento", "1", "3", "Robot", "Independent")]), Task("T2", "Cosi", []), Task("T3", "Lupo", [])]
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
        f_type = data[i]["type"]
        f_pos = data[i]["pos"]
        f_pos1 = data[i]["pos1"]
        f_operator = data[i]["operator"]
        f_collaboration = data[i]["collab"]
        func = Function(f_type, f_pos, f_pos1, f_operator, f_collaboration)
        functions.append(func)

    name = data[len(data)-1]["taskName"].strip().capitalize()
    description = data[len(data)-1]["descTask"].strip().capitalize()
    task = Task(name, description, functions)
    #aggiunta del task alla lista
    lista.append(task)

    return render_template("index.html", lista=lista)



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
    # SYN_Task = "\tSYNCHRONIZE AssemblyProcess.tasks {\n"
    # for task in lista:
    #     SYN_Task += "\t\tVALUE " + task.name + "() {\n"
    #     for function in element.functions:
    #         SYN_Task += "\t\t\tm CollaborationType.modality." + function.collaboration_type + "();\n"
    #         if (function.human == "manipolazione"):
    #             SYN_Task += "\t\t\tt1 <!> HumanProcess.process._Task_manipolazione(?loc1);\n"
    #             SYN_Task += "\t\t\t?loc1 = " + function.positionH + ";\n"
    #             SYN_Task += "\t\t\t\tb1 <!> " + function.positionH + ".position.REQUIREMENT(?amount1);\n"
    #             if (function.collaboration_type == "Independent" | function.collaboration_type == "Synchronous"):
    #                 SYN_Task += "\t\t\t\t?amount1 = 2;\n"
    #             else:
    #                 SYN_Task += "\t\t\t\t?amount1 = 1;\n"
    #             SYN_Task += "\t\t\tb1 EQUALS t1;\n" 
    #             SYN_Task += "\n\t\t\tm CONTAINS [0, +INF] [0, +INF] t1;\n"
    #             SYN_Task += "\n\t\t\tCONTAINS [0, +INF] [0, +INF] t1;\n"
    #         else:
    #             print("1")
    #         if(function.robot == "manipolazione"):
    #             SYN_Task += "\t\t\tt2 <!> RoboticProcess.process.Task_manipolazione(?loc2);\n"
    #             SYN_Task += "\t\t\t?loc2 = " + function.positionR + ";\n"
    #             SYN_Task += "\t\t\t\tb2 <!> " + function.positionR + ".position.REQUIREMENT(?amount2);\n"
    #             if (function.collaboration_type == "Independent" | function.collaboration_type == "Synchronous"):
    #                 SYN_Task += "\t\t\t\t?amount2 = 2;\n"
    #             else:
    #                 SYN_Task += "\t\t\t\t?amount2 = 1;\n"
    #             SYN_Task += "\t\t\tb2 EQUALS t2;\n" 
    #             SYN_Task += "\n\t\t\tm CONTAINS [0, +INF] [0, +INF] t2;\n"
    #             SYN_Task += "\n\t\t\tCONTAINS [0, +INF] [0, +INF] t2;\n"
    #         else:
    #             print("2")
    #         if(function.collaboration_type == "Synchronous (prima umano)"):
    #             SYN_Task += "\n\t\t\tt1 BEFORE [0, +INF] t2;\n"
    #         if(function.collaboration_type == "Synchronous (prima robot)"):
    #             SYN_Task += "\n\t\t\tt2 BEFORE [0, +INF] t1;\n"
    #         if(function.collaboration_type == "Supportive"):
    #             SYN_Task += "\n\t\t\tt1 EQUALS t2;\n"


    #     SYN_Task += "\t\t}\n"
    # SYN_Task += "\t}\n"



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
    #lista.clear()

if __name__ == '__main__':
    app.run()
