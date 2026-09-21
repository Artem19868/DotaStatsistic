import React from "react";
import Header from "../src/components/header";
import Aside from "../src/components/aside";

class Heroes extends React.Component {
    render() {
        return (
            <>
                <div id="layout">
                    <Aside />
                    <div id="aside-header-container">
                    </div>

                    <main>
                        <Header />

                        <h1 onClick={this.props.getHeroData}>Dota stats</h1>

                        <p>Heroes page</p>
                    </main>

                </div>

            </>
        )
    }
}

export default Heroes