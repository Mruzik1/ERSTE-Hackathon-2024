// template.js

"use client";

import { useEffect } from "react";
import { animatePageIn } from "@utils/animation";

export default function Template({ children }) {
  useEffect(() => {
    animatePageIn();
  }, []);

  return (
    <>
      <div
        id="banner-1"
        style={{ width: "12.5%", left: "0%", backgroundColor: "#3F3C38" }}
        className="min-h-screen bg-neutral-950 z-[9999] fixed top-0"
      />
      <div
        id="banner-2"
        style={{ width: "12.5%", left: "12.5%", backgroundColor: "#3F3C38" }}
        className="min-h-screen bg-neutral-950 z-[9999] fixed top-0"
      />
      <div
        id="banner-3"
        style={{ width: "12.5%", left: "25%", backgroundColor: "#3F3C38" }}
        className="min-h-screen bg-neutral-950 z-[9999] fixed top-0"
      />
      <div
        id="banner-4"
        style={{ width: "12.5%", left: "37.5%", backgroundColor: "#3F3C38" }}
        className="min-h-screen bg-neutral-950 z-[9999] fixed top-0"
      />
      <div
        id="banner-5"
        style={{ width: "12.5%", left: "50%", backgroundColor: "#3F3C38" }}
        className="min-h-screen bg-neutral-950 z-[9999] fixed top-0"
      />
      <div
        id="banner-6"
        style={{ width: "12.5%", left: "62.5%", backgroundColor: "#3F3C38" }}
        className="min-h-screen bg-neutral-950 z-[9999] fixed top-0"
      />
      <div
        id="banner-7"
        style={{ width: "12.5%", left: "75%" , backgroundColor: "#3F3C38"}}
        className="min-h-screen bg-neutral-950 z-[9999] fixed top-0"
      />
      <div
        id="banner-8"
        style={{ width: "12.5%", left: "87.5%", backgroundColor: "#3F3C38" }}
        className="min-h-screen bg-neutral-950 z-[9999] fixed top-0"
      />
      {children}
    </>
  );
}