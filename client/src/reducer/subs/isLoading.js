import { createSlice } from "@reduxjs/toolkit";

const reducerObject = {};
reducerObject["setLoading"] = (state, action) => state + 1;
reducerObject["setLoaded"] = (state, action) => {
  if (state > 0) {
    return state - 1;
  } else {
    return 0;
  }
};
reducerObject["clearLoading"] = (state, action) => 0;

const slice = createSlice({
  name: "isLoading",
  initialState: 0,
  reducers: reducerObject,
});

export const { setLoading, setLoaded, clearLoading } = slice.actions;
export default slice.reducer;
