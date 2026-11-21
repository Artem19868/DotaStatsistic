import React, { useEffect, useState } from "react";
import Header from "../src/components/header";
import Aside from "../src/components/aside";
import { Link, useParams } from "react-router-dom";

function HeroPage() {
    const { heroId } = useParams();
    const [data, setData] = useState(null);

    useEffect(() => {
    const baseUrl = "http://127.0.0.1:8000/";
    const completeUrl = baseUrl +`api/hero/${heroId}`;

    fetch(completeUrl)
    .then((response) => response.json())
    .then(data => setData(data))
    .catch((error) => {
        console.error('Error fetching api data: ', error);
     });
    }, [heroId]);


    return (
        <>
            <div id="layout">
                <Aside />
                <div id="aside-header-container">
                </div>

                <main>
                    <Header />
                    <div>
                        <p>hero with id {data?.[0]?.pk}</p>
                        {data?.[0]?.fields?.display_name}
                        <img src={data?.[0]?.fields?.image_url} alt="hero image" />
                    </div>

                    <p>Heroes page</p>
                </main>

            </div>

        </>
    );
}

export default HeroPage;