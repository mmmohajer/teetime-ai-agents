import { createSlice } from "@reduxjs/toolkit";

const reducerObject = {};
reducerObject["setActiveSubMenuItem"] = (state, action) => action.payload;

const slice = createSlice({
  name: "activeMenuItem",
  initialState: "",
  reducers: reducerObject,
});

export const { setActiveSubMenuItem } = slice.actions;
export default slice.reducer;
