import { IPerson } from "@/interfaces/identification-profile/person";
import { Stack } from "@mui/material";
import { ImageComponent } from "./image";
import { ImageUpdateComponent } from "./image-update";
import { Errortext, Helptext, LabelImage } from "./ui";

export interface IChooseImageProps {
  data?: IPerson;
  textError?: string;
  setFiles: any;
  files: any[];
}

export function ChooseImageUniform(props: IChooseImageProps) {
  console.log("props.data: ", props.data);

  return (
    <Stack>
      <LabelImage />
      <Stack>
        {props.data ? (
          <ImageUpdateComponent data={props.data} />
        ) : (
          <ImageComponent setFiles={props.setFiles} files={props.files} />
        )}

        {props.textError ? <Errortext error={props.textError} /> : <Helptext />}
      </Stack>
    </Stack>
  );
}
