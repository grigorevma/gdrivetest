# gdrivetest
my simple cloud xD

add your api key and other in app/config.py


# bucket = os.environ['BUCKET'] 
your bucket S3
# AWS_IDKEY = os.environ['AWS_IDKEY']
from IAM AWS
# AWS_SKEY = os.environ['AWS_SKEY']
from IAM AWS
# urldb = os.environ['URLDB']
"url:port/postgres"
# userpass = os.environ['USERPASS']
"user:pass"
# session_csy = os.environ['SESSION_CSY']
text field
# session_key = os.environ['SESSION_KEY']
text field

deploy your app on heroku simple:

heroku create yourappname

heroku container:push web --app yourappname
#push from current dir (where Dockerfile placed)

Then
heroku container:release web --app yourappname

Finish! visit your app
https://yourappname.herokuapp.com
