import { useState } from "react";
import axios from "axios";

function App() {

  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([]);

  const sendMessage = async () => {

    if (!message.trim()) return;

    // User message
    const userMessage = {
      sender: "You",
      text: message
    };

    setChat(prev => [...prev, userMessage]);

    try {

      const res = await axios.post(
        "http://127.0.0.1:8000/chat",
        {
          message: message
        }
      );

      // AI response
      const aiMessage = {
        sender: "AI",
        text: res.data.response
      };

      setChat(prev => [...prev, aiMessage]);

    } catch (error) {

      console.log(error);

    }

    setMessage("");
  };

  return (

    <div style={{ padding: "20px" }}>

      <h1>Emotion Companion</h1>

      <div>

        {
          chat.map((msg, index) => (

            <div key={index}>

              <b>{msg.sender}: </b>
              {msg.text}

            </div>

          ))
        }

      </div>

      <br />

      <input
        type="text"
        placeholder="Type here..."
        value={message}
        onChange={(e) => setMessage(e.target.value)}
      />

      <button onClick={sendMessage}>
        Send
      </button>

    </div>
  );
}

export default App;