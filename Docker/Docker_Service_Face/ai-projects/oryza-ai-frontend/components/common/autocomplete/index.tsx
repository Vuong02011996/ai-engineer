import { SelectModel } from "@/models/select";
import { useAutocomplete } from "@mui/base/useAutocomplete";
import {
  AutocompleteChangeDetails,
  AutocompleteChangeReason,
  InputLabel,
  Stack,
  Typography,
} from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
import clsx from "clsx";
import { SyntheticEvent, useCallback } from "react";

export interface IAutoCompleteCustomProps {
  label?: string;
  required?: boolean;
  options: SelectModel[];
  name?: string;
  onScroll?: () => void;
  textError?: string;
  value?: any;
  onChange:
    | ((
        event: SyntheticEvent<Element, Event>,
        value: any,
        reason: AutocompleteChangeReason,
        details?: AutocompleteChangeDetails<any> | undefined
      ) => void)
    | undefined;
}

export default function AutoCompleteCustom(props: IAutoCompleteCustomProps) {
  const { label, required, options, textError, onChange } = props;

  const {
    getRootProps,
    getInputLabelProps,
    getInputProps,
    getListboxProps,
    getOptionProps,
    groupedOptions,
  } = useAutocomplete({
    id: "use-autocomplete-demo",
    options: options,
    value: props.value || null,
    getOptionLabel: (option) => option?.name,
    onChange: onChange,
  });

  return (
    <div className="relative">
      <div {...getRootProps()} className="flex flex-col relative">
        <InputLabel
          {...getInputLabelProps()}
          sx={{ fontSize: 14, fontWeight: 400, color: "#55595D", mb: "6px" }}
        >
          {label}{" "}
          <span
            className={clsx(
              "text-[#E42727] text-[13px]",
              required ? "inline-block" : "hidden"
            )}
          >
            (✶)
          </span>
        </InputLabel>

        <input
          name={props.name}
          className={clsx(
            "text-[16px] text-[#323232] font-normal border border-[#E3E5E5] outline-none rounded-md px-4 py-3 leading-5 transition-all duration-300 ",
            "focus:border-[#78C6E7] focus:border-2"
          )}
          {...getInputProps()}
        />
      </div>
      {groupedOptions.length > 0 ? (
        <ul
          className={clsx(
            "absolute max-h-[300px] overflow-auto bg-white shadow-shadown1  top-[100%] w-full z-9999"
          )}
          {...getListboxProps()}
          onScroll={(e) => {
            const { scrollHeight, scrollTop, clientHeight } = e.currentTarget;

            if (scrollHeight - scrollTop === clientHeight) {
              // handle scroll when scroll to bottom
              if (props.onScroll) props.onScroll();
            }
          }}
        >
          {(groupedOptions as typeof options).map((option, index) => (
            <li
              key={option.id}
              {...getOptionProps({ option, index })}
              className="p-2 hover:bg-[#FAF8FF] transition-colors duration-150 cursor-pointer"
            >
              {option?.name}
            </li>
          ))}
        </ul>
      ) : null}

      {textError && (
        <Stack
          direction={"row"}
          spacing={"5px"}
          sx={{ alignItems: "center", mt: "4px" }}
        >
          <Stack
            sx={{
              width: "13px",
              height: "13px",
              alignItems: "center",
              justifyContent: "center",
              background: "#E42727",
              borderRadius: "50%",
            }}
          >
            <CloseIcon sx={{ color: "#fff", fontSize: 10, fontWeight: 600 }} />
          </Stack>

          <Typography
            sx={{
              fontSize: 12,
              fontWeight: 400,
              color: "#E42727",
            }}
          >
            {textError}
          </Typography>
        </Stack>
      )}
    </div>
  );
}
