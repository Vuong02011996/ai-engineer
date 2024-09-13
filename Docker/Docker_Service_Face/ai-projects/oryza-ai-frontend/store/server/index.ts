import { ServeSliceInterface } from "@/models/redux.model";
import { createSlice } from "@reduxjs/toolkit";

let initialState: ServeSliceInterface = {
  server: null,
  service: null,
  info_server: null,
};

const common = createSlice({
  name: "server",
  initialState,
  reducers: {
    setServer(state, action) {
      const { data } = action.payload;
      state.server = data;
    },
    setService(state, action) {
      const { data } = action.payload;
      state.service = data;
    },
    setInfoServer(state, action) {
      const { data } = action.payload;
      state.info_server = data;
    },
  },
});

const { reducer, actions } = common;

export const { setServer, setService, setInfoServer } = actions;

export default reducer;
