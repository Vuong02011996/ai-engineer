import { configureStore } from "@reduxjs/toolkit";
import eventSiles from "./event/event";
import serverSiles from "./server";
import cameraPersonSiles from "./camra-person";
import processSiles from "./process";

const rootReducer = {
  event: eventSiles,
  server: serverSiles,
  cameraPerson: cameraPersonSiles,
  process: processSiles,
};

const store = configureStore({
  reducer: rootReducer,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({ serializableCheck: false }),
});

export default store;

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
