import { createSlice } from "@reduxjs/toolkit";

const reducerObject = {};
reducerObject["setMainContainerWidth"] = (state, action) => action.payload;

const slice = createSlice({
  name: "mainContainerWidth",
  initialState: 0,
  reducers: reducerObject,
});

export const { setMainContainerWidth } = slice.actions;
export default slice.reducer;
