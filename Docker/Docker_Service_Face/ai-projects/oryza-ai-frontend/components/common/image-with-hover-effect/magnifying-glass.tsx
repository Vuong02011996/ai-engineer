import React, { useState } from "react";
import Image from "next/image";

// Constants for magnifier size and zoom level
const MAGNIFIER_SIZE = 100;
const ZOOM_LEVEL = 2.5;

// ImageEffect component with styled components
const ImageEffect = ({ src }: any) => {
  // State variables
  const [zoomable, setZoomable] = useState(false);
  const [imageSize, setImageSize] = useState({ width: 0, height: 0 });
  const [position, setPosition] = useState({
    x: 100,
    y: 100,
    mouseX: 0,
    mouseY: 0,
  });

  // Event handlers
  const handleMouseEnter = (e: any) => {
    let element = e.currentTarget;
    let { width, height } = element.getBoundingClientRect();
    setImageSize({ width, height });
    setZoomable(true);
    updatePosition(e);
  };

  const handleMouseLeave = (e: any) => {
    setZoomable(false);
    updatePosition(e);
  };

  const handleMouseMove = (e: any) => {
    updatePosition(e);
  };

  const updatePosition = (e: any) => {
    const { left, top } = e.currentTarget.getBoundingClientRect();
    let x = e.clientX - left;
    let y = e.clientY - top;
    setPosition({
      x: -x * ZOOM_LEVEL + MAGNIFIER_SIZE / 2,
      y: -y * ZOOM_LEVEL + MAGNIFIER_SIZE / 2,
      mouseX: x - MAGNIFIER_SIZE / 2,
      mouseY: y - MAGNIFIER_SIZE / 2,
    });
  };

  // Render method
  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <div
        style={{
          width: `160px`,
          height: `90px`,
          // height: '100px',
          position: "relative",
          overflow: "hidden",
        }}
        onMouseLeave={(e) => handleMouseLeave(e)}
        onMouseEnter={(e) => handleMouseEnter(e)}
        onMouseMove={(e) => handleMouseMove(e)}
      >
        <Image
          style={{
            objectFit: "cover",
            border: "1px solid black",
            zIndex: 10,
          }}
          alt=""
          src={src}
          fill
        />
        <div
          style={{
            width: `100px`,
            height: `100px`,
            backgroundPosition: `${position.x}px ${position.y}px`,
            backgroundImage: `url(${src})`,
            backgroundSize: `${imageSize.width * ZOOM_LEVEL}px ${
              imageSize.height * ZOOM_LEVEL
            }px`,
            backgroundRepeat: "no-repeat",
            display: zoomable ? "block" : "none",
            top: `${position.mouseY}px`,
            left: `${position.mouseX}px`,
            // width: `${MAGNIFIER_SIZE}px`,
            // height: `${MAGNIFIER_SIZE}px`,
            zIndex: 50,
            border: "2px solid #808080",
            borderRadius: "50%",
            position: "absolute",
            pointerEvents: "none",
          }}
        />
      </div>
    </div>
  );
};

export default ImageEffect;
