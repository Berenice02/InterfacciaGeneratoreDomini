// function to execute on page load
$(document).ready(function() {

    var Constraint = class Constraint {
        constructor(id, t1, t2) {
            this.id = id;
            this.t1 = t1;
            this.t2 = t2;
        }
    };

    /**************************************
    *   Disable select options
    ***************************************/
    $("#t1").focus(function () {
        // Store the current value on focus, before it changes
        previous = this.value;
    }).change(function() {
        if (previous !== ""){
            $("#t2").find('option[value=' + previous + ']').removeAttr('disabled');
        }
        $("#t2").find('option[value=' + this.value + ']').attr('disabled', 'disabled');
    });

    $("#t2").focus(function () {
        // Store the current value on focus, before it changes
        previous = this.value;
    }).change(function() {
        if (previous !== ""){
            $("#t1").find('option[value=' + previous + ']').removeAttr('disabled');
        }
        $("#t1").find('option[value=' + this.value + ']').attr('disabled', 'disabled');
    });

    $(".t1").show(function() {
        $(this).siblings(".t2").find('option[value=' + this.value + ']').attr('disabled', 'disabled');
    });

    $(".t2").show(function() {
        $(this).siblings(".t1").find('option[value=' + this.value + ']').attr('disabled', 'disabled');
    });

    /**************************************
    *   Create a constraint
    ***************************************/
   $("#sub").click(function(){
         //take the elements
         var ID = parseInt(sessionStorage.getItem("c_id"));
         var t1 = (document.getElementById("t1").value);
         var t2 = (document.getElementById("t2").value);

         if(t1 === "" || t2 === "") {
           window.alert("Enter all the information about the constraint!");
         }

         else {
            c = new Constraint(ID, t1, t2);

            var tmp = [c, "new"];
            //create the json data
            var js_data = JSON.stringify(tmp);
            $.ajax({                        
                url: '/vincoli',
                type : 'post',
                contentType: 'application/json; charset=utf-8',
                dataType : 'json',
                data : js_data
            }).always(function(){
                location.replace("/vincoli");
            });

           sessionStorage.setItem("c_id", ID+1);
         }
   });

   /**************************************
    *   Remove a constraint
    ***************************************/
   $(".remove").click(function(){

        var id = $(this).siblings(".id").html();
        
        var tmp =[id, "remove"];
        //create the json data
        var js_data = JSON.stringify(tmp);
        $.ajax({                        
            url: '/vincoli',
            type : 'post',
            contentType: 'application/json; charset=utf-8',
            dataType : 'json',
            data : js_data
        }).always(function() {
            location.replace("/vincoli");
        });
    });


    /**************************************
    *   Modify a constraint
    ***************************************/
    $(".t1").focus(function () {
        // Store the current value on focus, before it changes
        previous = this.value;
    }).change(function() {
        var t = $(this).siblings(".t2");
        t.find('option[value=' + previous + ']').removeAttr('disabled');
        t.find('option[value=' + this.value + ']').attr('disabled', 'disabled');
        
        var id = $(this).siblings(".id").html();
        var t2 = t[0].value;

        c = new Constraint(id, this.value, t2);
        
        var tmp =[c, "mod"];
        send(tmp);
    });

    $(".t2").focus(function () {
        // Store the current value on focus, before it changes
        previous = this.value;
    }).change(function() {
        var t = $(this).siblings(".t1");
        t.find('option[value=' + previous + ']').removeAttr('disabled');
        t.find('option[value=' + this.value + ']').attr('disabled', 'disabled');
        
        var id = $(this).siblings(".id").html();
        var t1 = t[0].value;
        c = new Constraint(id, t1, this.value);
        
        var tmp =[c, "mod"];
        send(tmp);
    });

    
    /**************************************
    *   Send the json
    ***************************************/
    function send(tmp) {
        //create the json data
        var js_data = JSON.stringify(tmp);
        $.ajax({                        
            url: '/vincoli',
            type : 'post',
            contentType: 'application/json; charset=utf-8',
            dataType : 'json',
            data : js_data
        });
    }

});