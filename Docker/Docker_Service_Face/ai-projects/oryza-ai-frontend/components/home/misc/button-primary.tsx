import React from "react";

const ButtonPrimary = ({ children, addClass }: any) => {
  return (
    <button
      className={
        "py-3 lg:py-4 px-12 lg:px-16 text-white font-semibold rounded-lg bg-[#007dc0] hover:shadow-shadown1 transition-all outline-none hover:scale-105 " +
        addClass
      }
    >
      {children}
    </button>
  );
};

export default ButtonPrimary;
