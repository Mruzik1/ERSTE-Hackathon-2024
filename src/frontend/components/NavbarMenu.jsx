"use client"
import React, { useState, useEffect } from 'react';
import Image from 'next/image';
import Link from 'next/link';
import { AiOutlineClose, AiOutlineMail, AiOutlineMenu } from "react-icons/ai";
import { FaGithub, FaLinkedinIn } from 'react-icons/fa'
import { BsFillPersonLinesFill, BsHouseAdd } from 'react-icons/bs'

const NavbarMenu = () => {

    return (
        <div className='flex w-full justify-center'>
            <div className="fixed gap-5 max-w-7xl mt-10 h-16 bg-[#FF6D40] shadow-lg flex items-center justify-evenly rounded-lg p-5 py-10 ">

                {/* Логотип */}
                <img 
                        src="https://cdn0.erstegroup.com/content/dam/at/ed/www_erstedigital_com/hackathon/EDLogo.png"
                        alt="Erste Digital Logo"
                        width={100} // задайте подходящие размеры
                        height={30} // можно настроить по необходимости
                        className='p-1'
                />

                {/* Навигация */}
                <div className="flex space-x-6 px-10 font-semibold">
                    <div href="#introduction">
                        <a className="text-white hover:text-gray-200">Introduction</a>
                    </div>
                    <div href="#apis">
                        <a className="text-white hover:text-gray-200">APIs</a>
                    </div>
                    <div href="#datasets">
                        <a className="text-white hover:text-gray-200">Datasets</a>
                    </div>
                    <div href="#solutions">
                        <a className="text-white hover:text-gray-200">Solutions</a>
                    </div>
                    <div href="#projects">
                        <a className="text-white hover:text-gray-200">Template projects</a>
                    </div>
                    <div href="#design-system">
                        <a className="text-white hover:text-gray-200">Design system</a>
                    </div>
                    <div href="#psd2-related">
                        <a className="text-white hover:text-gray-200">PSD2 related</a>
                    </div>
                    <div href="#erste-digital">
                        <a className="text-white hover:text-gray-200">Erste Digital</a>
                    </div>
                </div>

                {/* Поиск и вход */}
                <div className="flex items-center space-x-4 border-l-2 border-white pl-3">
                    <button className="text-white hover:text-gray-200 flex items-center">
                        <span className="mr-1">🔍</span> Search
                    </button>
                    <button className="bg-white text-orange-500 font-bold py-1 px-4 rounded-lg hover:bg-gray-100">
                        Login
                    </button>
                </div>
            </div>
        </div>
    );
}
export default NavbarMenu;



