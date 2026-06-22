import re

with open('static/script.js', 'r', encoding='utf-8') as f:
    text = f.read()

bad_trigger = """    if (keysPressed.includes('hacker')) {
        keysPressed = ''; // reset
        switchView('view-hacker');
        printHacker("AUREX OS ROOT ACCESS GRANTED.");
        printHacker("Type 'help' for commands.");
        setTimeout(() => document.getElementById('hacker-input').focus(), 100);
    }"""

good_trigger = """    if (keysPressed.includes('hacker')) {
        keysPressed = ''; // reset
        switchView('view-hacker');
        document.getElementById('hacker-output').innerHTML = '';
        
        const bootSequence = [
            "Initializing AurexOS kernel...",
            "Loading drivers... OK",
            "Mounting virtual filesystems... OK",
            "Bypassing firewall protocols [■■■■■■■■■■] 100%",
            "Decrypting RSA-4096 keys... SUCCESS",
            "Establishing secure tunneling to remote server...",
            "WARNING: Intrusion countermeasures detected.",
            "Deploying counter-countermeasures...",
            "Injecting payload... [0x0F82A1B]",
            "Extracting classified datablocks...",
            "----------------------------------------",
            "AUREX OS ROOT ACCESS GRANTED.",
            "Type 'help' for commands."
        ];
        
        let delay = 0;
        bootSequence.forEach((line, index) => {
            setTimeout(() => {
                if (index < 10) {
                    printHacker(line + " [" + Math.random().toString(16).substring(2, 10) + "]");
                } else {
                    printHacker(line);
                }
            }, delay);
            delay += Math.floor(Math.random() * 200) + 50; // Random delay between 50 and 250ms
        });
        
        setTimeout(() => document.getElementById('hacker-input').focus(), delay + 100);
    }"""

if bad_trigger in text:
    text = text.replace(bad_trigger, good_trigger)
    with open('static/script.js', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Fixed hacker tons of code!")
else:
    print("Could not find hacker trigger!")
