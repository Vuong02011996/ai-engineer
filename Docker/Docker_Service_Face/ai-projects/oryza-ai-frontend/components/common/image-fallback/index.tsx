import Image, { ImageProps } from "next/image";
import { memo, useEffect, useState } from "react";

export interface IImageFallbackProps extends ImageProps {
  src: string;
  fallbackSrc: string;
}

function ImageFallback(props: IImageFallbackProps) {
  const { src, fallbackSrc, ...rest } = props;
  const [imgSrc, set_imgSrc] = useState<string>(src);

  useEffect(() => {
    set_imgSrc(src);
  }, [src]);

  return (
    <Image
      {...rest}
      src={imgSrc}
      onLoad={(event) => {
        const img = event.currentTarget;
        if (img.naturalWidth === 0) {
          set_imgSrc(fallbackSrc);
        }
      }}
      onError={() => {
        set_imgSrc(fallbackSrc);
      }}
    />
  );
}
export default memo(ImageFallback);
