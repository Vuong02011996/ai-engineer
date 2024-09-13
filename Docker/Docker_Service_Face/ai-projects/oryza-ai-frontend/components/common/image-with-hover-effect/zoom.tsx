import React from "react";
import ReactImageMagnify from "react-image-magnify";

interface ImageMagnifyProps {
  src: string;
  alt: string;
}

const ImageMagnifyComponent: React.FC<ImageMagnifyProps> = (props) => {
  const { src, alt } = props;

  return (
    <ReactImageMagnify
      {...{
        smallImage: {
          alt: alt,
          isFluidWidth: true,
          src: src,
          sizes: "(min-width: 800px) 33.5vw, (min-width: 415px) 50vw, 100vw",
        },
        largeImage: {
          alt: "",
          src: src,
          width: 1000,
          height: 1000,
        },
        enlargedImageContainerDimensions: {
          width: "200%",
          height: "400%",
        },
        className: "magnify-handler",
        enlargedImageClassName: "magnify-image",
        imageClassName: "magnify-target",
        enlargedImageContainerClassName: "magnify-box",
        isHintEnabled: false,
      }}
    />
  );
};

export default ImageMagnifyComponent;
