import { IPerson } from "@/interfaces/identification-profile/person";
import { Stack } from "@mui/material";
import { ImageComponent } from "./image";
import { ImageUpdateComponent } from "./image-update";
import { Errortext, Helptext, LabelImage } from "./ui";
import { FileInterface } from "./interface";

export interface IChooseImageProps {
  name: string;
  label: string;
  data?: IPerson;
  textError?: string;
  setFiles: React.Dispatch<React.SetStateAction<FileInterface[]>>;
  files: FileInterface[];
  defaultImage?: string[];
}

export function ChooseImage(props: IChooseImageProps) {
  return (
    <Stack>
      <LabelImage />
      <Stack>
        {props.data ? (
          <ImageUpdateComponent data={props.data} />
        ) : (
          <ImageComponent
            setFiles={props.setFiles}
            files={props.files}
            defaultImage={props.defaultImage}
          />
        )}

        {props.textError ? <Errortext error={props.textError} /> : <Helptext />}
      </Stack>
    </Stack>
  );
}
