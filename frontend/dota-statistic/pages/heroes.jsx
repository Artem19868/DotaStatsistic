import React, { useEffect, useState } from "react";
import Header from "../src/components/header";
import Aside from "../src/components/aside";
import { Link, useParams } from "react-router-dom";

function Heroes() {
    const [data, setData] = useState([]);

    useEffect(() => {
        const url = "http://127.0.0.1:8000/api/heroes"
        fetch(url)
            .then((response) => response.json())
            .then((data) => setData(data))
            .catch((error) => console.log('error at fething API: ', error))
    }, []);
    return (
        <>
            <div id="layout">
                <Aside />
                <div id="aside-header-container">
                </div>

                <main>
                    <Header />

                    <p to="/hero/42">Dota stats</p>

                    <p>Heroes page</p>
                    <ul>
                        {data.map(hero => (
                        <Link to={"/hero/" + hero?.pk}>
                                <li>
                                    <p>hero with id {hero?.pk}</p>
                                    {hero?.fields?.display_name}
                                    <img src={hero?.fields?.image_url} alt="hero image" />
                                </li>
                            </Link>

                        ))}
                    </ul>

                </main>

            </div>

        </>
    );
}


export default Heroes;