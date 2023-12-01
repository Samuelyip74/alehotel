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
          checkMakeAudioVideoCall();


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

    if (message.includes("activeCallMsg")) { message = "Incoming Call"; className = 'bubble-center'};
    if (message.includes("missedCall")) { message = "Missed Call"; className = 'bubble-center'};

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

let checkMakeAudioVideoCall = function checkMakeAudioVideoCall(){

    if(rainbowSDK.webRTC.canMakeAudioVideoCall()) {
        /* Your browser is compliant: You can make audio and video call using WebRTC in your application */
        console.log("Audio OK")
        document.getElementById("call").style.display = "flex;";

    }
    else {
        /* Your browser is not compliant: Do not propose audio and video call in your application */
        console.log("Audio NOK")
        document.getElementById("call").style.display = "none;";
    }

};

let callInAudio = function callInAudio(contactId) {
    /* Call this API to call a contact using only audio stream*/
    rainbowSDK.webRTC.callInAudio(contactId).then(res => {
        if(res.label === "OK") {
            /* Your call has been correctly initiated. Waiting for the other peer to answer */
        }
    }).catch(err => {
        return err
    });
};

let initialCall = function initialCall() {
    var who = document.getElementById("whois").textContent 
    if(who == "Operator"){
        callInAudio(OperatorContact.id)
    } else if (who == "Room Service") {
        callInAudio(RoomServiceContact.id)
    }

}
document.getElementById("call").addEventListener("click", initialCall);

var callevent = null
let onWebRTCCallChanged = function onWebRTCCallChanged(event) {
    callevent = event;
    let call = event.detail;
    console.log(call.status.value)
    if (call.status.value === "incommingCall") {
        const CallToast = document.getElementById('CallToast');
        CallToast.classList.add("show");
    } else if(call.status.value === "Unknown"){
        CallToast.classList.remove("show");
    }


};

/* Subscribe to WebRTC call change */
document.addEventListener(rainbowSDK.webRTC.RAINBOW_ONWEBRTCCALLSTATECHANGED, onWebRTCCallChanged)

var callerid = null;
let AnswerCall = function AnswerCall(){
        /* Listen to WebRTC call state change */
    var event = callevent
    let call = event.detail;

    if (call.status.value === "incommingCall") {
        // You have an incoming call, do something about it:
        callerid = call.id;
        // Detect the type of incoming call

        if (call.remoteMedia === 3) {

            // The incoming call is of type audio + video
            rainbowSDK.webRTC.answerInVideo(call.id);

            // Populate the #minivideo and #largevideo elements with the video streams

            rainbowSDK.webRTC.showLocalVideo();
            rainbowSDK.webRTC.showRemoteVideo(call.id);

        } else if (call.remoteMedia === 1) {

            // The incoming call is of type audio
            rainbowSDK.webRTC.answerInAudio(call.id);
        }
    }
    // CallToast.classList.remove("show");
    document.getElementById("Answer").style.display = "None";
    document.getElementById("Reject").style.display = "None";
    document.getElementById("End").style.display = "inline-block";
}
document.getElementById("Answer").addEventListener("click", AnswerCall);

let dropCall = function dropCall(){
    releaseCall(callerid);
    document.getElementById("Answer").style.display = "inline-block";
    document.getElementById("Reject").style.display = "inline-block";
    document.getElementById("End").style.display = "None";
}
document.getElementById("End").addEventListener("click", dropCall);


let releaseCall = function releaseCall(callerid) {
    /* Call this API to release the call */
    let res = rainbowSDK.webRTC.release(callerid);
};


rainbowSDK.start();
rainbowSDK.load();
SignIn();

