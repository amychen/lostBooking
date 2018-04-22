window.onload = function(){
	var d = new Date();
	var month_name = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 
						'August', 'September', 'October', 'November', 'December'];
	var month = d.getMonth();
	var day = d.getDay();
	var year = d.getFullYear();

	var curr_date = month_name[month] + " " + day + " " + year;
	var dateString = new Date(curr_date).toDateString();
	var dayOfTheWeek = dateString.substring(0, 3); //Mon, Tue, ...
	var nameOfDay = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
	var dayIndex = nameOfDay.indexOf(dayOfTheWeek);	//0, 1, 2, ...
	var totDays = new Date(year, month + 1, 0).getDate();

	var calendar = getCalendar(dayIndex, totDays);
	document.getElementById("month-year").innerHTML = month_name[month] + " " + year;
	document.getElementById("dates").appendChild(calendar);
}	

function getCalendar(day_no, days){
	var table = document.createElement('table');
	var tr = document.createElement('tr');

	for (var day_name = 0; day_name < 7; day_name++){
		var td = document.createElement('td');
		td.innerHTML = "SMTWTFS"[day_name];
		tr.appendChild(td);
	}
	table.appendChild(tr);

	tr = document.createElement('tr');

	var d;
	for (d = 0; d < 7; d++){
		if (d == day_no) {
			break;
		}
		var td = document.createElement('td');
		td.innerHTML = "";
		tr.appendChild(td);
	}
	var count = 1;
	for (; d <= 6; d++){
		var td = document.createElement('td');
		td.innerHTML = count;
		count++;
		tr.appendChild(td);
	}
	table.appendChild(tr);

	for (var row = 3; row < 8; row++){
		tr = document.createElement('tr');
		for (var day = 0; day < 7; day++){
			if (count > days){
				table.appendChild(tr);
				return table;
			}
			var td = document.createElement('td');
			td.innerHTML = count;
			count++;
			tr.appendChild(td);
		}
		table.appendChild(tr);
	}

	return table;
}

