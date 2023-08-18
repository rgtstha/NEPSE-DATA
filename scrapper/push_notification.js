var admin = require("firebase-admin");
require('dotenv').config();

var serviceAccount = process.env.SERVICE_ACCOUNT_JSON;

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