import "./App.css";
import { FiChevronDown, FiTrash, FiShare, FiPlusSquare } from "react-icons/fi";
import { SiBmw } from "react-icons/si";
import { SiToyota } from "react-icons/si";
import { SiDacia } from "react-icons/si";
import { SiMitsubishi } from "react-icons/si";

import { motion } from "framer-motion";
import { useState } from "react";
import Login from "./components/login";
import React from 'react';

import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import VehicleDetails from './components/VehicleDetails';
import Layout from './components/layout';
import MesRoutes from './MesRoutes';

function App() {
    return (
        <MesRoutes />
    );
}

export default App;
