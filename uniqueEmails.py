from flask import Flask, request
import re

app = Flask(__name__)


def countEmails(emails):
    listOfEmails = None
    uniqueEmails = {}

    # elif block to cover for a python list or a string of all emails
    if type(emails) is str:
        listOfEmails = emails.split(',')
    elif type(emails) is list:
        listOfEmails = emails
    for i in listOfEmails:
        # remove leading and trailing whitespaces, only for form usage
        strippedString = i.strip()
        # + sign in http requests turn into spaces
        spaceToPlus = strippedString.replace(' ', '+')
        # check if valid email, after formatting earlier
        if not (re.search('^[a-z0-9+]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', spaceToPlus)):
            continue
        noPeriods = spaceToPlus.replace('.', '')
        # regex to ignore + in email
        noPlus = re.sub('[+].*(?=\@)', '', noPeriods)
        if noPlus not in uniqueEmails.keys():
            uniqueEmails[noPlus] = 1
    return len(uniqueEmails)


@app.route('/query')
def query():
    emails = request.args.get('emails')
    numUniqueEmails = countEmails(emails)
    return '<h1>the number of unique emails is : {} </h1>'.format(numUniqueEmails)


@app.route('/form', methods=['POST', 'GET'])
def form():
    if request.method == 'POST':
        emails = request.form.get('emails')
        numUniqueEmails = countEmails(emails)
        return '<h1>the number of unique emails is : {} </h1>'.format(numUniqueEmails)

    return '''<form method = "POST">
    <h2>Input the emails you would like to check below (separated by commas) and press submit to check the number of unique emails</h2>
    Emails <textarea type="text" name="emails" rows="4" cols ="50"></textarea>
    <input type="submit">
    </form>
    '''


@app.route('/json', methods=['POST'])
def json():
    req_data = request.get_json()
    emails = req_data['emails']
    numUniqueEmails = countEmails(emails)
    return '<h1>the number of unique emails is : {} </h1>'.format(numUniqueEmails)


@app.route('/')
def home():
    return '''<h1>This is the uniqueEmails webservice</h1>
    <p>To do a URL query, add "/query?emails=" (without the quotes) to the address bar and add the emails you want to check, separated by commas (no spaces) and then enter the query.</p>
    <p>To use a form, <a href="http://127.0.0.1:5000/form">click on this hyperlink to navigate to the form</a>. A text box should appear and allow you to input a list of emails, separated by commas. To check the number of unique emails, press the submit button</p>
    <p>To use JSON data, use an API tester (e.g Postman) to send in a JSON, where the request URL is "127.0.0.1:5000/json". Set your emails in an array and make the key label "emails" The http request to use is POST. An example: <pre><code>{
     "emails": ["testemail@gmail.com", "test.email@fetchrewards.com"] 
}</p>
    '''


if __name__ == '__main__':
    app.run(debug=True, port=5000)
