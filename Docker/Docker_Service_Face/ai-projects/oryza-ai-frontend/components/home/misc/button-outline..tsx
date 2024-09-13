import React from "react";

const ButtonOutline = ({ children, onClick }: any) => {
  return (
    <button
      onClick={onClick}
      className="font-medium tracking-wide py-2 px-5 sm:px-8 border border-[#007dc0] text-[#007dc0] bg-white-500 outline-none rounded-l-full rounded-r-full capitalize hover:bg-[#007dc0] hover:text-white transition-all hover:shadow-orange "
    >
      {" "}
      {children}
    </button>
  );
};

export default ButtonOutline;
