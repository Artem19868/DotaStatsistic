import React from "react";
import { NavLink } from "react-router-dom";

class Aside extends React.Component {
    render() {
        return (<aside id="aside">
            <div className="container">
                <img src="/dota-icon.svg" alt="Dota 2 icon" className="icon"/>

                <div>
                    <h3>Dota Stats</h3>
                    <p>Insights. Analize. Win</p>
                </div>

            </div>

            <ul id="side-bar">
                <li className="aside-navigation">
                    <div className="link-container">
                     <NavLink to={`/`} className={({ isActive }) =>
                        isActive ? "nav-link active-link" : "nav-link"
                     }>Home</NavLink>   
                    </div>
                </li>
                <li className="aside-navigation">
                    <div className="link-container">
                        <NavLink to={`/heroes`} className={({ isActive }) =>
                        isActive ? "nav-link active-link" : "nav-link"
                     }>Heroes</NavLink>
                    </div>
                </li>
                <li className="aside-navigation">
                    <div className="link-container">
                        <NavLink to={`/matches`} className={({ isActive }) =>
                        isActive ? "nav-link active-link" : "nav-link"
                     }>Matches</NavLink>
                    </div>
                </li>
                <li className="aside-navigation">
                    <div className="link-container">
                        <NavLink to={`/items`} className={({ isActive }) =>
                        isActive ? "nav-link active-link" : "nav-link"
                     }>Items</NavLink>
                    </div>
                </li>

                {/* make this in future */}

                {/* <li className="aside-navigation">
                    <div className="link-container">
                        <NavLink to={`/meta`} className={({ isActive }) =>
                        isActive ? "nav-link active-link" : "nav-link"
                     }>Meta</NavLink>
                    </div>
                </li>
                <li className="aside-navigation">
                    <div className="link-container">
                        <NavLink to={`/rankings`} className={({ isActive }) =>
                        isActive ? "nav-link active-link" : "nav-link"
                     }>Rankings</NavLink>
                    </div>
                </li> */}
            </ul>
        </aside>)
    }
}

export default Aside