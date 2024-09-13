import { ProcessSliceInterface } from "@/models/redux.model";
import { createSlice } from "@reduxjs/toolkit";

let initialState: ProcessSliceInterface = {
  data: null,
};

const common = createSlice({
  name: "process",
  initialState,
  reducers: {
    setProcess(state, action) {
      const { data } = action.payload;
      state.data = data;
    },
  },
});

const { reducer, actions } = common;

export const { setProcess } = actions;

export default reducer;
