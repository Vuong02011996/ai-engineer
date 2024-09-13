import { CameraPersonEvent } from "@/containers/identification-profile/user/socket";
import { createSlice } from "@reduxjs/toolkit";

interface SliceInterface {
  data: CameraPersonEvent | null;
}

let initialState: SliceInterface = {
  data: null,
};

const common = createSlice({
  name: "camera-person",
  initialState,
  reducers: {
    addData(state, action) {
      const { data } = action.payload;
      state.data = data;
    },
  },
});

const { reducer, actions } = common;

export const { addData } = actions;

export default reducer;
