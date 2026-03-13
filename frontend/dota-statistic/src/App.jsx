import React from "react"
import { Routes, Route } from "react-router-dom";

import Home from '/pages/home';
import Heroes from "../pages/heroes";
import Items from "../pages/items";
import Matches from "../pages/matches";

import "./index.css";

class App extends React.Component{

  getHeroData(){
    const baseUrl = "http://127.0.0.1:8000/";
    const completeUrl = baseUrl +`api/hero/${42}`;

    fetch(completeUrl)
    .then((response) => response.json())
    .then((data) => {console.log(data)})
    .catch((error) => {
        console.error('Error fetching api data:', error);
     });
  }

  render(){
    return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/heroes" element={<Heroes getHeroData={this.getHeroData}/>} />
      <Route path="/items" element={<Items />} />
      <Route path="/matches" element={<Matches />} />
    </Routes>
    )
  }
  
}
  

export default App
