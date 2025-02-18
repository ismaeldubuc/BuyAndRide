import "./App.css";
import { FiChevronDown, FiTrash, FiShare, FiPlusSquare } from "react-icons/fi";
import { SiBmw } from "react-icons/si";
import { SiToyota } from "react-icons/si";
import { SiDacia } from "react-icons/si";
import { SiMitsubishi } from "react-icons/si";

import { motion } from "framer-motion";
import { useState } from "react";
import Login from "./components/Login";
import Register from "./components/Register";
import Annonce from "./components/Annonce";

function App() {
  return (
    <>
      <Register />
      <Annonce />
    </>
  );
}

export default App;
