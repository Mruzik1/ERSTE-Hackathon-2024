"use client";
import React, { useEffect, useRef } from 'react';
import '@styles/Fonts.css';
import '@styles/globals.css';
import '@styles/home_button.css';

import Clef from '@models/Clef';
import { Canvas } from '@react-three/fiber';
import '@styles/Light_style.css'
import { AiOutlineClose, AiOutlineMail, AiOutlineMenu } from "react-icons/ai";
import { FaGithub, FaLinkedinIn } from 'react-icons/fa'
import { BsFillPersonLinesFill, BsHouseAdd } from 'react-icons/bs'

import SplitType from 'split-type';
import gsap from 'gsap';

import { ScrollTrigger } from 'gsap/dist/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

const Main = () => {
    const refs = [useRef(null), useRef(null), useRef(null), useRef(null), useRef(null), useRef(null)];

    useEffect(() => {
        const createAnimation = (ref, timeline, params) => {
            const typeSplit = new SplitType(ref.current, {
                types: params.types,
                tagName: 'span'
            });

            const elements = typeSplit[params.types];
            gsap.set(elements, { y: '100%', opacity: 0 });

            timeline.to(elements, {
                y: params.y,
                opacity: 1,
                duration: params.duration,
                ease: params.ease,
                stagger: params.stagger,
            });

            return typeSplit;
        };

        const getAnimationParams = () => {
            if (window.innerWidth <= 768) {
                return [
                    { duration: 0, ease: 'power4.out', stagger: 0.5, types: 'words', y: '0%', start: "top 0%", end: "top 0%" },
                    { duration: 0, ease: 'power4.out', stagger: 0.4, types: 'words', y: '0%', start: "top 20%", end: "top 0%" },
                    { duration: 0, ease: 'power4.out', stagger: 0.4, types: 'words', y: '0%', start: "top -10%", end: "top -50%" },
                    { duration: 0.4, ease: 'expo.out', stagger: 0, types: 'lines', y: '0%', start: "top 20%", end: "top 0%" },
                    { duration: 0.1, ease: 'expo.out', stagger: 0, types: 'lines', y: '0%', start: "top 60%", end: "top 50%" },
                    { duration: 0.1, ease: 'expo.out', stagger: 0, types: 'lines', y: '0%', start: "top 60%", end: "top 50%" }
                ];
            } else {
                return [
                    { duration: 0.5, ease: 'power4.out', stagger: 0.4, types: 'words', y: '0%', start: "top 10%", end: "top 10%" },
                    { duration: 0.8, ease: 'power4.out', stagger: 0.3, types: 'words', y: '0%', start: "top 35%", end: "top -10%" },
                    { duration: 0.08, ease: 'expo.out', stagger: 0.3, types: 'lines', y: '0%', start: "top 0%", end: "top -50%" },
                    { duration: 0.2, ease: 'expo.out', stagger: 0, types: 'lines', y: '0%', start: "top 50%", end: "top 40%" },
                    { duration: 0.1, ease: 'expo.out', stagger: 0, types: 'lines', y: '0%', start: "top 70%", end: "top 60%" },
                    { duration: 0.1, ease: 'expo.out', stagger: 0, types: 'lines', y: '0%', start: "top 70%", end: "top 60%" }
                ];
            }
        };

        const tl = gsap.timeline({ delay: 1.6 });
        const animationParams = getAnimationParams();

        const splitTypes = refs.map((ref, index) => createAnimation(ref, tl, animationParams[index]));

        refs.forEach((ref, index) => {
            let params = animationParams[index];
            ScrollTrigger.create({
                trigger: ref.current,
                start: params.start,
                end: params.end,
                // markers: 'true',
                onUpdate: (self) => {
                    gsap.to(ref.current, { opacity: 1 - self.progress, ease: 'power1.out', duration: 0.35 });
                }
            });
        });

        return () => {
            splitTypes.forEach(typeSplit => typeSplit.revert());
        };
    }, []);

    return (
        <div id="Home">
            <div className=' gradient-background w-full h-auto mx-auto p-2  justify-center items-center'>
                <div className="flex flex-col gap-16 justify-center items-center h-full w-full md:text-center xs:text-left">

                    <div className='flex md:flex-row flex-col gap-0 md:gap-20 justify-between pt-20 '>
                        <div className="text-[#ffffff]   flex flex-col justify-center  font-extrabold text-start xs:text-8xl">
                            <div className='flex felx-row gap-5'>
                                <div className='text-[6vw] text-[#2f2f2f]'>Erste</div>
                                <div className='text-[6vw] text-[#2f2f2f]'>Digital</div>
                            </div>
                            <div className='text-[5vw] pt-5 text-[#2f2f2f]'> <span className='text-[#FF6D40]'>AI </span>  Dashboard </div>
                        </div>

                        <div className='relative' style={{ overflow: 'visible' }}>
                            <Canvas
                                ref={refs[2]}
                                className="absolute top-0 left-0 overflow-visible"
                                style={{ width: '300px', height: '300px' }}
                                camera={{
                                    position: [0, -1, 5],
                                    fov: 60,
                                    rotation: [(3 * Math.PI) / 180, 0, 0],
                                }}
                            >
                                {/* Главный источник красного света */}
                                <ambientLight color="#FF6D40" intensity={12} />

                                {/* Дополнительный свет с белым цветом для баланса */}
                                <ambientLight color="#FF6D40" intensity={0.1} />

                                {/* Точечный свет для создания акцентов */}
                                <pointLight position={[0, 1, 2]} color="#FF6D40" intensity={1} />

                                {/* Ваш объект */}
                                <Clef position={[0, 0, -4]} scale={[-4, 4, 4]} />
                            </Canvas>

                        </div>

                    </div>

                    <div className='flex gap-10 flex-row mt-20'>
                        <button id="bottone1"><strong className='text-white uppercase font-semibold'>About Us</strong></button>

                        <div className='flex flex-row  gap-8'>
                            <button id="bottone1"><strong className='text-white uppercase font-semibold'>Read Documentation and FAQ </strong></button>
                            <a href="http://localhost:3000/dashboard"><button id="bottone1"><strong className='text-white uppercase font-semibold'>Go to AI Dashboard</strong></button></a>
                        </div>

                    </div>
                
                </div>
            </div>

        </div>
    )

}

export default Main