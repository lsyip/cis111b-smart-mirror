//Helps run the Python code

var NodeHelper = require("node_helper");
var PythonShell = require("python-shell");

module.exports = NodeHelper.create({
    start:function(){
            console.log("Starting module: " + this.name);
    },

    //sendSocketNotification setup: runs the getName() function, which identifies the user
    socketNotificationReceived: function(notification, payload) {
    		if (notification === 'GET NAME') {
    			console.log('Name request received.');
    			this.getName();
    		};
    	},

    // Returns identity of user via webcam
    getName: function() {
        const self = this;
        const fileName = 'RecognizeUser.py';  //The file that we want to run
        console.log('Running ' + fileName);   // Log event

        //Create new PythonShell, use that to run the file
        const faceRecPyShell = new PythonShell(fileName, {mode: 'json', scriptPath: 'modules/face-rec-module/python'});

        //TODO: Figure out what this does
        faceRecPyShell.on('message', function (message) {
                if (message['type'] == 'name') {
                    self.sendSocketNotification('DATA', message);
                }
        });


        faceRecPyShell.end(function (err) {
                if (err) throw err;
                self.sendSocketNotification('UPDATE', 'Finished getting name');
                console.log('Finished getting name');
        });
    },
});