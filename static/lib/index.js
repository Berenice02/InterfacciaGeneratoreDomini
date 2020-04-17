/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

// function to execute on page load
$(document).ready(function() {
    const Manipolazione = "Manipolazione";
    const Spostamento = "Spostamento";

    const Human = "Human";
    const Robot = "Robot";
    const H_R = "Human/Robot";
    const Indiff = "Indifferente";

    const Ind = "Independent";
    const Syn = "Synchronous";
    const Sim = "Simultaneous";
    const Supp = "Supportive";

    var lista = [];

    var SubTask = class SubTask {
        constructor(id, type, pos, pos1, operator) {
            this.id = id;
            this.type = type;
            this.pos = pos;
            this.pos1 = pos1;
            this.operator = operator;
        }
    };
    
    // show only task names and collaboration modality initially
    $(".task-description").hide();
    $(".task").hide();

    /**************************************
    *   Set onclick actions
    ***************************************/
    $(".process-name").click(function() {
       // display an initial part of process description
       $(this).siblings(".process-description").fadeToggle("fast");
       // hide process description details
       $(this).parent(".process").find(".task-description").hide();
    });
    $(".task-name").click(function() {
        // display task description
        $(this).siblings(".task-description").fadeToggle("fast");
    });

    /**********************************************
    *   Display task (with modify's constraints)
    ***********************************************/
    $(".collaboration-type").show(function() {
        var sub = $(this).parent().siblings(".task-description").children(".function");
        if($(this).html()=== Sim || $(this).html() === Supp) {
            sub.children(".type").children(".select-type").prop("disabled", true);
            sub.children(".assigned-to").children(".select-operator").prop("disabled", true);
        }

        if($(this).html()=== Ind || $(this).html() === Syn) {
            sub.children(".type").children(".select-type").prop("disabled", false);
            sub.children(".assigned-to").children(".select-operator").prop("disabled", false);
        }
    });

   $(".select-type").show(function() {
        var position = $(this).parent().siblings(".position");
        if (this.value === Manipolazione) {
            position.children(".handle-pos").show();
            position.children(".first-pos").hide();
            position.children(".second-pos").hide();
       }
        if (this.value === Spostamento) {
            position.children(".handle-pos").hide();
            position.children(".first-pos").show();
            position.children(".second-pos").show();
        }
    });
    
   
    /********************************************
     *  Modify a task
     ********************************************/
    //Change Manipolazione/Spostamento
    $(".select-type").change(function() {
        var position = $(this).parent().siblings(".position");
        if (this.value === Manipolazione) {
            position.children(".handle-pos").show();
            position.children(".first-pos").hide();
            position.children(".second-pos").hide();
        }

        if (this.value === Spostamento) {
            position.children(".handle-pos").hide();
            position.children(".first-pos").show();
            position.children(".second-pos").show();
        }

        var id = $(this).parent().siblings(".id").html();
        var pos = position.children(".p")[0].value;
        if(this.value === Manipolazione) {
            var pos1 = 0
        }
        if(this.value === Spostamento) {
            var pos1 = position.children(".p1")[0].value;
        }
        var operator = $(this).parent().siblings(".assigned-to").children(".select-operator")[0].value;

        var nomeTask = $(this).parent().parent().parent().siblings(".task-name").children(".el-name").html();
        var subtmp = new SubTask(id, this.value, pos, pos1, operator);

        var tmp =[nomeTask, subtmp, "mod"];
        //create the json data
        var js_data = JSON.stringify(tmp);
        $.ajax({                        
            url: '/',
            type : 'post',
            contentType: 'application/json; charset=utf-8',
            dataType : 'json',
            data : js_data
        });
    });

    //Change first position
    $(".p").change(function() {
        var id = $(this).parent().siblings(".id").html();
        var type = $(this).parent().siblings(".type").children(".select-type")[0].value;
        if(type === Manipolazione) {
            var pos1 = 0
        }
        if(type === Spostamento) {
            var pos1 = $(this).siblings(".p1")[0].value;
        }
        var operator = $(this).parent().siblings(".assigned-to").children(".select-operator")[0].value;

        var nomeTask = $(this).parent().parent().parent().siblings(".task-name").children(".el-name").html();
        var subtmp = new SubTask(id, type, this.value, pos1, operator);

        var tmp =[nomeTask, subtmp, "mod"];
        //create the json data
        var js_data = JSON.stringify(tmp);
        $.ajax({                        
            url: '/',
            type : 'post',
            contentType: 'application/json; charset=utf-8',
            dataType : 'json',
            data : js_data
        });
    });

    //Change second position
    $(".p1").change(function() {
        var id = $(this).parent().siblings(".id").html();
        var type = $(this).parent().siblings(".type").children(".select-type")[0].value;
        if(type === Manipolazione) {
            var pos = 0
        }
        if(type === Spostamento) {
            var pos = $(this).siblings(".p")[0].value;
        }
        var operator = $(this).parent().siblings(".assigned-to").children(".select-operator")[0].value;

        var nomeTask = $(this).parent().parent().parent().siblings(".task-name").children(".el-name").html();
        var subtmp = new SubTask(id, type, pos, this.value, operator);
        var tmp =[nomeTask, subtmp, "mod"];
        //create the json data
        var js_data = JSON.stringify(tmp);
        $.ajax({                        
            url: '/',
            type : 'post',
            contentType: 'application/json; charset=utf-8',
            dataType : 'json',
            data : js_data
        });
    });

    //Change operator
    $(".select-operator").change(function() {
        var position = $(this).parent().siblings(".position");

        var id = $(this).parent().siblings(".id").html();
        var type = $(this).parent().siblings(".type").children(".select-type")[0].value;
        var pos = position.children(".p")[0].value;
        if(type === Manipolazione) {
            var pos1 = 0
        }
        if(type === Spostamento) {
            var pos1 = position.children(".p1")[0].value;
        }
        
        var nomeTask = $(this).parent().parent().parent().siblings(".task-name").children(".el-name").html();
        var subtmp = new SubTask(id, type, pos, pos1, this.value);

        var tmp =[nomeTask, subtmp, "mod"];
        //create the json data
        var js_data = JSON.stringify(tmp);
        $.ajax({                        
            url: '/',
            type : 'post',
            contentType: 'application/json; charset=utf-8',
            dataType : 'json',
            data : js_data
        });
    });

    /**************************************
    *   Remove Subtask
    ***************************************/
    $(".removeF").click(function() {
        var id = $(this).siblings(".id").html();
        
        var nomeTask = $(this).parent().parent().siblings(".task-name").children(".el-name").html();

        var tmp =[nomeTask, id, "removeF"];
        //create the json data
        var js_data = JSON.stringify(tmp);
        $.ajax({                        
            url: '/',
            type : 'post',
            contentType: 'application/json; charset=utf-8',
            dataType : 'json',
            data : js_data
        }).always(function() {
            location.replace("/");
        });
    });

    /**************************************
    *   Remove Task
    ***************************************/
   $(".removeT").click(function() {

    var nomeTask = $(this).siblings(".el-name").html();
    
    var tmp =[nomeTask, "removeT"];
    //create the json data
    var js_data = JSON.stringify(tmp);
    $.ajax({                        
        url: '/',
        type : 'post',
        contentType: 'application/json; charset=utf-8',
        dataType : 'json',
        data : js_data
    }).always(function() {
        location.replace("/");
    });
});

    /**************************************
    *   Change background-color
    ***************************************/
    $(".select-operator").show(function() {
        // check selected operator
        if (this.value === Human) {
            $(this).parents(".function").css("background-color", "lightblue");
        }
        if (this.value === Robot) {
            $(this).parents(".function").css("background-color", "lightgreen");
        }
        if (this.value === H_R) {
            $(this).parents(".function").css("background-color","lemonchiffon");
        }
        if (this.value === Indiff) {
         $(this).parents(".function").css("background-color","palevioletred");
         }
     });
     $(".select-operator").change(function() {
        // check selected option
        if (this.value === Human) {
            // set color
            $(this).parents(".function").css("background-color", "lightblue");
        }
        if (this.value === Robot) {
            // set color
            $(this).parents(".function").css("background-color", "lightgreen");
        }
        if (this.value === H_R) {
            // set color
            $(this).parents(".function").css("background-color","lemonchiffon");
        }
        if (this.value === Indiff) {
         $(this).parents(".function").css("background-color","palevioletred");
        }
     });


    /**************************************
    *   Display new task form or popup
    ***************************************/
    $(".new-task").click(function() {
        if(sessionStorage.getItem("nPos") === null) {
            window.alert("Inserisci il numero di posizioni!");
        }
        else {
            $(this).siblings(".task").fadeToggle("fast");

            if($("#new-collaboration")[0].value == ""){
                $(".sub-task-form").hide();
            }
            else {
                $(".sub-task-form").show();
            }
            
        }
    });


    /*******************************************
    *   Display/Hide input fields of each task
    ********************************************/
    $("#new-collaboration").change(function(){
        $(".sub-task-form").show();
        if(this.value == Ind || this.value == Syn){
            $("#f-new-type").prop("disabled", false);
            $("#new-operator").prop("selectedIndex", 0);
            $("#new-operator").prop("disabled", false);            
        }
        
        // Simultaneous or Supportive modality
        if(this.value == Sim || this.value == Supp){
            // set Manipulation as default type
            $("#f-new-type").prop("selectedIndex", 1);
            $("#f-new-type").prop("disabled", true);

            $(".move").hide();
            $(".handle").show();

            // set Human/Robot as default operator
            $("#new-operator").prop("selectedIndex", 4);
            $("#new-operator").prop("disabled", true);
        }
    });


    $(".move").hide();
    $("#f-new-type").show(function(){
        if (this.value === Spostamento) {
            $(".handle").hide();
            $(".move").show();
        }
        if(this.value === Manipolazione) {
            $(".move").hide();
            $(".handle").show();
        }
    });
    $("#f-new-type").change(function(){
        if (this.value === Spostamento) {
            $(".handle").hide();
            $(".move").show();
        }
        if(this.value === Manipolazione) {
            $(".move").hide();
            $(".handle").show();
        }
    });

    /**************************************
    *   Create a subtask
    ***************************************/
    funcID = 0;
    $("#func").click(function(){
          //take the elements
          var type = (document.getElementById("f-new-type").value);
          var pos = (document.getElementById("pos").value);
          var operator = (document.getElementById("new-operator").value);
          if (type === Spostamento) {
            var pos1 = (document.getElementById("pos1").value);
          }
          if (type === Manipolazione) {
            var pos1 = 0
          }

          if(type === "" || pos === "" || pos1 === "" || operator === "") {
            window.alert("Inserisci tutti i dati del sub-task");
          }

          else {
            var tmp = new SubTask(funcID, type, pos, pos1, operator);
            lista.push(tmp);

            //display the new subtask
            var res = ("<p>Sub-task di tipo: " + type);
            if (type === Manipolazione){
                res += (" In posizione: " + pos);
            }
            if (type === Spostamento) {
                res += (" Dalla posizione " + pos);
                res += (" alla " + pos1);
            }
            res += (" Assegnato a: " + operator + "</p>");
            $("#results").append(res);
            
            funcID += 1;

            //block the number of positions and the collaboration modality
            $("#n_positions").prop("disabled", true); 
            $("#new-collaboration").prop("disabled", true);
          }
    });

    /**************************************
    *   Submit a task
    ***************************************/
    $("#sub").click(function(){
        //take the elements
        var nomeTask = document.getElementById("new-name").value;
        var collab = document.getElementById("new-collaboration").value;
        if (nomeTask === "" || collab === "" || lista.length<=0) {
            window.alert("Inserisci tutti i dati del task");
        }

        else {
            sessionStorage.removeItem("new");
            lista.push({"taskName": nomeTask, "collab": collab});
            lista.push("new")
            //create the json data
            var js_data = JSON.stringify(lista);
            $.ajax({                        
                url: '/',
                type : 'post',
                contentType: 'application/json; charset=utf-8',
                dataType : 'json',
                data : js_data
            }).always(function(){
                location.replace("/");
            });
        }
    });

    $("#n_positions").show(function() {
        if ( sessionStorage.getItem("nPos") === null ) {
            $("#n_positions").prop("disabled", false);
        }

        else if( sessionStorage.getItem("new") === "false" ) {
            $("#n_positions").prop("disabled", true);
            this.value = sessionStorage.getItem("nPos");

            //add options to select-position
            addPositions();
        }

        else {
            $("#n_positions").prop("disabled", true);
            this.value = sessionStorage.getItem("nPos");

            //add options to select-position
            addPositions();
        }
    });
    //change #positions
    $("#n_positions").change(function() {
        sessionStorage.setItem("nPos", this.value);

        //add options to select-position
        addPositions();
    });

    function addPositions () {
        $(".pos").find("option:gt(0)").remove();
        for (var i=0; i<sessionStorage.getItem("nPos"); i++){
            $(".pos").append("<option>" + (i+1).toString() + "</option>");
        }
    }

    sessionStorage.setItem("c_id", 0);
});
