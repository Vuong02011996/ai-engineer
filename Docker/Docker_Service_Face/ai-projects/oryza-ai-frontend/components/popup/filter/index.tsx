import * as React from "react";
import { useState, useEffect } from "react";
import { useAnimate, stagger, motion } from "framer-motion";
import clsx from "clsx";

const staggerMenuItems = stagger(0.1, { startDelay: 0.15 });

function useMenuAnimation(isOpen: boolean) {
  const [scope, animate] = useAnimate();

  useEffect(() => {
    animate(".arrow", { rotate: isOpen ? 180 : 0 }, { duration: 0.2 });

    animate(
      "ul",
      {
        clipPath: isOpen
          ? "inset(-10% -10% -10% -10% round 10px)"
          : "inset(10% 50% 90% 50% round 10px)",
      },
      {
        type: "spring",
        bounce: 0,
        duration: 0.5,
      }
    );

    animate(
      "li",
      isOpen
        ? { opacity: 1, scale: 1, filter: "blur(0px)", x: 0 }
        : { opacity: 0, scale: 0.3, filter: "blur(20px)", x: 50 },
      {
        duration: 0.2,
        delay: isOpen ? staggerMenuItems : 0,
      }
    );
  }, [isOpen]);

  return scope;
}

export interface FilterComponentsProps {
  options: {
    id: number;
    name: string;
    key: string;
  }[];
  onChange?: (value: any) => void;
  value?: string;
}

export const FilterComponents = (props: FilterComponentsProps) => {
  const { options } = props;

  const [isOpen, setIsOpen] = useState(false);
  const scope = useMenuAnimation(isOpen);

  const [value, setValue] = useState(props?.value || "ALL");
  useEffect(() => {
    if (props?.value) {
      setValue(props?.value);
    }
  }, [props?.value]);

  const displayName = React.useCallback(() => {
    return options.find((i) => i.key === value)?.name ?? "";
  }, [value]);

  return (
    <div ref={scope} className="relative">
      <div
        onClick={() => setIsOpen(false)}
        className={clsx(
          "top-0 left-0 right-0 bottom-0 z-9999",
          isOpen ? "fixed" : "hidden"
        )}
      />
      <motion.div
        onClick={() => setIsOpen(!isOpen)}
        className={[
          "px-3 py-2 rounded-lg border-2 bg-white transition-all duration-300 h-10 flex flex-row items-center space-x-1 cursor-pointer",
          isOpen ? " border-[#78C6E7]" : "shadow-shadown1 border-transparent",
        ].join(" ")}
      >
        <p className="text-[#808080] text-[14px] font-normal truncate">
          Hiển thị:{" "}
          <span
            className={[
              " text-[14px] font-medium ",
              isOpen ? "text-primary" : "text-blackOz",
            ].join(" ")}
          >
            {displayName()}
          </span>
        </p>
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="10"
          height="6"
          viewBox="0 0 10 6"
          fill="none"
          className="arrow"
        >
          <path
            d="M0.333372 1.00013C0.332602 0.867717 0.371284 0.738071 0.444485 0.627725C0.517685 0.517378 0.622088 0.431331 0.744385 0.380553C0.86668 0.329775 1.00133 0.316567 1.13116 0.342614C1.26099 0.36866 1.38013 0.432781 1.47337 0.5268L5.00004 4.06013L8.52671 0.5268C8.65224 0.401264 8.8225 0.330739 9.00004 0.330739C9.08795 0.330739 9.17499 0.348053 9.25621 0.381694C9.33742 0.415334 9.41121 0.464641 9.47337 0.5268C9.53553 0.588959 9.58484 0.662753 9.61848 0.743967C9.65212 0.825182 9.66943 0.912228 9.66943 1.00013C9.66943 1.17767 9.59891 1.34793 9.47337 1.47347L5.47337 5.47347C5.34846 5.59763 5.1795 5.66733 5.00337 5.66733C4.82725 5.66733 4.65828 5.59763 4.53337 5.47347L0.533372 1.47347C0.47038 1.41172 0.420267 1.33809 0.385937 1.25684C0.351605 1.17559 0.333738 1.08834 0.333372 1.00013Z"
            fill={!isOpen ? "#323232" : "#007DC0"}
            className="transition-all duration-300"
          />
        </svg>
      </motion.div>

      <ul
        style={{
          pointerEvents: isOpen ? "auto" : "none",
          clipPath: "inset(10% 50% 90% 50% round 10px)",
        }}
        className={clsx(
          " absolute top-[55px] bg-white shadow-shadown1 rounded-lg overflow-x-hidden min-w-[135px] w-full z-9999 ",
          isOpen ? "" : "hidden"
        )}
      >
        {options.map((item) => {
          const isActive = item.key === value;
          return (
            <li
              key={item.id}
              onClick={() => {
                setValue(item.key);
                if (props.onChange) props.onChange(item.key);
              }}
              className={[
                "px-2 py-1   cursor-pointer flex flex-row items-center justify-between  transition-all duration-300 ",
                isActive ? "bg-[#55595d]  " : "bg-white hover:bg-[#F2F2F2]",
              ].join(" ")}
            >
              <p
                className={[
                  "font-medium text-[14px] ",
                  isActive ? "  text-white" : "  text-[#808080]",
                ].join(" ")}
              >
                {item.name}
              </p>
              {isActive && (
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="16"
                  height="16"
                  viewBox="0 0 16 16"
                  fill="none"
                >
                  <path
                    fillRule="evenodd"
                    clipRule="evenodd"
                    d="M13.8048 4.19526C14.0651 4.45561 14.0651 4.87772 13.8048 5.13807L7.13815 11.8047C6.87781 12.0651 6.45569 12.0651 6.19534 11.8047L2.86201 8.4714C2.60166 8.21107 2.60166 7.78893 2.86201 7.5286C3.12236 7.26827 3.54447 7.26827 3.80482 7.5286L6.66675 10.3905L12.862 4.19526C13.1223 3.93491 13.5445 3.93491 13.8048 4.19526Z"
                    fill="white"
                  />
                </svg>
              )}
            </li>
          );
        })}
      </ul>
    </div>
  );
};
