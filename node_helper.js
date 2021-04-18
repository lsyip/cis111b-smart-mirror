//Helps run the Python code

var NodeHelper = require("node_helper");
var PythonShell = require("python-shell");

module.exports = NodeHelper.create({
    start:function(){
    console.log("Starting module: " + this.name);
    },

    //TODO: sendSocketNotification setup

    // Returns identity of user via webcam
    getName: function() {
        const self = this;
        const fileName = 'setup.py';
        console.log('Running ' + fileName);
        const faceRecPyShell = new PythonShell(fileName, {mode: 'json', scriptPath: 'modules/face-rec-module/python'});

        faceRecPyShell.on('message', function (message) {
                if (message['type'] == 'data') {
                    self.sendSocketNotification('DATA', message);
                }
        });

        faceRecPyShell.end(function (err) {
                if (err) throw err;
                self.sendSocketNotification('UPDATE', 'Finished getting data');
                console.log('Finished getting data');
        });
    },
});