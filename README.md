# Medical Systems
The goal of the following application is to provide a service for medical institutions that allows for automation and better documentation of patients' hospital stays.
## Functionalities
The application allows the creation, modification, deletion, and viewing of:
* Visits
* Recommendations
* Prescriptions
* States of patients
* Illnesses of patients
## Roles
The application recognizes three roles:</br>
<b>Administrators</b> are allowed to work on all of the above functionalities, as well as performing CRUD operations on:</br>
* Users and their Profiles
* Doctors
* Patients
* Specializations
* Countries
* Addresses</br>

<b>Doctors</b> are allowed to work on all of the above functionalities.</br>

<b>Patients</b> can only:</br>
* See their discharge
* See their visits
* Book a new visit</br>
## Installation
After creating a local copy of the files, in the root folder, run the following command in a terminal of your choice:</br>
<pre>
pip install -r requirements.txt
</pre>
This will install necessary dependencies.</br>
Next, execute following commands:</br>
<pre>
python manage.py makemigrations
python manage.py migrate
</pre>
This will prepare the database.<br>
Next, add administrators:</br>
<pre>
python manage.py createsuperuser
</pre>
And follow the prompts. Users added this way will have full access to the entire application.</br>
## Usage
Execute the following command:
<pre>
python manage.py runserver
</pre>
This will start the server and allow access its web interface.</br></br>
Administrators should navigate to:
<pre>
http://127.0.0.1:8000/api/
</pre>
Other user should navigate to:
<pre>
http://127.0.0.1:8000/home/
</pre>
Users should press their respective login button and provide their credentials.</br></br>
After that, they will be granted access to their resources.</br>
