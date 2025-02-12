import "./App.css";
import { FiChevronDown, FiTrash, FiShare, FiPlusSquare } from "react-icons/fi";
import { SiBmw } from "react-icons/si";
import { SiToyota } from "react-icons/si";
import { SiDacia } from "react-icons/si";
import { SiMitsubishi } from "react-icons/si";

import { motion } from "framer-motion";
import { useState } from "react";

// Composant StaggeredDropDown
const StaggeredDropDown = () => {
  const [open, setOpen] = useState(false);

  return (
    <div className="p-8 pb-56 flex items-center justify-center bg-white">
      <motion.div animate={open ? "open" : "closed"} className="relative">
        <button
          onClick={() => setOpen((pv) => !pv)}
          className="flex items-center gap-2 px-3 py-2 rounded-md text-indigo-50 bg-indigo-500 hover:bg-indigo-500 transition-colors"
        >
          <span className="font-medium text-sm">Marque</span>
          <motion.span variants={iconVariants}>
            <FiChevronDown />
          </motion.span>
        </button>

        <motion.ul
          initial={wrapperVariants.closed}
          variants={wrapperVariants}
          style={{ originY: "top", translateX: "-50%" }}
          className="flex flex-col gap-2 p-2 rounded-lg bg-white shadow-xl absolute top-[120%] left-[50%] w-48 overflow-hidden"
        >
          <Option setOpen={setOpen} Icon={SiBmw} text="Marque 1" />
          <Option setOpen={setOpen} Icon={SiToyota} text="Marque 2" />
          <Option setOpen={setOpen} Icon={SiDacia} text="Marque 3" />
          <Option setOpen={setOpen} Icon={SiMitsubishi} text="Marque 4" />
        </motion.ul>
      </motion.div>
    </div>
  );
};

// Composant Option
const Option = ({ text, Icon, setOpen }) => {
  return (
    <motion.li
      variants={itemVariants}
      onClick={() => setOpen(false)}
      className="flex items-center gap-2 w-full p-2 text-xs font-medium whitespace-nowrap rounded-md hover:bg-indigo-100 text-slate-700 hover:text-indigo-500 transition-colors cursor-pointer"
    >
      <motion.span variants={actionIconVariants}>
        <Icon />
      </motion.span>
      <span>{text}</span>
    </motion.li>
  );
};

// Variantes pour les animations
const wrapperVariants = {
  open: {
    scaleY: 1,
    transition: {
      when: "beforeChildren",
      staggerChildren: 0.1,
    },
  },
  closed: {
    scaleY: 0,
    transition: {
      when: "afterChildren",
      staggerChildren: 0.1,
    },
  },
};

const iconVariants = {
  open: { rotate: 180 },
  closed: { rotate: 0 },
};

const itemVariants = {
  open: {
    opacity: 1,
    y: 0,
    transition: {
      when: "beforeChildren",
    },
  },
  closed: {
    opacity: 0,
    y: -15,
    transition: {
      when: "afterChildren",
    },
  },
};

const actionIconVariants = {
  open: { scale: 1, y: 0 },
  closed: { scale: 0, y: -7 },
};

// Composant principal App
function App() {
  return (
    <>
      <h1 className="text-2xl font-bold mb-4">Bonjour</h1>

      <div className="flex items-center justify-center w-full">
        <label
          htmlFor="dropzone-file"
          className="flex flex-col items-center justify-center w-full h-48 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 dark:hover:bg-gray-800 dark:bg-gray-700 hover:bg-gray-100 dark:border-gray-600 dark:hover:border-gray-500"
        >
          <div className="flex flex-col items-center justify-center pt-5 pb-6">
            <svg
              className="w-8 h-8 mb-4 text-gray-500 dark:text-gray-400"
              aria-hidden="true"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 20 16"
            >
              <path
                stroke="currentColor"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 0 0 0 16 6.5 5.5 5.5 0 0 0 5.207 5.021C5.137 5.017 5.071 5 5 5a4 4 0 0 0 0 8h2.167M10 15V6m0 0L8 8m2-2 2 2"
              />
            </svg>
            <p className="mb-2 text-sm text-gray-500 dark:text-gray-400">
              <span className="font-semibold">Cliquez pour télécharger</span> ou
              glissez et déposer
            </p>
            <p className="text-xs text-gray-500 dark:text-gray-400">
              SVG, PNG, JPG or GIF (MAX. 800x400px)
            </p>
          </div>
          <input id="dropzone-file" type="file" className="hidden" />
        </label>
      </div>

      <div className="p-4 flex flex-col gap-4">
        <div className="flex gap-4 w-full">
          <StaggeredDropDown />
          <div>
            <input
              type="text"
              placeholder="Modele"
              className="border border-gray-400 p-3 rounded-sm"
            />
          </div>
        </div>

        <input
          type="text"
          placeholder="Prix"
          className="border border-gray-400 p-3 rounded-sm"
        />
        <input
          type="text"
          placeholder="Mileage"
          className="border border-gray-400 p-3 rounded-sm"
        />
        <input
          type="text"
          placeholder="Type d'energie"
          className="border border-gray-400 p-3 rounded-sm"
        />
        <input
          type="text"
          placeholder="Description"
          className="border border-gray-400 p-3 rounded-sm"
        />
      </div>
    </>
  );
}

export default App;
