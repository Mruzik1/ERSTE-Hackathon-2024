"use client";
import React, { useEffect } from 'react';
import CustomCursor from '@components/Cursors';
import NavbarMenu from '@components/NavbarMenu';
import Dashboard from "@components/Dashboard";
import Template from '@components/template';
import '@styles/globals.css';
import '@styles/Fonts.css';
import '@styles/globals.css';

const dashboard = ({ children }) => {


    return (
        <div id="wrapper">

            <div className="hidden md:flex">
                <CustomCursor />
            </div>

            <NavbarMenu />

            <div className="circle"></div>

            <main className='app'>
                <div className="panel blue">
                    <Dashboard />
                </div>
            </main>


        </div>
    );
}

export default dashboard;