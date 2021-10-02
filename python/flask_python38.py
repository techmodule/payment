from __future__ import print_function

from datetime import timedelta, datetime
import requests
from flask import Blueprint, request, jsonify, json
import base64
from .models import HaraCustomers, \
    HaraShop

now = datetime.utcnow() + timedelta(hours=7)
payments = Blueprint('payments', __name__)
import hashlib
import hmac
import json
import uuid
def zalo_payment(amount):
    # parameters send to MoMo get get payUrl
    endpoint = " https://test-payment.momo.vn/gw_payment/transactionProcessor"
    partnerCode = "MOMOIQA420180417"
    accessKey = "SvDmj2cOTYZmQQ3H"
    secretKey = "PPuDXq1KowPT1ftR8DvlQTHhC03aul17"
    orderInfo = "pay with MoMo"
    redirectUrl = "https://booking-app.vn/api/v2/zalo/payment/return"
    ipnUrl = "https://booking-app.vn/api/v2/zalo/payment/notify"
    #amount = "50000"
    orderId = str(uuid.uuid4())
    requestId = str(uuid.uuid4())
    requestType = "captureWallet"
    extraData = ""  # pass empty value or Encode base64 JsonString
    # before sign HMAC SHA256 with format: accessKey=$accessKey&amount=$amount&extraData=$extraData&ipnUrl=$ipnUrl&orderId=$orderId&orderInfo=$orderInfo&partnerCode=$partnerCode&redirectUrl=$redirectUrl&requestId=$requestId&requestType=$requestType
    rawSignature = "accessKey=" + accessKey + "&amount=" + amount + "&extraData=" + extraData + "&ipnUrl=" + ipnUrl + "&orderId=" + orderId + "&orderInfo=" + orderInfo + "&partnerCode=" + partnerCode + "&redirectUrl=" + redirectUrl + "&requestId=" + requestId + "&requestType=" + requestType
    print(rawSignature, type (rawSignature))
    # puts raw signature
    #digest = hmac.new(secretKey.encode('utf-8'), rawSignature, hashlib.sha256).digest()
    key_bytes = bytes(secretKey, 'utf-8')
    # encoding as per other answers
    byte_key = bytes(secretKey, 'UTF-8')  # key.encode() would also work in this case
    message = rawSignature.encode()

    # now use the hmac.new function and the hexdigest method
    h = hmac.new(byte_key, message, hashlib.sha256)
    signature = h.hexdigest()
    data = {
        'partnerCode': partnerCode,
        'partnerName': "Test",
        'storeId': "MomoTestStore",
        'requestId': requestId,
        'amount': amount,
        'orderId': orderId,
        'orderInfo': orderInfo,
        'redirectUrl': redirectUrl,
        'ipnUrl': ipnUrl,
        'lang': "vi",
        'extraData': extraData,
        'requestType': requestType,
        'signature': signature
    }
    #data = json.dumps(data)
    clen = len(data)
    headers ={'Content-Type': 'application/json; charset=UTF-8', 'Content-Length': str(clen)}
    response = requests.post(endpoint, headers=headers, json=data)
    print(response.json())
    return response
