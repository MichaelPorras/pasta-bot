// install: npm install
// usage: node lul.js $ACCESS_KEY $SECRET_KEY text you want me to say
var fs = require('fs'),
Ivona = require('ivona-node');
var exec = require('child_process').exec;
var le_words = process.argv.slice(2, process.argv.length)
var ivona = new Ivona({
    accessKey: le_words[0], 
    secretKey: le_words[1] 
});
ivona.createVoice(le_words.slice(2, le_words.length).join(' '))
    .pipe(fs.createWriteStream('/tmp/kek.mp3').on('finish', function () {
        exec('cvlc /tmp/kek.mp3 vlc://quit', function callback(error, stdout, stderr){
            console.log(error, stdout, stderr)
        });
}));

