import { SelectModel } from "@/models/select";
import * as React from "react";
import { useEffect, useState } from "react";
import AutoCompleteCustom from "../common/autocomplete";
import { personApi } from "@/api-client/identification-profile/person";
import { useAuth } from "@/hooks/auth-hook";

interface ExtendedSelectModel extends SelectModel {
  images: { id: string; url: string; name: string }[];
}

export interface IChooseIdentificationUserProps {
  name: string;
  label: string;
  value?: any;
  defaultValue?: string;
  textError?: string;
  onChange?: (v: any) => void;
  onClose?: () => void;
}

export function ChooseIdentificationUser(props: IChooseIdentificationUserProps) {
  const [options, setOptions] = useState<ExtendedSelectModel[]>([]);
  const [value, setValue] = useState<SelectModel | null>(null);
  const [images, setImages] = useState<{ id: string; url: string; name: string }[]>([]); // State for images
  const { profile } = useAuth();
  let companyId = profile?.company?.id ?? "";

  const getData = React.useCallback(async () => {
    try {
      let { data } = await personApi.getByCompany({
        page: 0,
        page_break: false,
        data_search: ""
      }, companyId);
      
      let option = data.map((item: any) => {
        return {
          id: item?.id ?? "",
          name: item?.name ?? "",
          images: item?.images ?? []
        };
      });

      console.log("option", option);
      console.log("props", props);
      
      if (props?.value) {
        let findValue = option.find(
          (item: any) => item?.id === props?.value?.id
        );

        if (findValue) {
          setValue(findValue);
          setImages(findValue.images); // Set images for the selected value
        }
      }

      setOptions(option);
    } catch (error) {
      console.error(error);
    }
  }, [props.value, companyId]);

  useEffect(() => {
    getData();
  }, [getData]);

  console.log("value search", value);

  return (
    <div>
      <AutoCompleteCustom
        label={props.label}
        options={options}
        required
        value={value}
        name={props.name}
        textError={props.textError}
        onChange={(event, value, reason, details) => {
          console.log({ event, value, reason, details });
          setValue(value);
          if (value) {
            const selectedOption = options.find(option => option.id === value.id);
            if (selectedOption) {
              setImages(selectedOption.images); // Update images when a new option is selected
            }
          }
          if (props.onChange) props.onChange(value?.id);
        }}
      />
      <div style={{ display: 'flex', flexDirection: 'row', flexWrap: 'wrap' }}>
        {images.map((image, index) => (
          <img key={index} src={image.url} alt={image.name} style={{ width: '100px', height: '100px', margin: '5px' }} />
        ))}
      </div>
    </div>
  );
}