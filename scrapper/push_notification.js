var admin = require("firebase-admin");
require('dotenv').config();

var serviceAccount = JSON.parse(process.env.SERVICE_ACCOUNT_JSON);

admin.initializeApp({
    credential: admin.credential.cert(serviceAccount)
});

const ipo_list = require('./ipo_list.json');
const todayDate = new Date().toISOString().slice(0, 10);
const opening_today = ipo_list.ipo_list.filter(ipo => ipo.opening_date === todayDate);
const closing_today = ipo_list.ipo_list.filter(ipo => ipo.closing_date === todayDate);

const sendNotification = (title, body) => {
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
};

if (opening_today.length > 0) {
    opening_today.forEach(ipo => {
        sendNotification("IPO Opening Today", ipo.company_name + " is opening today.");
    });
}

if (closing_today.length > 0) {
    closing_today.forEach(ipo => {
        sendNotification("IPO Closing Today", ipo.company_name + " is closing today.");
    });
}