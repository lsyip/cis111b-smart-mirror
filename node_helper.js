//Helps run the Python code

var NodeHelper = require("node_helper");
const {PythonShell} = require("python-shell");

module.exports = NodeHelper.create({
    start:function(){
            console.log("Starting module: " + this.name);
    },

    //sendSocketNotification processes request
    socketNotificationReceived: function(notification, payload) {
            if (notification === "CONFIG") {
                console.log('Initial setup request');
                this.setProfile();
            }
    		if (notification === 'GET NAME') {
    			console.log('Initial name request received.');
    			this.getName();
    		};
    		if (notification === 'UPDATE') {
    		    console.log('Update name request received.');
    		    this.getName();
    		}

    	},

    // Initial setup
    setProfile: function() {
        PythonShell.run('python/setup.py', options, function(err, results) {
            if (err) throw err;
            console.log('results: %j', results);
        });
    },

    // Returns identity of user via webcam
    getName: function() {
        const self = this;
        const fileName = 'RecognizeUser.py';  //The file that we want to run
        console.log('Running ' + fileName);   // Log event

        //Create new PythonShell, use that to run the file
        let faceRecPyShell = new PythonShell(fileName, {scriptPath: 'modules/face-rec-module/python'});
        console.log('Creating new pyShell');

        //TODO: Figure out what this does
        faceRecPyShell.on('message', function (message) {
                if (message['type'] == 'name') {
                    console.log('')
                    self.sendSocketNotification('DATA', message);
                }
        });


        faceRecPyShell.end(function (err) {
                if (err) throw err;
                self.sendSocketNotification('DATA', 'Finished getting name');
                console.log('Finished getting name');
        });
    },
});
