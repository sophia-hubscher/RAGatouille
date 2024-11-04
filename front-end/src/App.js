//import logo from './logo.svg';
//import './App.css';
import React, { useState } from "react";
import styled, { ThemeProvider, keyframes } from "styled-components";

//Char Limit
const maxLength = 1000;

//THEMES
const lightTheme = {
  background: "#ffffff",
  textColor: "#000000",
  headerBackground: "#2394d9",
  messageBackgroundUser: "#2394d9",
  messageBackgroundBot: "#e9ecef",
};

const darkTheme = {
  background: "#1a1a1a",
  textColor: "#ffffff",
  headerBackground: "#2394d9",
  messageBackgroundUser: "#2394d9",
  messageBackgroundBot: "#555555",
};

const dotFlashing = keyframes`
  0% {
    opacity: 0.2;
  }
  20% {
    opacity: 1;
  }
  100% {
    opacity: 0.2;
  }
`;

const LoadingDots = styled.div`
  display: inline-flex;
  align-items: center;
  justify-content: center;

  & span {
    width: 8px;
    height: 8px;
    margin: 0 2px;
    background-color: ${(props) => props.theme.textColor};
    border-radius: 50%;
    animation: ${dotFlashing} 1s infinite linear;
  }

  & span:nth-child(1) {
    animation-delay: 0s;
  }
  & span:nth-child(2) {
    animation-delay: 0.2s;
  }
  & span:nth-child(3) {
    animation-delay: 0.4s;
  }
`;

const ChatContainer = styled.div`
  paddingleft: 50px;
  border: 1px solid #ddd;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background: ${(props) => props.theme.background};
  color: ${(props) => props.theme.textColor};
  height: 100vh;
`;

const Header = styled.div`
  background: ${(props) => props.theme.headerBackground};
  color: white;
  padding: 20px;
  text-align: center;
  font-family: Arial, Helvetica, sans-serif;
  font-weight: bold;
  font-size: 2vw;
  position: relative;
`;

//This is just for the title of the website because I wanted the switch themes button
//up top with it but not centered
const Title = styled.div`
  text-align: center;
`;

const MessagesContainer = styled.div`
  padding: 20px;
  flex-grow: 1;
  display: flex;
  flex-direction: column-reverse;
  justify-content: flex-start;
  overflow: auto;
  height: 80vh;
  scroll-behavior: smooth;
`;

const Message = styled.div`
  background: ${(props) =>
    props.isBot
      ? props.theme.messageBackgroundBot
      : props.theme.messageBackgroundUser};
  color: ${(props) => (props.isBot ? props.theme.textColor : "#fff")};
  padding: 10px;
  border-radius: 10px;
  margin: 5px 0;
  align-self: ${(props) => (props.isBot ? "flex-start" : "flex-end")};
  float: ${(props) => (props.isBot ? "left" : "right")};
  overflow-wrap: break-word;
  max-width: 75%;
  font-family: Arial, Helvetica, sans-serif;
  white-space: pre-wrap;
`;

const InputContainer = styled.div`
  display: flex;
  border-top: 1px solid ${(props) => props.theme.textColor};
  padding: 10px;
  background-color: ${(props) => props.theme.background};
  border-radius: 10px;
`;

const TextInput = styled.textarea`
  width: 100%;
  padding: 15px;
  border: 1px solid ${(props) => props.theme.textColor};
  border-radius: 10px;
  outline: none;
  display: flex;
  overflow-wrap: break-word;
  resize: none;
  margin-right: 10px;
  background-color: ${(props) => props.theme.background};
  color: ${(props) => props.theme.textColor};
`;

const SendButton = styled.button`
  background: ${(props) => props.theme.headerBackground};
  color: white;
  padding: 15px 20px;
  border: none;
  cursor: pointer;
  outline: none;
  border-radius: 10px;
  font-weight: bold;
  transition: background 0.3s;
  &:hover {
    background: #1a73e8;
  }
`;

const CharCount = styled.div`
  text-align: center;
  color: ${(props) => (props.remaining < 0.05 * maxLength ? "red" : "green")};
  font-size: 12px;
  padding: 10px 1px;
  background: ${(props) => props.theme.background};
`;

const ThemeToggleButton = styled.button`
  background: none;
  border: none;
  color: white;
  font-size: 1em;
  cursor: pointer;
  position: absolute;
  top: 50%;
  right: 20px;
  transform: translateY(-50%);
`;

const App = () => {
  const [messages, setMessages] = useState([
    { text: "Hello! How can I assist you today?", isBot: true },
  ]);
  const [userInput, setUserInput] = useState("");
  const [theme, setTheme] = useState(darkTheme);
  const [loading, setLoading] = useState(false);

  // Function to call the back-end API
  const fetchRetrievedInfo = async (user_query) => {
    try {
      const response = await fetch("http://127.0.0.1:5000/retrieve", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ user_query: user_query }), // Change this line
      });
      const data = await response.json();
      return data.retrievedInfo;
    } catch (error) {
      console.error("Error fetching retrieved info:", error);
      return "Sorry, there was an error retrieving the information.";
    }
  };

  // Handle sending a new message
  const handleSendMessage = async () => {
    if (userInput.trim()) {
      const userMessage = { text: userInput, isBot: false };
      setMessages([userMessage, ...messages]);
      setUserInput("");

      //shows animation
      setLoading(true);

      // Fetch retrieved information from the back-end
      const retrievedInfo = await fetchRetrievedInfo(userInput);
      const botMessage = { text: retrievedInfo, isBot: true };
      setLoading(false);
      setMessages((prevMessages) => [botMessage, ...prevMessages]);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      if (e.ctrlKey) {
        // Ctrl + Enter makes new line
        const cursorPos = e.target.selectionStart;
        setUserInput(
          userInput.slice(0, cursorPos) + "\n" + userInput.slice(cursorPos)
        );
        setTimeout(() => {
          e.target.selectionStart = e.target.selectionEnd = cursorPos + 1;
        }, 0);
      } else {
        e.preventDefault();
        handleSendMessage();
      }
    }
  };

  const toggleTheme = () => {
    setTheme(theme === darkTheme ? lightTheme : darkTheme);
  };

  return (
    <ThemeProvider theme={theme}>
      <ChatContainer>
        <Header>
          <Title>ISOtope's RAGatouille Chatbot</Title>
          <ThemeToggleButton onClick={toggleTheme}>
            {theme === darkTheme ? "🌙 Dark Mode" : "☀️ Light Mode"}
          </ThemeToggleButton>
        </Header>
        <MessagesContainer>
          {loading && (
            <Message isBot={true}>
              <LoadingDots>
                <span></span>
                <span></span>
                <span></span>
              </LoadingDots>
            </Message>
          )}
          {messages.map((msg, index) => (
            <Message key={index} isBot={msg.isBot}>
              {msg.text}
            </Message>
          ))}
        </MessagesContainer>
        <InputContainer>
          <TextInput
            type="text"
            maxLength={maxLength}
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
            placeholder="Type your message..."
            onKeyDown={handleKeyPress}
          />
          <CharCount remaining={maxLength - userInput.length}>
            {maxLength - userInput.length} Characters Remaining
          </CharCount>
          <SendButton onClick={handleSendMessage}>Send</SendButton>
        </InputContainer>
      </ChatContainer>
    </ThemeProvider>
  );
};

export default App;
