/* Chose one of the import statement below */
// import rainbowSDK from './rainbow-sdk.min.js'; // If you do not use the bundler
import rainbowSDK from '../js/rainbow-sdk.min.js'; // If you do not use the bundler

var OperatorContact = null;
var RoomServiceContact = null;
var InRoomDiningContact = null;
var MyAccount = null;
// var myRainbowLogin = "samuel.yip@al-enterprise.com";       // Replace by your login
// var myRainbowPassword = "Ciscotac_123"; // Replace by your password

let onReady = function onReady() {
    console.log('[RainbowSDK] :: On SDK Ready!');

};
document.addEventListener(rainbowSDK.RAINBOW_ONREADY, onReady);


let onStarted = function onStarted() {
    console.log('[RainbowSDK] :: On SDK Started!');
};
document.addEventListener(rainbowSDK.connection.RAINBOW_ONSTARTED, onStarted); // event will be fired once user connects and all SDK services start


let onLoaded = function onLoaded() {
    console.log('[RainbowSDK] :: On SDK Loaded!');

    rainbowSDK
        .initialize('8fbb04008ced11eea993e3f906271088', 'iYlE1lOWB2qFbB0cIJVU4P5BxFKfLrx5dAaQqwOqPcaKZDJ8CD5MMK5ye9BSugLU')
        .then(() => {
            console.log('[RainbowSDK] :: Rainbow SDK is initialized!');
        })
        .catch(err => {
            console.log('[RainbowSDK] :: Something went wrong with the SDK...', err);
        });
};
document.addEventListener(rainbowSDK.RAINBOW_ONLOADED, onLoaded);


let SignIn = function SignIn() {

    // The SDK for Web is ready to be used, so you can sign in
    rainbowSDK.connection.signin(myRainbowLogin, myRainbowPassword)
    .then(function(account) {
          // Successfully signed to Rainbow and the SDK is started completely. Rainbow data can be retrieved.
          console.log('[RainbowSDK] :: Sign in!');
          rainbowSDK.contacts.searchByLogin("operator@alehotel.dyndns-ip.com").then(function(usersFound) {
            OperatorContact = usersFound
          });
          rainbowSDK.contacts.searchByLogin("roomservice@alehotel.dyndns-ip.com").then(function(usersFound) {
            RoomServiceContact = usersFound
          }); 
          rainbowSDK.contacts.searchByLogin("inroomdinning@alehotel.dyndns-ip.com").then(function(usersFound) {
            InRoomDiningContact = usersFound
          });        
          
          document.getElementById("loading").style.display = "none";
          document.getElementById("loaded").style.display = "block";


    })
    .catch(function(err) {
          // An error occurs (e.g. bad credentials). Application could be informed that sign in has failed
    });  
};


let onSigned = function onSigned(event) {
    let account = event.detail;
    MyAccount = account;
    console.log(MyAccount);

    // Authentication has been performed successfully. Account information could be retrieved.
};
document.addEventListener(rainbowSDK.connection.RAINBOW_ONSIGNED, onSigned);

var associatedConversation = null;
var currentPage = 0;

let ContactOperator = function ContactOperator(){
    document.getElementById("whois").textContent = "Operator";
    document.getElementById("conversations").innerHTML = ""
    rainbowSDK.conversations.openConversationForContact(OperatorContact).then(function(conversations) {
        // console.log(conversations)
        associatedConversation = conversations;
        rainbowSDK.im.getMessagesFromConversation(associatedConversation.id, 30).then(function() {
            // The conversation object is updated with the messages retrieved from the server (same reference)
            
            // Call a function to display the new messages received
            displayMessages(associatedConversation, currentPage);
    
            // Display something if there is possibly more messages on the server
            if(!associatedConversation.historyAboveComplete) {
                // e.g. display a button to get more messages
            }
        });
    }).catch(function(err){

    });
};
document.getElementById("ContactOperator").addEventListener("click", ContactOperator);

let RoomService = function RoomService(){
    document.getElementById("whois").textContent = "Room Service";
    document.getElementById("conversations").innerHTML = ""
    rainbowSDK.conversations.openConversationForContact(RoomServiceContact).then(function(conversations) {
        // console.log(conversations)
        associatedConversation = conversations;
        rainbowSDK.im.getMessagesFromConversation(associatedConversation.id, 30).then(function() {
            // The conversation object is updated with the messages retrieved from the server (same reference)
            
            // Call a function to display the new messages received
            displayMessages(associatedConversation, currentPage);
    
            // Display something if there is possibly more messages on the server
            if(!associatedConversation.historyAboveComplete) {
                // e.g. display a button to get more messages
            }
        });
    }).catch(function(err){

    });
};
document.getElementById("RoomService").addEventListener("click", RoomService);


function displayMessages(conversations, currentPage) {
    console.log(conversations)
    Object.values(conversations.messages).forEach(message => {
        if(message.from.emailPro == "operator@alehotel.dyndns-ip.com"){
            displayMyMessage(message.data, "bubble-left")
        } else if (message.from.emailPro == "roomservice@alehotel.dyndns-ip.com"){
            displayMyMessage(message.data, "bubble-left")
        } else if(message.from.emailPro == "inroomdinning@alehotel.dyndns-ip.co"){
            displayMyMessage(message.data, "bubble-left")
        } else {
            displayMyMessage(message.data, "bubble-right")
        }
    });
};

function displayMyMessage(message, className) {
    const div = document.getElementById("conversations")
    div.innerHTML += '<div class="row"><div class="' + className + '">' + message + '</div></div>';
    div.scrollTo({
        top: div.scrollHeight,
        behavior:'smooth'
    })
};

let onNewMessageReceived = function onNewMessageReceived(event) {

    // as noted in the documentation, RAINBOW_ONNEWIMMESSAGERECEIVED carries three parameters: Message, Conversation and CC. Let's retrieve them:

    let message = event.detail.message;
    let conversation = event.detail.conversation;
    let cc = event.detail.cc;

    console.log(message.data)
    displayMyMessage(message.data, "bubble-left")


    rainbowSDK.im.markMessageFromConversationAsRead(conversation.id, message.id);
    // do something with the event

}
document.addEventListener(rainbowSDK.im.RAINBOW_ONNEWIMMESSAGERECEIVED, onNewMessageReceived);

let sendMessage = function sendMessage(){
    var messageContent = document.getElementById("sendMessage").value
    rainbowSDK.im.sendMessageToConversation(associatedConversation.id, messageContent);
    displayMyMessage(messageContent, "bubble-right")
    document.getElementById("sendMessage").value = ""
};
document.getElementById("send").addEventListener("click", sendMessage);


let sendMessageEnterPress = function sendMessageEnterPress(event) {
    if (event.key === "Enter") {
        // Cancel the default action, if needed
        event.preventDefault();
        // Trigger the button element with a click
        document.getElementById("send").click();
    }
}
document.getElementById("sendMessage").addEventListener("keypress", sendMessageEnterPress);


rainbowSDK.start();
rainbowSDK.load();
SignIn();

