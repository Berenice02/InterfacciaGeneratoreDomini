/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

// function to execute on page load
$(document).ready(function() {
    
    // show only process names and descriptions (task names) initially
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
        // display taks description
        $(this).siblings(".task-description").fadeToggle("fast");
    });

    /**********************************************
    *   Display task (with modify's constraints)
    ***********************************************/
   $(".select-type").show(function() {
        var position = $(this).parent().siblings(".position");
        var modality = $(this).parent().siblings(".collaboration-type").children(".select-collaboration");
        var operator = $(this).parent().siblings(".assigned-to").children(".select-operator");
        if (this.value === "Manipolazione") {
            position.children(".handle-pos").show();
            position.children(".first-pos").hide();
            position.children(".second-pos").hide();

            modality.prop("disabled", false);
        }
        if (this.value === "Spostamento") {
            position.children(".handle-pos").hide();
            position.children(".first-pos").show();
            position.children(".second-pos").show();

            modality.prop("disabled", true);
        }
    });
    
   $(".select-type").change(function() {
        var position = $(this).parent().siblings(".position");
        var modality = $(this).parent().siblings(".collaboration-type").children(".select-collaboration");
        var operator = $(this).parent().siblings(".assigned-to").children(".select-operator");
        if (this.value === "Manipolazione") {
            position.children(".handle-pos").show();
            position.children(".first-pos").hide();
            position.children(".second-pos").hide();

            // restore original collaboration-type
            modality.prop("selectedIndex", 0);
            modality.prop("disabled", false);

            //QUESTA NON FUNZIONA QUANDO INDEPENDENT
            //E' LA VARIABILE FLASK
            if (modality.value === "Independent") {
                //restore original operator
                operator.prop("selectedIndex", 0);
                if(operator.value === "Human/Robot"){
                    // set robot as operator
                    operator.prop("selectedIndex", 1);
                }
                operator.prop("disabled", false);
            }
            else {
                // set Human/Robot as default operator
                operator.prop("selectedIndex", 4);
                operator.prop("disabled", true);
            }
        }
        if (this.value === "Spostamento") {
            position.children(".handle-pos").hide();
            position.children(".first-pos").show();
            position.children(".second-pos").show();
            
            // set Independent as default collaboration-type
            modality.prop("selectedIndex", 4);
            modality.prop("disabled", true);

            // set Robot as operator
            operator.prop("selectedIndex", 1);
            operator.prop("disabled", false);
        }
    });

    $(".select-collaboration").show(function(){
        var operator = $(this).parent().siblings(".assigned-to").children(".select-operator");
        if (this.value === "Independent") {
            operator.prop("disabled", false);
        }
        else {
            operator.prop("disabled", true);
        }
    });
        //QUESTA NON FUNZIONA QUANDO INDEPENDENT
        //E' LA VARIABILE FLASK
    $(".select-collaboration").change(function(){
        var operator = $(this).parent().siblings(".assigned-to").children(".select-operator");
        if (this.value === "Independent") {
            //restore original operator
            operator.prop("selectedIndex", 0);
            if($(".select-operator").value === "Human/Robot"){
                // set robot as operator
                operator.prop("selectedIndex", 1);
            }
            console.log($(".select-operator").value);
            operator.prop("disabled", false);
        }
        else {
            // set Human/Robot as default operator
            operator.prop("selectedIndex", 4);
            operator.prop("disabled", true);
        }
    });

    /**************************************
    *   Change background-color
    ***************************************/
    $(".select-operator").show(function() {
        // check selected operator
        if (this.value === "Human") {
            $(this).parents(".function").css("background-color", "lightblue");
        }
        if (this.value === "Robot") {
            $(this).parents(".function").css("background-color", "lightgreen");
        }
        if (this.value === "Human/Robot") {
            $(this).parents(".function").css("background-color","lemonchiffon");
        }
        if (this.value === "Indifferente") {
         $(this).parents(".function").css("background-color","palevioletred");
         }
     });
     $(".select-operator").change(function() {
        // check selected option
        if (this.value === "Human") {
            // set color
            $(this).parents(".function").css("background-color", "lightblue");
        }
        if (this.value === "Robot") {
            // set color
            $(this).parents(".function").css("background-color", "lightgreen");
        }
        if (this.value === "Human/Robot") {
            // set color
            $(this).parents(".function").css("background-color","lemonchiffon");
        }
        if (this.value === "Indifferente") {
         $(this).parents(".function").css("background-color","palevioletred");
        }
     });


    /**************************************
    *   Display new task form or popup
    ***************************************/
    $(".new-task").click(function() {
        if(nPos === undefined) {
            window.alert("Inserisci il numero di posizioni!");
        }
        else {
            $(this).siblings(".task").fadeToggle("fast");
        }
    });


    /*******************************************
    *   Display/Hide input fields of each task
    ********************************************/
    $(".move").hide();
    $(".indep").hide();
    $("#f-new-type").show(function(){
        if (this.value === "Spostamento") {
            $(".handle").hide();
            $(".move").show();
        }
        if(this.value === "Manipolazione") {
            $(".move").hide();
            $(".handle").show();
        }
    });
    $("#f-new-type").change(function(){
        if (this.value === "Spostamento") {
            $(".handle").hide();
            $(".move").show();
        }
        if(this.value === "Manipolazione") {
            $(".move").hide();
            $(".handle").show();
        }
    });
    $("#new-collab").show(function(){
        if(this.value === "Independent") {
            $(".indep").show();
        }
        else {
            $(".indep").hide();
        }
    });
    $("#new-collab").change(function(){
        if(this.value === "Independent") {
            $(".indep").show();
        }
        else {
            $(".indep").hide();
        }
    });

    var lista = [];

    var SubTask = class SubTask {
        constructor(id, type, pos, pos1, operator, collab) {
            this.id = id;
            this.type = type;
            this.pos = pos;
            this.pos1 = pos1;
            this.operator = operator;
            this.collab = collab;
        }
    };

    /**************************************
    *   Create a subtask
    ***************************************/
    count = 0;
    $("#func").click(function(){
          //take the elements
          var type = (document.getElementById("f-new-type").value);
          var pos = (document.getElementById("pos").value);
          if (type === "Spostamento") {
            var pos1 = (document.getElementById("pos1").value);
            var collab = "Independent";
            var operator = (document.getElementById("new-operator").value);
          }
          else {
            var pos1 = 0
            var collab = (document.getElementById("new-collab").value);
            if (collab === "Independent") {
                var operator = (document.getElementById("new-operator").value);
            }
            else {
                var operator = "Human/Robot";
            }
          }

          var tmp = new SubTask(count, type, pos, pos1, operator, collab);
          lista.push(tmp);

          //display the new subtask
          $("#results").append("<p>Sub-task di tipo: " + type + pos + pos1 + " Assegnato a: " + operator +" Con modalità: " +collab + "</p>");

          //reset the values of subtask form
          $("#f-new-type").prop('selectedIndex', 0);
          $("#new-operator").prop('selectedIndex', 1);
          $("#new-collab").prop('selectedIndex', 1);
          $(".handle").show();
          $(".move").hide();
          $(".indep").hide();

          count += 1;
    });


    /**************************************
    *   Submit a task
    ***************************************/
    $("#sub").click(function(){
        //take the elements
        var nomeTask = document.getElementById("new-name").value;
        var descTask = document.getElementById("new-description").value;
        lista.push({"taskName": nomeTask, "descTask": descTask});
        //create the json data
        var js_data = JSON.stringify(lista);
          $.ajax({                        
              url: '/',
              type : 'post',
              contentType: 'application/json; charset=utf-8',
              dataType : 'json',
              data : js_data
          }).always(function(){
            location.reload(true);
         });
    });

    var nPos;
    //change #positions
    $("#n_positions").change(function() {
        nPos = this.value;
        console.log(nPos);

        //add options to select-position
        for (var i=0; i<nPos; i++){
            $(".pos").append("<option>" + (i+1).toString() + "</option>");
        }
    });

});
