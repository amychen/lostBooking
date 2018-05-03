var num_of_rows = document.getElementById("flights").rows.length;
for (var i = 0; i < num_of_rows - 1; i++){
    var airline_name = document.getElementsByClassName("airline_name")[i].innerHTML;
    var flight_num = document.getElementsByClassName("flight_num")[i].innerHTML;
    var purchaseButton = document.getElementsByClassName("purchaseButton")[i];

    purchaseButton.id = airline_name + "_" + flight_num;
}

function purchaseTicket(e){
    var modal = document.getElementById("statusBox");
    var closeButton = document.getElementById("close");
    var header = document.getElementById("header");

    purchaseButton = document.getElementById(e.id)
    var name_num_stat = purchaseButton.id.split("_");
    modal.style.display = "block";
    header.innerHTML = "You are purchasing ticket for <br><span>" + name_num_stat[0] + "</span><br>on flight number<br><span>" 
                        + name_num_stat[1] + "</span><br>";

    closeButton.addEventListener("click", function(e){
        modal.style.display = "none";
    });

    var purchaseBtn = document.getElementById("purchaseBtn")
    var air_name = document.getElementById("air_name")
    var fl_num = document.getElementById("fl_num")

    purchaseBtn.addEventListener("click", function(e) {
        air_name.value = name_num_stat[0];
        fl_num.value = name_num_stat[1];
    })
}