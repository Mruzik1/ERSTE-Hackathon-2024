"use client";
import React, { useEffect } from 'react';
import CustomCursor from '@components/Cursors';
import NavbarMenu from '@components/NavbarMenu';
import Main from "@components/Main";
import Template from '@components/template';
import '@styles/globals.css';

const Home = ({ children }) => {


    return (
        <Template>
            <div id="wrapper">

                <div className="hidden md:flex">
                    <CustomCursor />
                </div>

                <NavbarMenu />

                <div className="circle"></div>

                <main className='app'>
                    <div className="panel blue">
                        <Main />
                    </div>
                </main>


            </div>
        </Template>
    );
}

export default Home;