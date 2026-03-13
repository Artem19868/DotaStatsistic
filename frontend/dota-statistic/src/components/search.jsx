import React from "react";

import searchIcon from '../assets/search-icon.png'

class Search extends React.Component{
    render(){
        return(
            <div id="search">
                <input type="text" placeholder={this.props.placeholder} className="search-input" />
                <div className="search-icon">
                    <img src={searchIcon} alt="Search icon" />
                </div>
            </div>
        )
    }
}

export default Search