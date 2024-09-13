import ImageFallback from "@/components/common/image-fallback";
import { IImage } from "@/interfaces/identification-profile/person";
import { Stack, Typography } from "@mui/material";
import Image from "next/image";
export interface IImageStackProps {
  images: IImage[];
}

export function ImageStack({ images }: IImageStackProps) {
  const imgCount = images.length;
  return (
    <Stack
      sx={{
        position: "relative",
        height: "80px",
        width: "100%",
      }}
    >
      {images.map((img, index) => {
        return (
          <Stack
            key={index}
            className="img-item"
            sx={{
              position: "absolute",
              height: "80px",
              width: "fit-content",
              left: 20 * index,
              zIndex: (20 * imgCount) / (index + 1),
              transition: "all .3s ease-in-out",
              display: index > 3 ? "none" : "block",
            }}
          >
            {index === 0 && imgCount > 1 && (
              <Typography
                className="image-number"
                sx={{
                  position: "absolute",
                  right: "0",
                  top: "50%",
                  transform: "translateY(-50%)",
                  color: "#fff",
                  transition: "all .3s ease-in-out",
                  fontWeight: 500,
                }}
              >
                +{imgCount}
              </Typography>
            )}
            <ImageFallback
              src={img.url}
              fallbackSrc={"/images/user.png"}
              alt="ung"
              width={500}
              height={300}
              style={{
                width: "100%",
                height: "100%",
                objectFit: "contain",
                background: "#f8f8f8",
              }}
            />
          </Stack>
        );
      })}
    </Stack>
  );
}
