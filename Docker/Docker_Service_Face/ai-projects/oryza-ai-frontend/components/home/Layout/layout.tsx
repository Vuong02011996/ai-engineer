import React from "react";
import Footer from "./footer";
import { Header } from "./header";

const Layout = ({ children }: any) => {
  return (
    <div className="bg-gradient-to-b  from-white to-[#323232]">
      <Header />
      {children}
      <Footer />
    </div>
  );
};

export default Layout;
