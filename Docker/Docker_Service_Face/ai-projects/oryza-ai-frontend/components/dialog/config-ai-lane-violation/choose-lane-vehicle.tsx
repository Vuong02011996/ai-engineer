import React, { useState } from 'react';
import CheckboxCustom from "@/components/common/checkbox";
import { all_classes } from './lane-vehicle';
import { SelectModel } from "@/models/select";

interface IChooseLaneVehicleMultipleProps {
  laneIndex: number;
  onChange: (newValue: { item: any; checked: boolean; laneIndex: number }[]) => void;
  value: { item: any; checked: boolean; laneIndex: number }[];
}

export function ChooseLaneVehicleMultiple(
  props: IChooseLaneVehicleMultipleProps
) {
  const allClassesArray = Object.entries(all_classes).map(([key, value]) => ({
    id: Number(key),
    name: value,
  }));

  const [options, setOptions] = useState<SelectModel[]>(
    allClassesArray.map((item) => {
      return {
        id: item.id.toString(),
        name: item.name,
      };
    })
  );

  const handleChange = (newItem: any, checked: boolean) => {
    const updatedValue = props.value.map((v) =>
      v.item === newItem ? { ...v, checked } : v
    );

    if (!updatedValue.some((v) => v.item === newItem)) {
      updatedValue.push({ item: newItem, checked, laneIndex: props.laneIndex });
    }

    props.onChange(updatedValue);
  };

  return (
    <div className="flex flex-row items-center py-1 justify-between">
      <div className='w-[30%]'>
      <p className="text-[#323232] text-[14px] font-medium">
        Phương tiện được đi trên làn đường {props.laneIndex}
      </p>
      </div>
      <div className="w-[70%] flex flex-row items-center space-x-2">
        {options.map((option) => {
          const isChecked = props.value.some((v) => v.item === option.id && v.checked);
          return (
            <CheckboxCustom
              key={option.id}
              label={option.name}
              onChange={(checked) => {
                handleChange(option.id, checked);
              }}
              defaultChecked={isChecked}
            />
          );
        })}
      </div>
    </div>
  );
}