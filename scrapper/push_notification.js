var admin = require("firebase-admin");
require('dotenv').config();


var project_id = process.env.FIREBASE_PROJECT_ID;
var private_key_id = process.env.FIREBASE_PRIVATE_KEY_ID;
var private_key = process.env.FIREBASE_PRIVATE_KEY;
var client_email = process.env.FIREBASE_CLIENT_EMAIL;
var client_id = process.env.FIREBASE_CLIENT_ID;
var auth_uri = process.env.FIREBASE_AUTH_URI;
var token_uri = process.env.FIREBASE_TOKEN_URI;
var auth_provider_x509_cert_url = process.env.FIREBASE_AUTH_PROVIDER_X509_CERT_URL;
var client_x509_cert_url = process.env.FIREBASE_CLIENT_X509_CERT_URL;
var universe_domain = process.env.FIREBASE_UNIVERSE_DOMAIN;

var serviceAccount = {
    "type": "service_account",
    "project_id": project_id,
    "private_key_id": private_key_id,
    "private_key": private_key,
    "client_email": client_email,
    "client_id": client_id,
    "auth_uri": auth_uri,
    "token_uri": token_uri,
    "auth_provider_x509_cert_url": auth_provider_x509_cert_url,
    "client_x509_cert_url": client_x509_cert_url,
    "universe_domain": universe_domain
}


console.log("service account type: " + typeof serviceAccount);

admin.initializeApp({
    credential: admin.credential.cert(serviceAccount)
});

const ipo_list = require('./ipo_list.json');
const todayDate = new Date().toISOString().slice(0, 10);
console.log("Today's date: " + todayDate);
const opening_today = ipo_list.ipo_list.filter(ipo => ipo.opening_date == todayDate);
const closing_today = ipo_list.ipo_list.filter(ipo => ipo.closing_date == todayDate);

// log the value of opening today ipo

console.log("Opening today ipo: " + opening_today.map(ipo => ipo.company));

const sendNotification = (title, body) => {
    try {
        const notification = {
            title: title,
            body: body
        };

        const options = {
            priority: "high",
            timeToLive: 60 * 60 * 24
        };

        admin.messaging().sendToTopic("ipo", {
            notification: notification,
        }).then((response) => {
            console.log("Successfully sent message:", response);
        }).catch((error) => {
            console.log("Error sending message:", error);
        });
    }
    catch (err) {
        console.log("Error sending message:", err);
    }
};

console.log("Opening today ipo length: " + opening_today.length);
if (opening_today.length > 0) {
    opening_today.forEach(ipo => {
        sendNotification("IPO Opening Today", ipo.company + " is opening today.");
    });
}

if (closing_today.length > 0) {
    closing_today.forEach(ipo => {
        sendNotification("IPO Closing Today", ipo.company_name + " is closing today.");
    });
}