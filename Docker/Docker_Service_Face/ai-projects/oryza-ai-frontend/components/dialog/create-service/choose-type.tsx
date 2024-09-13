import CloseIcon from "@mui/icons-material/Close";
import {
  FormControl,
  FormControlLabel,
  FormLabel,
  Radio,
  RadioGroup,
  Stack,
  Typography,
} from "@mui/material";

export interface IChooseTypeCameraProps {
  defaultValue?: string;
  textError?: string;
  onChange?: (e: any) => void;
  value?: string;
}

export function ChooseTypeCamera(props: IChooseTypeCameraProps) {
  const { defaultValue, onChange, value } = props;

  const options = [
    {
      id: "AI_SERVICE",
      name: "Dịch vụ Oryza AI",
    },
    {
      id: "AI_CAMERA",
      name: "AI có sẵn trên camera",
    },
  ];
  return (
    <FormControl
      className="w-full"
      sx={{
        "& .Mui-focused": {
          color: "#55595d",
        },
        userSelect: "none",
      }}
    >
      <FormLabel
        id="services-type"
        sx={{
          color: "#55595d !important",
          fontSize: "14px",
          fontWeight: 400,
          ":focus": {},
        }}
      >
        Chọn loại AI trên camera{" "}
        <span className="text-[#E42727] text-[13px]">(✶)</span>
      </FormLabel>
      <RadioGroup
        aria-labelledby="services-type"
        defaultValue={defaultValue}
        value={value}
        name="type"
        sx={{
          display: "flex",
          flexDirection: "row",
        }}
        onChange={(e) => {
          if (onChange) onChange(e.target.value);
        }}
      >
        {options.map((item) => (
          <FormControlLabel
            key={item.id}
            value={item.id}
            control={
              <Radio
                className=""
                size="small"
                sx={{
                  color: "#55595d",
                }}
              />
            }
            label={<p className="text-grayOz" style={{fontSize: "14px", fontWeight: 400}}> {item.name}</p>}
            sx={{
              "& .Mui-checked": {
                "& + .MuiFormControlLabel-label > p": {
                  color: "#323232",
                },
              },
            }}
          />
        ))}
      </RadioGroup>
      {props.textError && (
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
            {props.textError}
          </Typography>
        </Stack>
      )}
    </FormControl>
  );
}
