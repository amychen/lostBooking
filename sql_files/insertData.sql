-- a
insert into airline values ('China Eastern');
insert into airline values ('Emirates');
insert into airline values ('Delta');
insert into airline values ('Virgin America');
insert into airline values ('Alaska Airlines');
insert into airline values ('Southwest Airlines');
insert into airline values ('Qatar Airways');
insert into airline values ('Singapore Airlines');
insert into airline values ('Cathay Pacific');
insert into airline values ('Ethihad Airways');
insert into airline values ('Asiana Airlines');
insert into airline values ('Air France');
insert into airline values ('British Airways');
insert into airline values ('Air New Zealand');
insert into airline values ('Hainan Airlines');
insert into airline values ('Malaysia Airlines');
insert into airline values ('Peach');
insert into airline values ('Vietnam Airlines');
insert into airline values ('United Airlines');
insert into airline values ('Japan Airlines');
insert into airline values ('Air Canada');
insert into airline values ('China Southern');

-- b
insert into airport values ('JFK', 'New York City');
insert into airport values ('PVG', 'Shanghai');
insert into airport values ('SFO', 'San Francisco');
insert into airport values ('ORD', 'Chicago');
insert into airport values ('ATL', 'Atlanta');
insert into airport values ('PEK', 'Beijing');
insert into airport values ('DXB', 'Dubai');
insert into airport values ('HND', 'Tokyo');
insert into airport values ('LAX', 'Los Angeles');
insert into airport values ('LHR', 'United Kingdom');
insert into airport values ('HKG', 'Hong Kong');
insert into airport values ('CDG', 'France');
insert into airport values ('FRA', 'Frankfurt');
insert into airport values ('DEL', 'Delhi');		
insert into airport values ('SIN', 'Changi');
insert into airport values ('ICN', 'Incheon');
insert into airport values ('BKK', 'Bang Phli');


-- c
insert into customer values ('abc@gmail.com', 'Ava Chen', 'applePie', "100", 'Grand Street', 'New York', 'New York', 
							 9173333333, '998877665', '2017-03-27', 'USA', '2000-10-29');
insert into customer values ('123@gmail.com', 'Andy Chen', 'hotPotato', "911", 'Bleeke Street', 'New York', 'New York', 
							 6462838618, '112233445', '2017-03-28', 'USA', '1999-03-15');
-- d
insert into airplane values ('Delta', 'Boeing 737', 200);
insert into airplane values ('Malaysia Airlines', 'Boeing 757', 430);
insert into airplane values ('China Eastern', 'Boeing 737', 137);
insert into airplane values ('China Eastern', 'Airbus A320', 240);
insert into airplane values ('United Airlines', 'Airbus A380', 850);
insert into airplane values ('Emirates', 'Boeing 747', 600);
insert into airplane values ('Emirates', 'Airbus A380', 1000);
insert into airplane values ('Singapore Airlines', 'Airbus A380', 1231);
insert into airplane values ('Qatar Airways', 'Boeing 727', 450);
insert into airplane values ('Cathay Pacific', 'Boeing 676', 871);
insert into airplane values ('Hainan Airlines', 'Boeing 757', 535);
insert into airplane values ('Alaska Airlines', 'Boeing 787', 683);
insert into airplane values ('Southwest Airlines', 'Boeing 757', 137);	
insert into airplane values ('British Airways', 'Boeing 747', 230);	
insert into airplane values ('Ethihad Airways', 'Boeing 747', 240);
insert into airplane values ('Air New Zealand', 'McDonnell Douglas DC-9', 350);		

-- e
insert into airline_staff values ('amychen', 'abcd1234!', 'Amy', 'Chen', '1998-03-19', 'China Eastern');

-- f 
insert into flight values ('Delta', 267, 'JFK', 090920, 'SFO', 171008, 314.89, 'UPCOMING', 'Boeing 737');
insert into flight values ('China Eastern', 587, 'PVG', 091059, 'JFK', 233050, 580.33, 'DELAYED', 'Airbus A320');
insert into flight values ('United Airlines', 297, 'PVG', 213005, 'JFK', 103070, 857.79, 'IN-PROGRESS', 'Airbus A380');

-- g
insert into ticket values (12345, 'Delta', 267);
insert into ticket values (54321, 'China Eastern', 587);
insert into ticket values (32154, 'United Airlines', 297);

insert into booking_agent values ('myemail@mu.com', 'password', 123456);
insert into booking_agent values ('dummy@gmail.com', 'dummy', 99999999999);

insert into purchases values (12345, '123@gmail.com', 123456, '2018-07-07');
insert into purchases values (54321, 'abc@gmail.com', 99999999999, '2018-08-19');