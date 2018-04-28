var inputName = document.getElementById("usertype");


var userType;
function whichFormClicked(){
	if (document.getElementById('customerRegister').checked == true)
	{
		userType = "customer";
	} 
	else if (document.getElementById('bookingAgentRegister').checked == true) 
	{
		userType = "booking_agent";
	} 
	else if (document.getElementById('airlineStaffRegister').checked == true) {
		userType = "airline_staff";
	}

	inputName.value = userType;
}