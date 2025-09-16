import { createSlice } from "@reduxjs/toolkit";

const reducerObject = {};

reducerObject["addAlertItem"] = (state, action) => {
  const curState = [...state];
  curState.push({ ...action.payload });
  return curState;
};

reducerObject["updateAlertDisplay"] = (state, action) => {
  let curState = [...state];
  const curKey = action.payload.key;
  const curAlert = curState.find((item) => item.key === curKey);
  if (curAlert) {
    curAlert.display = action.payload.display;
  }
};

reducerObject["removeAlertItem"] = (state, action) => {
  let curState = [...state];
  const curKey = action.payload.key;
  curState = curState.filter((item) => item.key !== curKey);
  return curState;
};

reducerObject["clearAlert"] = (state, action) => {
  return [];
};

const slice = createSlice({
  name: "alert",
  initialState: [],
  reducers: reducerObject,
});

export const { addAlertItem, removeAlertItem, updateAlertDisplay, clearAlert } =
  slice.actions;
export default slice.reducer;
