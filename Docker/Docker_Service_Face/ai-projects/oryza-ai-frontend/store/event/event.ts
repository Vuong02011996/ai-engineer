import { EventSliceInterface, SocketEventData } from "@/models/redux.model";
import { createSlice } from "@reduxjs/toolkit";

let initialState: EventSliceInterface = {
  data: null,
};

const common = createSlice({
  name: "event",
  initialState,
  reducers: {
    setDataEvent(state, action) {
      const { data } = action.payload;
      state.data = data;
    },
  },
});

const { reducer, actions } = common;

export const { setDataEvent } = actions;

export default reducer;
