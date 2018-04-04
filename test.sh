!#/bin/bash

curl -H "Content-Type: application/json" \
	-X POST \
	-d '{"problem":["Anxiety","Something else ..."],"other":"other","max-spend":"2","tell-us":"Something else!","first":"c","last":"g","email":"ixplode@gmail.com","age":"30","zip":"10009"}' \
 	https://api.monday.health/patient/submit

