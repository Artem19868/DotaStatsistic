import React from "react";
import { Link } from "react-router-dom";
import Search from "./search";

function Header(){
    return (<header id="header">
            <Search placeholder="Search player by Steam id" />
            <p>Track your</p>
            <p>Dota 2 <span className="purple-text">perfomance</span></p>

            <p>Advanced statistics. Better insights. Climb higher</p>
        </header>)
}

export default Header