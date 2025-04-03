import { useState } from "react";
import { IoSend } from "react-icons/io5";

function ChatIA() {
  const [messages, setMessages] = useState([
    {
      text: "Bonjour, je suis l'IA de Buy and Ride. Posez-moi une question !",
      sender: "bot",
    },
  ]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    if (!input.trim()) return;

    // Ajouter le message utilisateur
    const userMessage = { text: input, sender: "user" };
    setMessages((prev) => [...prev, userMessage]);

    // Afficher les trois petits points en attendant la réponse
    setMessages((prev) => [...prev, { text: "...", sender: "bot" }]);

    try {
      // Envoyer la requête à l'API Flask
      const response = await fetch("http://127.0.0.1:8000/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question: input }),
      });

      if (!response.ok) {
        throw new Error("Erreur serveur");
      }

      const data = await response.json();

      // Supprimer les trois petits points et afficher la vraie réponse
      setMessages((prev) => [
        ...prev.slice(0, -1),
        { text: data.response, sender: "bot" },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev.slice(0, -1),
        {
          text: error.message || "Erreur de connexion avec l'IA.",
          sender: "bot",
        },
      ]);
    }

    setInput("");
  };

  return (
    <div className="h-screen flex flex-col bg-gray-100">
      <div className="flex-1 p-4 space-y-2 flex flex-col justify-end">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`p-3 rounded-lg max-w-[70%] break-words ${
              msg.sender === "user"
                ? "bg-blue-500 text-white ml-auto"
                : "bg-gray-300 text-black"
            }`}
          >
            {msg.text}
          </div>
        ))}
      </div>

      <div className="p-4 bg-white shadow-md flex items-center gap-2">
        <input
          type="text"
          className="flex-1 p-2 border rounded-lg"
          placeholder="Écrivez votre question..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        />
        <button
          onClick={sendMessage}
          className="p-2 bg-blue-500 text-white rounded-lg"
        >
          <IoSend />
        </button>
      </div>
    </div>
  );
}

export default ChatIA;
