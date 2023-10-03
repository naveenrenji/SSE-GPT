import React, { useState, useEffect, useRef } from "react";
import "./ChatBot.css";
import axios from "axios";
import botAvatar from "../../carloavatar.jpeg"; // Import your bot avatar image here

function ChatBot() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [context, setContext] = useState("");
  const messagesEndRef = useRef(null);
  const [isLoading, setIsLoading] = useState(false); // New state for loading animation

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    localStorage.setItem("chatMessages", JSON.stringify(messages));
    localStorage.setItem("chatContext", JSON.stringify(context));
    scrollToBottom();
  }, [messages, context]);

  const clearChat = () => {
    setMessages([]);
    setContext("");
    localStorage.removeItem("chatMessages");
    localStorage.removeItem("chatContext");
  };

  const sendMessage = async (e) => {
    e.preventDefault();
    setIsLoading(true); // Start loading animation
    if (input.trim().length === 0) {
      setErrorMessage("Please enter your message first");
      setIsLoading(false); // Stop loading animation
      return;
    }
    try {
      const response = await axios.post("http://127.0.0.1:5000/chat", {
        message: input,
        context,
      });
      setIsLoading(false); // Stop loading animation
      let messagedata = [
        {
          sender: "Carlo Lipizzi",
          content: "I am too tired right now, can we talk later?",
        },
      ];
      if (response.data.response) {
        messagedata = [
          {
            sender: "user",
            content: input,
          },
          {
            sender: "Carlo Lipizzi",
            content: response.data.response,
          },
        ];
      }

      setMessages([...messages, ...messagedata]);
      setInput("");
      setErrorMessage("");
    } catch (error) {
      console.error("There was an error sending the message", error);
      setErrorMessage("There was an error sending the message");
    } finally {
      setIsLoading(false); // Stop loading animation in either case
    }
  };

  return (
    <div className="chat-container">
      <h1 className="chat-title">SSE - EduBot</h1>
      <h2 className="chat-subtitle">
        Your Advanced Secure and Scalable Chatbot Ecosystem
      </h2>
      <div className="clear-chat-button">
        {messages.length > 0 && (
          <button className="clear-button" onClick={clearChat}>
            Clear Chat
          </button>
        )}
      </div>
      <div className="chat-messages">
        {messages.map((message, index) => (
          <div className={`chat-message-wrapper ${message.sender}`} key={index}>
            {message.sender === "Carlo Lipizzi" && (
              <img src={botAvatar} alt="Bot Avatar" className="bot-avatar" />
            )}
            <p className={`chat-message ${message.sender}`}>
              {message.content}
            </p>
          </div>
        ))}
        {isLoading && (
          <div className="loading-animation">Generating response...</div>
        )}
        {/* {isLoading && (
          <div className="loading-animation">
            <div></div>
            <div></div>
            <div></div>
          </div>
        )} */}

        <div ref={messagesEndRef} />
      </div>
      {!isLoading && (
      <form onSubmit={sendMessage} className="chat-form">
        <input
          className="chat-input"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Enter your message"
          disabled={isLoading} // Disable input during loading
        />
        <button className="chat-button" type="submit" disabled={isLoading}>
          Submit
        </button>
      </form>)}
      {errorMessage && <p className="error-message">{errorMessage}</p>}
    </div>
  );
}

export default ChatBot;
