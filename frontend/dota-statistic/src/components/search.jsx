import React from "react";

import searchIcon from '../assets/search.png'

class Search extends React.Component{
    render(){
        return(
            <div id="search">
                <div className="search-container">
                    {/* <img className="search-icon" src={searchIcon} alt="Search icon" /> */}
                    <input type="text" placeholder={this.props.placeholder} className="search-input" />
                </div>
                

                <button className="search-button" type="submit">Search</button>
            </div>
        )
    }
}

export default Search