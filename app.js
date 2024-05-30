class Chatbox {
  constructor() {
    this.args = {
      openButton: document.querySelector(".chatbox__button"),
      chatBox: document.querySelector(".chatbox__support"),
      sendButton: document.querySelector(".send__button"), //text send button
      sendImageButton: document.querySelector(".send__button_img"), //image send button
      input: document.querySelector("#imageInput"),
      display: document.querySelector(".displayImage"),
      img: document.querySelector("img"),
    };

    this.state = false;
    this.messages = [];
    this.imageURL = null; // Add imageURL property to the class
  }

  display() {
    const { openButton, chatBox, sendButton, input, sendImageButton } =
      this.args;

    openButton.addEventListener("click", () => this.toggleState(chatBox));

    sendButton.addEventListener("click", () => this.onSendButton(chatBox)); //text input

    sendImageButton.addEventListener("click", () =>
      //image input
      this.onImageSendButton(chatBox)
    );

    input.addEventListener("change", () => this.onImageChange());

    input.addEventListener("keyup", ({ key }) => {
      if (key === "Enter") {
        this.onSendButton(chatBox);
      }
    });
  }

  toggleState(chatbox) {
    this.state = !this.state;

    if (this.state) {
      chatbox.classList.add("chatbox--active");
    } else {
      chatbox.classList.remove("chatbox--active");
    }
  }

  onImageSendButton(chatbox) {
    const textField = chatbox.querySelector("input");
    const text1 = textField.value;

    //Check if there's an image URL and add it to the messages
    if (this.imageURL) {
      console.log("Hello", this.imageURL);
      const imgMsg = {
        name: "User",
        message: `<img src="${this.imageURL}" alt='User Image'/>`,
      };
      this.messages.push(imgMsg);
      this.imageURL = null; // Reset the imageURL after adding to messages
      this.args.display.innerHTML = ""; // Clear the image display in the footer bar
      // this.updateChatText(chatbox);
    }
    if (text1 !== "") {
      const textMsg = { name: "User", message: text1 };
      this.messages.push(textMsg);
    }

    fetch("http://127.0.0.1:5000/uploadImage", {
      method: "POST",
      body: "Research Me",
      mode: "cors",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((r) => r.json())
      .then((r) => {
        const msg2 = { name: "BotMe", message: r.answer };
        this.messages.push(msg2);
        this.updateChatText(chatbox);
        textField.value = "";
        // this.showInput(); // Show the input field after sending a message
      })
      .catch((error) => {
        console.error("Error:", error);
        this.updateChatText(chatbox);
        textField.value = "";
        this.showInput(); // Show the input field after an error
      });
  }

  onSendButton(chatbox) {
    const textField = chatbox.querySelector("input");
    const text1 = textField.value;

    if (text1 !== "") {
      const textMsg = { name: "User", message: text1 };
      this.messages.push(textMsg);
    }
    fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      body: JSON.stringify({ message: text1 }),
      mode: "cors",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => {
        if (response.ok) {
          if (response.headers.get("content-type").includes("image")) {
            return response.blob();
          } else {
            return response.json();
          }
        } else {
          throw new Error("Network response was not ok.");
        }
      })
      .then((data) => {
        if (data instanceof Blob) {
          // Handle image response
          const imageUrl = URL.createObjectURL(data);
          const imageMsg = {
            name: "BotMe",
            message: `<img src="${imageUrl}" alt='Bot Image'/>`,
          };
          this.messages.push(imageMsg);
          this.updateChatText(chatbox);
          textField.value = "";
          this.showInput(); // Show the input field after sending a message
        } else {
          // Handle text response
          const msg2 = { name: "BotMe", message: data.answer };
          console.log("msg2", msg2);
          this.messages.push(msg2);
          this.updateChatText(chatbox);
          textField.value = "";
          this.showInput(); // Show the input field after sending a message
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        this.updateChatText(chatbox);
        textField.value = "";
        this.showInput(); // Show the input field after an error
      });
  }

  updateChatText(chatbox) {
    let html = "";
    this.messages
      .slice()
      .reverse()
      .forEach(function (item) {
        if (item.name === "BotMe") {
          html +=
            '<div class="messages__item messages__item--visitor">' +
            item.message +
            "</div>";
        } else {
          html +=
            '<div class="messages__item messages__item--operator">' +
            item.message +
            "</div>";
        }
      });

    const chatmessage = chatbox.querySelector(".chatbox__messages");
    chatmessage.innerHTML = html;
  }

  onImageChange() {
    const { input, display } = this.args;

    let formData = new FormData();
    formData.append("image", input.files[0]);

    let reader = new FileReader();
    reader.readAsDataURL(input.files[0]);
    reader.addEventListener("load", () => {
      this.imageURL = reader.result; // Store the imageURL in the class

      if (!this.state) {
        display.innerHTML = `<img src="${reader.result}" alt=''/>`;
        this.uploadImageToServer(reader.result);
      }
    });

    fetch("http://127.0.0.1:5000/uploadImage", {
      method: "POST",
      body: formData,
      mode: "cors",
    })
      .then((r) => r.json())
      .catch((error) => {
        console.error("Error:", error);
        this.updateChatText(chatbox);
        textField.value = "";
        this.showInput(); // Show the input field after an error
      });
  }
}

// Call the functions
const chatbox = new Chatbox();
chatbox.display();
