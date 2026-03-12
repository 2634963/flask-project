# flask --app paymentProcessor run -p 3000

from flask import Flask
from flask import request

from markupsafe import escape

app = Flask(__name__)

# as long as the connection is https, an attacker can only see domain and subdomain of a connection
# they are unable to see any arguments in the URL
# so for example https://subdomain.domain.com/?cardNumber=1234123412341234&expireDay=12&expireMonth=03&ccv=123&paymentAmountPence=100
# the only part an attacker can see is https://subdomain.domain.com
# therefore this should be secure enough for our purposes as long as https is enforced

# localhost:3000/submitPayment?cardNumber=nnnnnnnnnnnnnnnn&ccv=nnn&expireMonth=nn&expireYear=nnnn&paymentAmountPence=nnn
# cardNumber:         16  digit number > 0
# ccv:                3   digit number  > 0
# expireMonth:        2   digit number  > 0  &&  <= 12
# expireYear:         any length number > 0
# paymentAmountPence: any length number > 0

def checkValidCardNumber(cardNumberString):
    if len(cardNumberString) != 16:
        return False

    try:
        if int(cardNumberString) < 0:
            return False
    except ValueError:
        return False

    return True

def checkExpiry(monthString, yearString):
    try:
        if not (1 <= int(monthString) <= 12):
            return False

        # just assume a valid year for now
        if int(yearString) <= 0:
            return  False

    except ValueError:
        return False

    return True

def checkCCV(ccvString):
    if len(ccvString) !=3:
        return False

    try:
        int(ccvString)
    except ValueError:
        return False

    return True

def checkPaymentAmount(paymentAmountPence):
    try:
        if int(paymentAmountPence) <= 0:
            return False
    except ValueError:
        return False

    return True

@app.route("/")
@app.route("/index.html")
def homePage():
    return "<p>please submit a request to /submitPayment</p>"

@app.route("/submitPayment")
def submitPayment():
    def error():
        return "<p>invalid card details or no payment amount</p>"

    print(request.remote_addr)
    print(request.remote_user)

    if (not app.debug) and request.host_url.startswith("https"):
        return "<p>connection not secure, please connect again using https", 400

    #                                      thing to get,         default value if not present
    cardNumber         = request.args.get("cardNumber",         "invalid")
    expireMonth        = request.args.get("expireMonth",        "invalid")
    expireYear         = request.args.get("expireYear",         "invalid")
    ccv                = request.args.get("ccv",                "invalid")
    paymentAmountPence = request.args.get("paymentAmountPence", "invalid")

    if not checkValidCardNumber(cardNumber):
        return error(), 400

    if not checkExpiry(expireMonth, expireYear):
        return error(), 400

    if not checkCCV(ccv):
        return error(), 400

    if not checkPaymentAmount(paymentAmountPence):
        return error(), 400

    return "<p>success<p>", 200
