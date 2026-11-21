import React from "react"
import { Routes, Route } from "react-router-dom";

import Home from '/pages/home';
import Heroes from "../pages/heroes";
import HeroPage from "../pages/hero_page";
import Items from "../pages/items";
import Matches from "../pages/matches";

import "./index.css";

function App(){
    return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/heroes" element={<Heroes/>} />
      <Route path="/hero/:heroId" element={<HeroPage/>} />
      <Route path="/items" element={<Items />} />
      <Route path="/matches" element={<Matches />} />
    </Routes>
    )
  
}
  

export default App
