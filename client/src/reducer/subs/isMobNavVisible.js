import { createSlice } from "@reduxjs/toolkit";

const reducerObject = {};
reducerObject["showMobNav"] = (state, action) => true;
reducerObject["hideMobNav"] = (state, action) => false;
reducerObject["toggleMobNav"] = (state, action) => !state;

const slice = createSlice({
  name: "isMobNavVisible",
  initialState: false,
  reducers: reducerObject,
});

export const { showMobNav, hideMobNav, toggleMobNav } = slice.actions;
export default slice.reducer;
