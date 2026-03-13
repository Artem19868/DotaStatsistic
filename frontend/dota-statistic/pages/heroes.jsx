import React from "react";
import Header from "../src/components/header";

class Heroes extends React.Component{
    render(){
        return(
        <>
            <Header />
            <h1 onClick={this.props.getHeroData}>Dota stats</h1>
            <p>Heroes page</p>
        </>
        )
    }
}

export default Heroes