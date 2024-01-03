class Chatbox {
    constructor() {
        this.args = {
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button')
        };

        this.state = false;
        this.messages = [];
    }

    display() {
        const { openButton, chatBox, sendButton } = this.args;

        openButton.addEventListener('click', () => this.toggleState(chatBox));
        sendButton.addEventListener('click', () => this.onSendButton(chatBox));

        const node = chatBox.querySelector('input');
        node.addEventListener("keyup", ({ key }) => {
            if (key === "Enter") {
                this.onSendButton(chatBox);
            }
        });
    }

    toggleState(chatbox) {
        this.state = !this.state;

        // Show or hide the box
        if (this.state) {
            chatbox.classList.add('chatbox--active');
        } else {
            chatbox.classList.remove('chatbox--active');
        }
    }

    onSendButton(chatbox) {
        const textField = chatbox.querySelector('input');
        const text = textField.value.trim();
    
        if (text.toLowerCase() === "quit") {
            // Handle the quit action (e.g., close the chatbox)
            this.toggleState(chatbox);
            fetch('/get_response', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({ user_message: text }).toString(),
            })
            .then(response => response.json())
            .then(response => {
                if (response.redirect) {
                    // Redirect to the result page
                    window.location.href = "/result";
                }
            });
            return;
        }
    
        const userMessage = { name: "User", message: text };
        this.messages.push(userMessage);
    
        fetch('/get_response', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({ user_message: text }).toString(),
        })
        .then(response => response.json())
        .then(response => {
            if (response.bot_response.toLowerCase() === 'chat terminated. goodbye!') {
                // Handle the quit action, for example, hide the chatbox
                this.toggleState(chatbox);
                return;
            }
        
            const samMessage = { name: "Sam", message: response.bot_response };
            this.messages.push(samMessage);
            this.updateChatText(chatbox);
            textField.value = '';
        });
    
    }

    updateChatText(chatbox) {
        let html = '';
        this.messages.slice().reverse().forEach(item => {
            const className = item.name === "Sam" ? "messages__item--visitor" : "messages__item--operator";
            html += `<div class="messages__item ${className}">${item.message}</div>`;
        });

        const chatmessage = chatbox.querySelector('.chatbox__messages');
        chatmessage.innerHTML = html;
    }
}

const chatbox = new Chatbox();
chatbox.display();
