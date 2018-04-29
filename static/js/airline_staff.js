var num_of_rows = document.getElementById("flights").rows.length;
for (var i = 0; i < num_of_rows - 1; i++){
    var airline_name = document.getElementsByClassName("airline_name")[i].innerHTML;
    var flight_num = document.getElementsByClassName("flight_num")[i].innerHTML;
    var statusButton = document.getElementsByClassName("changeStatusButton")[i];
    var flightStatus = document.getElementsByClassName("flight_status")[i].innerText;

    statusButton.id = airline_name + "_" + flight_num + "_" + flightStatus;
}

function changeStatus(e){
    var modal = document.getElementById("statusBox");
    var closeButton = document.getElementById("close");
    var header = document.getElementById("header");

    statusButton = document.getElementById(e.id)
    var name_num_stat = statusButton.id.split("_");
    modal.style.display = "block";
    header.innerHTML = "You are changing the flight status of " + name_num_stat[0] + " " + name_num_stat[1] + ".<br>";
    header.innerHTML += "The current status is <br>";
    header.innerHTML += "<span>" + name_num_stat[2] + "</span><br>";

    closeButton.addEventListener("click", function(e){
        modal.style.display = "none";
    });

    var updateBtn = document.getElementById("updateBtn")
    var newStatus = document.getElementById("newStatus")
    var a_name = document.getElementById("a_name")
    var f_num = document.getElementById("f_num")
    var options = document.getElementById("selectOption");

    updateBtn.addEventListener("click", function(e) {
        newStatus.value = options.value;
        a_name.value = name_num_stat[0];
        f_num.value = name_num_stat[1];
    })
}
// function showFlightForm(){
//     var newFlight = document.getElementById("add_flight_form");
//     if (newFlight.style.display === "none"){
//         newFlight.style.display = "block";
//     } else {
//         newFlight.style.display = "none";
//     }
// }

// function showCustomer(){
//     var newAirplane = document.getElementById("add_plane_form");
//     if (newAirplane.style.display === "none"){
//         newAirplane.style.display = "block";
//     } else {
//         newAirplane.style.display = "none";
//     }
// }

// function showRevenue(){
//     var newAirplane = document.getElementById("add_plane_form");
//     if (newAirplane.style.display === "none"){
//         newAirplane.style.display = "block";
//     } else {
//         newAirplane.style.display = "none";
//     }
// }

// function showReport(){
//     var newAirplane = document.getElementById("add_plane_form");
//     if (newAirplane.style.display === "none"){
//         newAirplane.style.display = "block";
//     } else {
//         newAirplane.style.display = "none";
//     }
// }

// function showDestination(){
//     var newAirplane = document.getElementById("add_plane_form");
//     if (newAirplane.style.display === "none"){
//         newAirplane.style.display = "block";
//     } else {
//         newAirplane.style.display = "none";
//     }
// }