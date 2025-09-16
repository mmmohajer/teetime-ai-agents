import { createSlice } from "@reduxjs/toolkit";

const reducerObject = {};
reducerObject["setAccessToken"] = (state, action) => action.payload;
reducerObject["clearAccessToken"] = (state, action) => "";

const slice = createSlice({
  name: "accessToken",
  initialState: "",
  reducers: reducerObject,
});

export const { setAccessToken, clearAccessToken } = slice.actions;
export default slice.reducer;
