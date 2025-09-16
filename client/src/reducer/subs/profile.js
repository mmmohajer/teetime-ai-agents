import { createSlice } from "@reduxjs/toolkit";

const reducerObject = {};
reducerObject["setProfile"] = (state, action) => action.payload;
reducerObject["clearProfile"] = (state, action) => {};

const slice = createSlice({
  name: "profile",
  initialState: {},
  reducers: reducerObject,
});

export const { setProfile, clearProfile } = slice.actions;
export default slice.reducer;
