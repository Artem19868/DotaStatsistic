import React from "react";
import Header from "../src/components/header";
import Aside from "../src/components/aside";

class Matches extends React.Component {
    render() {
        return (
            <>
                <div id="layout">
                    <Aside />
                    <div id="aside-header-container">
                    </div>

                    <main>
                        <Header />

                        <h1>Dota stats</h1>

                        <p>Matches page</p>
                    </main>

                </div>

            </>
        )
    }
}

export default Matches