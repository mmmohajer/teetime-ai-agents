import { createSlice } from "@reduxjs/toolkit";

const reducerObject = {};
reducerObject["setScrollPos"] = (state, action) => action.payload;

const slice = createSlice({
  name: "scrollPos",
  initialState: 0,
  reducers: reducerObject,
});

export const { setScrollPos } = slice.actions;
export default slice.reducer;
